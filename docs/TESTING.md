# Testing Strategy & Test Pyramid

## 1. Overview
The testing architecture follows a strict test pyramid covering unit, integration, API, security, and benchmark evaluation suites.

## 2. Test Execution
```bash
# Run complete pytest suite
pytest

# Run specific test modules
pytest tests/test_api_v1_routes.py
pytest tests/test_database_models.py
```

## 3. Test Coverage Areas
- **Unit Tests**: Query normalization, BM25 tokenizer, 3-score calculation, relationship analyzer, LLM gateway, evidence guard.
- **Integration Tests**: Database models, ORM persistence, unified retrieval, dimensional pipeline, REST v1 API endpoints.
- **Security & RBAC Tests**: Authentication token verification, role permissions, audit log tracking.
