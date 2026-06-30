from datetime import UTC, datetime
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.billing.models import BillingAccount, BillingProfile, BillingQuota, BudgetControl, Discount, EnterpriseContract, Invoice, PaymentMethod, Subscription, SubscriptionPlan, UsageRecord
from app.billing.schemas import BillingAccountCreate, BillingAccountOut, BillingAnalyticsSummary, BillingProfileCreate, BudgetControlCreate, CreditTransactionCreate, CreditTransactionOut, DiscountCreate, EnterpriseContractCreate, InvoiceOut, PlanCreate, PlanOut, QuotaCreate, SubscriptionCreate, SubscriptionOut, UsageRecordCreate, UsageRecordOut
from app.billing.service import account_out, billing_summary, create_credit_transaction, create_subscription_for_account, credit_out, ensure_plan_seed, invoice_out, plan_out, record_usage, subscription_out, usage_out
from app.core.database import get_db
from app.identity.audit import audit
from app.identity.dependencies import CurrentUser, require_permission
from app.identity.rbac import Permission

router = APIRouter(prefix="/billing", tags=["billing"])


@router.get("/plans", response_model=list[PlanOut])
async def list_plans(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    await ensure_plan_seed(db)
    rows = (await db.execute(select(SubscriptionPlan).where(SubscriptionPlan.deleted_at.is_(None)).order_by(SubscriptionPlan.base_price_cents.asc()))).scalars().all()
    await db.commit()
    return [PlanOut(**plan_out(item)) for item in rows]


@router.post("/plans", response_model=PlanOut, status_code=status.HTTP_201_CREATED)
async def create_plan(payload: PlanCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = SubscriptionPlan(slug=payload.slug, name=payload.name, billing_interval=payload.billing_interval, base_price_cents=payload.base_price_cents, currency=payload.currency, included_features=payload.included_features, usage_limits=payload.usage_limits, credit_allocation=payload.credit_allocation, support_level=payload.support_level, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return PlanOut(**plan_out(item))


@router.post("/account", response_model=BillingAccountOut, status_code=status.HTTP_201_CREATED)
async def create_billing_account(payload: BillingAccountCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = BillingAccount(organization_id=current.organization_id, status="active", plan_slug=payload.plan_slug, billing_email=payload.billing_email, provider=payload.provider, metadata_json=payload.metadata_json)
    db.add(item)
    await db.flush()
    await audit(db, "billing.account.created", current.user.id, current.organization_id, "billing_account", item.id)
    await db.commit()
    return BillingAccountOut(**account_out(item))


@router.get("/account", response_model=list[BillingAccountOut])
async def list_billing_accounts(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(BillingAccount).where(BillingAccount.organization_id == current.organization_id, BillingAccount.deleted_at.is_(None)).order_by(BillingAccount.created_at.desc()))).scalars().all()
    return [BillingAccountOut(**account_out(item)) for item in rows]


@router.post("/subscriptions", response_model=SubscriptionOut, status_code=status.HTTP_201_CREATED)
async def create_subscription(payload: SubscriptionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    account = await db.get(BillingAccount, payload.billing_account_id)
    if account is None or account.organization_id != current.organization_id:
        raise HTTPException(status_code=404, detail="Billing account not found")
    subscription = await create_subscription_for_account(db, current, payload)
    await audit(db, "billing.subscription.created", current.user.id, current.organization_id, "subscription", subscription.id)
    await db.commit()
    return SubscriptionOut(**subscription_out(subscription))


@router.get("/subscriptions", response_model=list[SubscriptionOut])
async def list_subscriptions(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Subscription).where(Subscription.organization_id == current.organization_id, Subscription.deleted_at.is_(None)).order_by(Subscription.created_at.desc()))).scalars().all()
    return [SubscriptionOut(**subscription_out(item)) for item in rows]


@router.post("/usage", response_model=UsageRecordOut, status_code=status.HTTP_201_CREATED)
async def create_usage_record(payload: UsageRecordCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    record = await record_usage(db, current, payload)
    await db.commit()
    return UsageRecordOut(**usage_out(record))


@router.get("/usage", response_model=list[UsageRecordOut])
async def list_usage(workspace_id: UUID, current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(UsageRecord).where(UsageRecord.organization_id == current.organization_id, UsageRecord.workspace_id == workspace_id).order_by(UsageRecord.created_at.desc()).limit(100))).scalars().all()
    return [UsageRecordOut(**usage_out(item)) for item in rows]


@router.post("/credits", response_model=CreditTransactionOut, status_code=status.HTTP_201_CREATED)
async def create_credit(payload: CreditTransactionCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    transaction = await create_credit_transaction(db, current, payload)
    await db.commit()
    return CreditTransactionOut(**credit_out(transaction))


@router.post("/quotas", status_code=status.HTTP_201_CREATED)
async def create_quota(payload: QuotaCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = BillingQuota(organization_id=current.organization_id, workspace_id=payload.workspace_id, meter_name=payload.meter_name, limit_type=payload.limit_type, limit_value=payload.limit_value, warning_threshold=payload.warning_threshold, grace_policy=payload.grace_policy, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "meter_name": item.meter_name, "status": item.status}


@router.get("/invoices", response_model=list[InvoiceOut])
async def list_invoices(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    rows = (await db.execute(select(Invoice).where(Invoice.organization_id == current.organization_id, Invoice.deleted_at.is_(None)).order_by(Invoice.created_at.desc()).limit(100))).scalars().all()
    return [InvoiceOut(**invoice_out(item)) for item in rows]


@router.post("/discounts", status_code=status.HTTP_201_CREATED)
async def create_discount(payload: DiscountCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = Discount(organization_id=current.organization_id, code=payload.code, discount_type=payload.discount_type, value=payload.value, rules=payload.rules, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "code": item.code, "status": item.status}


@router.post("/profiles", status_code=status.HTTP_201_CREATED)
async def create_profile(payload: BillingProfileCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = BillingProfile(organization_id=current.organization_id, billing_account_id=payload.billing_account_id, company_name=payload.company_name, billing_email=payload.billing_email, billing_contacts=payload.billing_contacts, address=payload.address, tax_info=payload.tax_info, invoice_preferences=payload.invoice_preferences, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "company_name": item.company_name}


@router.post("/contracts", status_code=status.HTTP_201_CREATED)
async def create_contract(payload: EnterpriseContractCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    item = EnterpriseContract(organization_id=current.organization_id, billing_account_id=payload.billing_account_id, contract_number=payload.contract_number, pricing_model=payload.pricing_model, committed_amount_cents=payload.committed_amount_cents, terms=payload.terms, metadata_json=payload.metadata_json, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "contract_number": item.contract_number, "status": item.status}


@router.post("/budgets", status_code=status.HTTP_201_CREATED)
async def create_budget(payload: BudgetControlCreate, current: CurrentUser = Depends(require_permission(Permission.ORG_WRITE)), db: AsyncSession = Depends(get_db)):
    forecast = {"end_of_month_cents": payload.monthly_budget_cents, "risk": "low"}
    item = BudgetControl(organization_id=current.organization_id, workspace_id=payload.workspace_id, name=payload.name, scope_type=payload.scope_type, scope_ref=payload.scope_ref, monthly_budget_cents=payload.monthly_budget_cents, hard_cap_cents=payload.hard_cap_cents, alert_thresholds=payload.alert_thresholds, forecast_state=forecast, created_by_user_id=current.user.id, updated_by_user_id=current.user.id)
    db.add(item)
    await db.commit()
    return {"id": item.id, "name": item.name, "forecast": item.forecast_state}


@router.get("/analytics", response_model=BillingAnalyticsSummary)
async def analytics(current: CurrentUser = Depends(require_permission(Permission.ORG_READ)), db: AsyncSession = Depends(get_db)):
    return BillingAnalyticsSummary(**await billing_summary(db, current))