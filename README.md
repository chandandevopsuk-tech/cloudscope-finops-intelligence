# CloudScope — FinOps Intelligence API

Analytics for cloud billing data: **account/service spend allocation**, robust MAD-based spikes and 7-day rolling-median spend forecasts. Designed as an auditable FinOps prototype with predictable results and no cloud credentials.

## Features
- Aggregate invoice line items by day, account and service
- Detect significant anomalies using prior observations (no current-day leakage)
- Report largest spend sources and forward budget estimates
- FastAPI/OpenAPI, CSV CLI, tests, Docker and CI

## Run
```bash
python -m pip install -e '.[dev]'
pytest
python -m cloudscope.cli examples/cloud-billing.csv --output finops.json
uvicorn cloudscope.api:app --reload
```

`POST /v1/analyse` with `{ "costs": [{"date":"2026-11-01","account":"prod","service":"compute","amount":42.50}] }`.

## Production limitations
- CSV import is intentionally vendor-neutral, not a direct AWS/Azure/GCP billing API integration.
- Forecast is a **median-based estimate**, not a trained forecasting model. Dates with no rows are not filled with zero; fill missing billing days upstream as appropriate. No currency conversion or commitment amortization.
- Add billing reconciliation, identity-bound tenancy, audit logging and alerting before production use. Keep billing account identifiers private.
