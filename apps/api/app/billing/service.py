from datetime import UTC, datetime, timedelta
from decimal import Decimal
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.billing.models import BillingAccount, BillingAnalyticsRecord, CreditTransaction, Invoice, Subscription, SubscriptionPlan, UsageRecord
from app.identity.dependencies import CurrentUser

PAYMENT_PROVIDER_CATALOG = ["stripe", "paddle", "lemon_squeezy", "paypal", "manual_invoicing"]
PLAN_SEEDS = [
    ("free", "Free", 0, "community", {"ai_employees": 1, "voice_minutes": 30, "api_requests": 1000}),
    ("starter", "Starter", 2900, "standard", {"ai_employees": 3, "voice_minutes": 500, "api_requests": 25000}),
    ("growth", "Growth", 9900, "priority", {"ai_employees": 10, "voice_minutes": 3000, "api_requests": 150000}),
    ("professional", "Professional", 24900, "priority", {"ai_employees": 25, "voice_minutes": 10000, "api_requests": 500000}),
    ("business", "Business", 49900, "premium", {"ai_employees": 75, "voice_minutes": 30000, "api_requests": 1500000}),
    ("enterprise", "Enterprise", 0, "enterprise", {"custom_contract": True}),
]


def plan_out(item: SubscriptionPlan) -> dict:
    return {"id": item.id, "slug": item.slug, "name": item.name, "status": item.status, "billing_interval": item.billing_interval, "base_price_cents": item.base_price_cents, "currency": item.currency, "included_features": item.included_features, "usage_limits": item.usage_limits, "credit_allocation": item.credit_allocation, "support_level": item.support_level, "metadata_json": item.metadata_json, "created_at": item.created_at}


def account_out(item: BillingAccount) -> dict:
    return {"id": item.id, "organization_id": item.organization_id, "status": item.status, "plan_slug": item.plan_slug, "billing_email": item.billing_email, "provider": item.provider, "provider_customer_id": item.provider_customer_id, "metadata_json": item.metadata_json, "created_at": item.created_at}


def subscription_out(item: Subscription) -> dict:
    return {"id": item.id, "organization_id": item.organization_id, "billing_account_id": item.billing_account_id, "plan_id": item.plan_id, "status": item.status, "billing_interval": item.billing_interval, "current_period_start": item.current_period_start, "current_period_end": item.current_period_end, "trial_end": item.trial_end, "cancel_at": item.cancel_at, "provider_subscription_id": item.provider_subscription_id, "contract_ref": item.contract_ref, "metadata_json": item.metadata_json, "created_at": item.created_at}


def usage_out(item: UsageRecord) -> dict:
    return {"id": item.id, "workspace_id": item.workspace_id, "subscription_id": item.subscription_id, "meter_name": item.meter_name, "quantity": float(item.quantity), "unit": item.unit, "source": item.source, "resource_type": item.resource_type, "resource_id": item.resource_id, "cost_cents": item.cost_cents, "occurred_at": item.occurred_at, "metadata_json": item.metadata_json, "created_at": item.created_at}


def credit_out(item: CreditTransaction) -> dict:
    return {"id": item.id, "billing_account_id": item.billing_account_id, "transaction_type": item.transaction_type, "credit_amount": item.credit_amount, "balance_after": item.balance_after, "source": item.source, "service_scope": item.service_scope, "expires_at": item.expires_at, "metadata_json": item.metadata_json, "created_at": item.created_at}


def invoice_out(item: Invoice) -> dict:
    return {"id": item.id, "billing_account_id": item.billing_account_id, "invoice_number": item.invoice_number, "status": item.status, "currency": item.currency, "subtotal_cents": item.subtotal_cents, "discount_cents": item.discount_cents, "credits_applied_cents": item.credits_applied_cents, "tax_cents": item.tax_cents, "total_cents": item.total_cents, "provider_invoice_id": item.provider_invoice_id, "pdf_file_id": item.pdf_file_id, "issued_at": item.issued_at, "due_at": item.due_at, "paid_at": item.paid_at, "metadata_json": item.metadata_json, "created_at": item.created_at}


async def ensure_plan_seed(db: AsyncSession) -> None:
    existing = int((await db.execute(select(func.count()).select_from(SubscriptionPlan))).scalar_one() or 0)
    if existing:
        return
    for slug, name, price, support, limits in PLAN_SEEDS:
        db.add(SubscriptionPlan(slug=slug, name=name, base_price_cents=price, support_level=support, billing_interval="monthly", currency="usd", included_features=["ai_employees", "conversations", "workflows", "api_access"], usage_limits=limits, credit_allocation={"monthly": max(price // 100, 100)}, metadata_json={"configurable": True}))
    await db.flush()


async def create_subscription_for_account(db: AsyncSession, current: CurrentUser, payload) -> Subscription:
    now = datetime.now(UTC)
    subscription = Subscription(organization_id=current.organization_id, billing_account_id=payload.billing_account_id, plan_id=payload.plan_id, status="active", billing_interval=payload.billing_interval, current_period_start=now, current_period_end=now + timedelta(days=365 if payload.billing_interval == "annual" else 30), metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(subscription)
    await db.flush()
    return subscription


async def record_usage(db: AsyncSession, current: CurrentUser, payload) -> UsageRecord:
    record = UsageRecord(organization_id=current.organization_id, workspace_id=payload.workspace_id, subscription_id=payload.subscription_id, meter_name=payload.meter_name, quantity=Decimal(str(payload.quantity)), unit=payload.unit, source=payload.source, resource_type=payload.resource_type, resource_id=payload.resource_id, cost_cents=payload.cost_cents, occurred_at=datetime.now(UTC), metadata_json=payload.metadata_json)
    db.add(record)
    await db.flush()
    return record


async def create_credit_transaction(db: AsyncSession, current: CurrentUser, payload) -> CreditTransaction:
    previous = (await db.execute(select(CreditTransaction).where(CreditTransaction.organization_id == current.organization_id, CreditTransaction.billing_account_id == payload.billing_account_id).order_by(CreditTransaction.created_at.desc()).limit(1))).scalar_one_or_none()
    previous_balance = previous.balance_after if previous else 0
    balance_after = previous_balance + payload.credit_amount
    transaction = CreditTransaction(organization_id=current.organization_id, billing_account_id=payload.billing_account_id, transaction_type=payload.transaction_type, credit_amount=payload.credit_amount, balance_after=balance_after, source=payload.source, service_scope=payload.service_scope, expires_at=payload.expires_at, metadata_json=payload.metadata_json)
    db.add(transaction)
    await db.flush()
    return transaction


async def billing_summary(db: AsyncSession, current: CurrentUser) -> dict:
    active_subscriptions = int((await db.execute(select(func.count()).select_from(Subscription).where(Subscription.organization_id == current.organization_id, Subscription.status == "active", Subscription.deleted_at.is_(None)))).scalar_one() or 0)
    usage_records = int((await db.execute(select(func.count()).select_from(UsageRecord).where(UsageRecord.organization_id == current.organization_id))).scalar_one() or 0)
    credit = (await db.execute(select(CreditTransaction).where(CreditTransaction.organization_id == current.organization_id).order_by(CreditTransaction.created_at.desc()).limit(1))).scalar_one_or_none()
    invoice_total = int((await db.execute(select(func.coalesce(func.sum(Invoice.total_cents), 0)).where(Invoice.organization_id == current.organization_id))).scalar_one() or 0)
    mrr = int((await db.execute(select(func.coalesce(func.sum(SubscriptionPlan.base_price_cents), 0)).select_from(Subscription).join(SubscriptionPlan, Subscription.plan_id == SubscriptionPlan.id, isouter=True).where(Subscription.organization_id == current.organization_id, Subscription.status == "active"))).scalar_one() or 0)
    return {"mrr_cents": mrr, "arr_cents": mrr * 12, "active_subscriptions": active_subscriptions, "usage_records": usage_records, "credit_balance": credit.balance_after if credit else 0, "invoice_total_cents": invoice_total, "forecast": {"end_of_month_cents": invoice_total + mrr, "credit_depletion": "stable", "capacity": "within_plan"}, "payment_provider_catalog": PAYMENT_PROVIDER_CATALOG}