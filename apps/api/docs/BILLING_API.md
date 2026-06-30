# Billing API

## Plans and Accounts

- `GET /api/v1/billing/plans`
- `POST /api/v1/billing/plans`
- `POST /api/v1/billing/account`
- `GET /api/v1/billing/account`

## Subscriptions, Usage, Credits, Quotas

- `POST /api/v1/billing/subscriptions`
- `GET /api/v1/billing/subscriptions`
- `POST /api/v1/billing/usage`
- `GET /api/v1/billing/usage?workspace_id=...`
- `POST /api/v1/billing/credits`
- `POST /api/v1/billing/quotas`

## Invoices, Profiles, Contracts, Budgets

- `GET /api/v1/billing/invoices`
- `POST /api/v1/billing/discounts`
- `POST /api/v1/billing/profiles`
- `POST /api/v1/billing/contracts`
- `POST /api/v1/billing/budgets`
- `GET /api/v1/billing/analytics`