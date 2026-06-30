from sqlalchemy import DateTime, ForeignKey, Index, Integer, Numeric, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.core.database import Base
from app.core.models import ActorMixin, IdMixin, OrganizationScopedMixin, SoftDeleteMixin, TimestampMixin, WorkspaceScopedMixin


class BillingAccount(IdMixin, TimestampMixin, SoftDeleteMixin, OrganizationScopedMixin, Base):
    __tablename__ = "billing_accounts"
    status: Mapped[str] = mapped_column(String(40), default="pending")
    plan_slug: Mapped[str | None] = mapped_column(String(80))
    billing_email: Mapped[str | None] = mapped_column(String(320))
    provider: Mapped[str | None] = mapped_column(String(60))
    provider_customer_id: Mapped[str | None] = mapped_column(String(180))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SubscriptionPlaceholder(IdMixin, TimestampMixin, SoftDeleteMixin, OrganizationScopedMixin, Base):
    __tablename__ = "subscription_placeholders"
    billing_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("billing_accounts.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="inactive")
    plan_slug: Mapped[str] = mapped_column(String(80))
    current_period_start: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[str | None] = mapped_column(DateTime(timezone=True))
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class SubscriptionPlan(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, Base):
    __tablename__ = "subscription_plans"
    __table_args__ = (UniqueConstraint("slug", name="uq_subscription_plan_slug"),)
    slug: Mapped[str] = mapped_column(String(80), index=True)
    name: Mapped[str] = mapped_column(String(160))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    billing_interval: Mapped[str] = mapped_column(String(40), default="monthly")
    base_price_cents: Mapped[int] = mapped_column(Integer, default=0)
    currency: Mapped[str] = mapped_column(String(12), default="usd")
    included_features: Mapped[list[str]] = mapped_column(JSONB, default=list)
    usage_limits: Mapped[dict] = mapped_column(JSONB, default=dict)
    credit_allocation: Mapped[dict] = mapped_column(JSONB, default=dict)
    support_level: Mapped[str] = mapped_column(String(80), default="standard")
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Subscription(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "subscriptions"
    billing_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("billing_accounts.id", ondelete="CASCADE"), index=True)
    plan_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("subscription_plans.id", ondelete="SET NULL"), index=True)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    billing_interval: Mapped[str] = mapped_column(String(40), default="monthly")
    current_period_start: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    current_period_end: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    trial_end: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    cancel_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    provider_subscription_id: Mapped[str | None] = mapped_column(String(180), index=True)
    contract_ref: Mapped[str | None] = mapped_column(String(180), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class UsageRecord(IdMixin, TimestampMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "billing_usage_records"
    subscription_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("subscriptions.id", ondelete="SET NULL"), index=True)
    meter_name: Mapped[str] = mapped_column(String(80), index=True)
    quantity: Mapped[float] = mapped_column(Numeric(18, 6))
    unit: Mapped[str] = mapped_column(String(40), default="count")
    source: Mapped[str] = mapped_column(String(80), default="platform", index=True)
    resource_type: Mapped[str | None] = mapped_column(String(80), index=True)
    resource_id: Mapped[str | None] = mapped_column(String(180), index=True)
    cost_cents: Mapped[int] = mapped_column(Integer, default=0)
    occurred_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class CreditTransaction(IdMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "credit_transactions"
    billing_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("billing_accounts.id", ondelete="CASCADE"), index=True)
    transaction_type: Mapped[str] = mapped_column(String(60), index=True)
    credit_amount: Mapped[int] = mapped_column(Integer)
    balance_after: Mapped[int] = mapped_column(Integer, default=0)
    source: Mapped[str] = mapped_column(String(80), default="system", index=True)
    service_scope: Mapped[str | None] = mapped_column(String(80), index=True)
    expires_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class BillingQuota(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "billing_quotas"
    meter_name: Mapped[str] = mapped_column(String(80), index=True)
    limit_type: Mapped[str] = mapped_column(String(40), default="soft", index=True)
    limit_value: Mapped[float] = mapped_column(Numeric(18, 6))
    warning_threshold: Mapped[float | None] = mapped_column(Numeric(8, 4))
    current_usage: Mapped[float] = mapped_column(Numeric(18, 6), default=0)
    period_start: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    period_end: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    grace_policy: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class Invoice(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "invoices"
    billing_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("billing_accounts.id", ondelete="CASCADE"), index=True)
    invoice_number: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    currency: Mapped[str] = mapped_column(String(12), default="usd")
    subtotal_cents: Mapped[int] = mapped_column(Integer, default=0)
    discount_cents: Mapped[int] = mapped_column(Integer, default=0)
    credits_applied_cents: Mapped[int] = mapped_column(Integer, default=0)
    tax_cents: Mapped[int] = mapped_column(Integer, default=0)
    total_cents: Mapped[int] = mapped_column(Integer, default=0)
    provider_invoice_id: Mapped[str | None] = mapped_column(String(180), index=True)
    pdf_file_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), ForeignKey("files.id", ondelete="SET NULL"), index=True)
    issued_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    due_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    paid_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class InvoiceLineItem(IdMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "invoice_line_items"
    invoice_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("invoices.id", ondelete="CASCADE"), index=True)
    description: Mapped[str] = mapped_column(Text)
    meter_name: Mapped[str | None] = mapped_column(String(80), index=True)
    quantity: Mapped[float | None] = mapped_column(Numeric(18, 6))
    unit_amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class Discount(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "discounts"
    code: Mapped[str] = mapped_column(String(80), index=True)
    discount_type: Mapped[str] = mapped_column(String(40), default="percentage", index=True)
    value: Mapped[float] = mapped_column(Numeric(12, 4))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    starts_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    ends_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    rules: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class BillingProfile(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "billing_profiles"
    billing_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("billing_accounts.id", ondelete="CASCADE"), index=True)
    company_name: Mapped[str | None] = mapped_column(String(220))
    billing_email: Mapped[str | None] = mapped_column(String(320))
    billing_contacts: Mapped[list[dict]] = mapped_column(JSONB, default=list)
    address: Mapped[dict] = mapped_column(JSONB, default=dict)
    tax_info: Mapped[dict] = mapped_column(JSONB, default=dict)
    invoice_preferences: Mapped[dict] = mapped_column(JSONB, default=dict)


class EnterpriseContract(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "enterprise_contracts"
    billing_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("billing_accounts.id", ondelete="CASCADE"), index=True)
    contract_number: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    status: Mapped[str] = mapped_column(String(40), default="draft", index=True)
    pricing_model: Mapped[str] = mapped_column(String(60), default="hybrid", index=True)
    start_date: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    end_date: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)
    committed_amount_cents: Mapped[int] = mapped_column(Integer, default=0)
    terms: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class PaymentProviderConfig(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, Base):
    __tablename__ = "payment_provider_configs"
    provider: Mapped[str] = mapped_column(String(80), index=True)
    status: Mapped[str] = mapped_column(String(40), default="disabled", index=True)
    priority: Mapped[int] = mapped_column(Integer, default=100)
    secret_ref: Mapped[str | None] = mapped_column(Text)
    capabilities: Mapped[list[str]] = mapped_column(JSONB, default=list)
    config: Mapped[dict] = mapped_column(JSONB, default=dict)


class PaymentMethod(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, Base):
    __tablename__ = "payment_methods"
    billing_account_id: Mapped[str] = mapped_column(UUID(as_uuid=True), ForeignKey("billing_accounts.id", ondelete="CASCADE"), index=True)
    provider: Mapped[str] = mapped_column(String(80), index=True)
    provider_payment_method_id: Mapped[str | None] = mapped_column(String(180), index=True)
    method_type: Mapped[str] = mapped_column(String(60), default="card", index=True)
    display_name: Mapped[str | None] = mapped_column(String(180))
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)
    billing_details: Mapped[dict] = mapped_column(JSONB, default=dict)
    metadata_json: Mapped[dict] = mapped_column(JSONB, default=dict)


class BudgetControl(IdMixin, TimestampMixin, SoftDeleteMixin, ActorMixin, OrganizationScopedMixin, WorkspaceScopedMixin, Base):
    __tablename__ = "budget_controls"
    name: Mapped[str] = mapped_column(String(180))
    scope_type: Mapped[str] = mapped_column(String(60), default="workspace", index=True)
    scope_ref: Mapped[str | None] = mapped_column(String(180), index=True)
    monthly_budget_cents: Mapped[int] = mapped_column(Integer, default=0)
    hard_cap_cents: Mapped[int | None] = mapped_column(Integer)
    alert_thresholds: Mapped[list[int]] = mapped_column(JSONB, default=list)
    forecast_state: Mapped[dict] = mapped_column(JSONB, default=dict)
    status: Mapped[str] = mapped_column(String(40), default="active", index=True)


class BillingAnalyticsRecord(IdMixin, TimestampMixin, OrganizationScopedMixin, Base):
    __tablename__ = "billing_analytics_records"
    metric_name: Mapped[str] = mapped_column(String(80), index=True)
    metric_value: Mapped[float] = mapped_column(Numeric(18, 6))
    currency: Mapped[str | None] = mapped_column(String(12))
    plan_slug: Mapped[str | None] = mapped_column(String(80), index=True)
    dimensions: Mapped[dict] = mapped_column(JSONB, default=dict)
    captured_at: Mapped[str | None] = mapped_column(DateTime(timezone=True), index=True)


Index("ix_billing_accounts_org_status", BillingAccount.organization_id, BillingAccount.status, BillingAccount.deleted_at)
Index("ix_subscriptions_org_status", Subscription.organization_id, Subscription.status, Subscription.current_period_end)
Index("ix_billing_usage_records_workspace_meter", UsageRecord.workspace_id, UsageRecord.meter_name, UsageRecord.occurred_at)
Index("ix_credit_transactions_account", CreditTransaction.billing_account_id, CreditTransaction.transaction_type, CreditTransaction.created_at)
Index("ix_billing_quotas_workspace_meter", BillingQuota.workspace_id, BillingQuota.meter_name, BillingQuota.status)
Index("ix_invoices_account_status", Invoice.billing_account_id, Invoice.status, Invoice.issued_at)
Index("ix_invoice_line_items_invoice", InvoiceLineItem.invoice_id, InvoiceLineItem.meter_name)
Index("ix_discounts_org_status", Discount.organization_id, Discount.status, Discount.code)
Index("ix_payment_methods_account_status", PaymentMethod.billing_account_id, PaymentMethod.status)
Index("ix_budget_controls_workspace_status", BudgetControl.workspace_id, BudgetControl.status)
Index("ix_billing_analytics_org_metric", BillingAnalyticsRecord.organization_id, BillingAnalyticsRecord.metric_name, BillingAnalyticsRecord.captured_at)