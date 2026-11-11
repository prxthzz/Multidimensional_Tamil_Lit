# Operations Manual & Monitoring

## 1. System Operations
- **Backend Service**: `uvicorn api.main:app --host 127.0.0.1 --port 8000`
- **Frontend Service**: `npm run dev` in `frontend/` folder.
- **Database Seed / Migration**: `python -m src.database.seed`

## 2. Health & Monitoring Endpoints
- `GET /api/v1/health`: Checks system status, database connection, and index counts.
- `GET /api/v1/admin/statistics`: Reports corpus metrics, persisted evidence records, and expert reviews.
- `GET /api/v1/audit/logs`: Fetches recent security audit trails.

## 3. Logs & Observability
- All HTTP requests log latency, status, user ID, and `X-Request-ID`.
