from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field


class PlanCreate(BaseModel):
    slug: str
    name: str
    billing_interval: str = "monthly"
    base_price_cents: int = 0
    currency: str = "usd"
    included_features: list[str] = Field(default_factory=list)
    usage_limits: dict = Field(default_factory=dict)
    credit_allocation: dict = Field(default_factory=dict)
    support_level: str = "standard"
    metadata_json: dict = Field(default_factory=dict)


class PlanOut(BaseModel):
    id: UUID
    slug: str
    name: str
    status: str
    billing_interval: str
    base_price_cents: int
    currency: str
    included_features: list[str]
    usage_limits: dict
    credit_allocation: dict
    support_level: str
    metadata_json: dict
    created_at: datetime


class BillingAccountCreate(BaseModel):
    plan_slug: str | None = None
    billing_email: str | None = None
    provider: str | None = None
    metadata_json: dict = Field(default_factory=dict)


class BillingAccountOut(BaseModel):
    id: UUID
    organization_id: UUID
    status: str
    plan_slug: str | None
    billing_email: str | None
    provider: str | None
    provider_customer_id: str | None
    metadata_json: dict
    created_at: datetime


class SubscriptionCreate(BaseModel):
    billing_account_id: UUID
    plan_id: UUID | None = None
    billing_interval: str = "monthly"
    metadata_json: dict = Field(default_factory=dict)


class SubscriptionOut(BaseModel):
    id: UUID
    organization_id: UUID
    billing_account_id: UUID
    plan_id: UUID | None
    status: str
    billing_interval: str
    current_period_start: datetime | None
    current_period_end: datetime | None
    trial_end: datetime | None
    cancel_at: datetime | None
    provider_subscription_id: str | None
    contract_ref: str | None
    metadata_json: dict
    created_at: datetime


class UsageRecordCreate(BaseModel):
    workspace_id: UUID
    subscription_id: UUID | None = None
    meter_name: str
    quantity: float
    unit: str = "count"
    source: str = "platform"
    resource_type: str | None = None
    resource_id: str | None = None
    cost_cents: int = 0
    metadata_json: dict = Field(default_factory=dict)


class UsageRecordOut(BaseModel):
    id: UUID
    workspace_id: UUID
    subscription_id: UUID | None
    meter_name: str
    quantity: float
    unit: str
    source: str
    resource_type: str | None
    resource_id: str | None
    cost_cents: int
    occurred_at: datetime | None
    metadata_json: dict
    created_at: datetime


class CreditTransactionCreate(BaseModel):
    billing_account_id: UUID
    transaction_type: str
    credit_amount: int
    source: str = "system"
    service_scope: str | None = None
    expires_at: datetime | None = None
    metadata_json: dict = Field(default_factory=dict)


class CreditTransactionOut(BaseModel):
    id: UUID
    billing_account_id: UUID
    transaction_type: str
    credit_amount: int
    balance_after: int
    source: str
    service_scope: str | None
    expires_at: datetime | None
    metadata_json: dict
    created_at: datetime


class QuotaCreate(BaseModel):
    workspace_id: UUID
    meter_name: str
    limit_type: str = "soft"
    limit_value: float
    warning_threshold: float | None = None
    grace_policy: dict = Field(default_factory=dict)


class InvoiceOut(BaseModel):
    id: UUID
    billing_account_id: UUID
    invoice_number: str
    status: str
    currency: str
    subtotal_cents: int
    discount_cents: int
    credits_applied_cents: int
    tax_cents: int
    total_cents: int
    provider_invoice_id: str | None
    pdf_file_id: UUID | None
    issued_at: datetime | None
    due_at: datetime | None
    paid_at: datetime | None
    metadata_json: dict
    created_at: datetime


class DiscountCreate(BaseModel):
    code: str
    discount_type: str = "percentage"
    value: float
    rules: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class BillingProfileCreate(BaseModel):
    billing_account_id: UUID
    company_name: str | None = None
    billing_email: str | None = None
    billing_contacts: list[dict] = Field(default_factory=list)
    address: dict = Field(default_factory=dict)
    tax_info: dict = Field(default_factory=dict)
    invoice_preferences: dict = Field(default_factory=dict)


class EnterpriseContractCreate(BaseModel):
    billing_account_id: UUID
    contract_number: str
    pricing_model: str = "hybrid"
    committed_amount_cents: int = 0
    terms: dict = Field(default_factory=dict)
    metadata_json: dict = Field(default_factory=dict)


class BudgetControlCreate(BaseModel):
    workspace_id: UUID
    name: str
    scope_type: str = "workspace"
    scope_ref: str | None = None
    monthly_budget_cents: int = 0
    hard_cap_cents: int | None = None
    alert_thresholds: list[int] = Field(default_factory=lambda: [50, 80, 100])


class BillingAnalyticsSummary(BaseModel):
    mrr_cents: int
    arr_cents: int
    active_subscriptions: int
    usage_records: int
    credit_balance: int
    invoice_total_cents: int
    forecast: dict
    payment_provider_catalog: list[str]