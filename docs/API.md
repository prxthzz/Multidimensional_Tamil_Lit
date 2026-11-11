# API Documentation (v1 REST Interface)

## Overview
All production APIs are under `/api/v1/` and return standard JSON schemas with `X-Request-ID` and `X-Process-Time-MS` headers.

## Key Endpoints

### 1. Authentication (`/api/v1/auth`)
- `POST /api/v1/auth/login`: Authenticate user, return JWT token.
- `GET /api/v1/auth/me`: Get current authenticated user profile & role.

### 2. Search & Analysis (`/api/v1/search`)
- `POST /api/v1/search/analyze`: Perform multi-dimensional analysis, hybrid retrieval, 3-score calculation, and LLM synthesis.

### 3. Scientific Ontology (`/api/v1/scientific`)
- `GET /api/v1/scientific/concepts`: List 54 curated scientific concepts across 8 domains.

### 4. Expert Review Workflow (`/api/v1/reviews`)
- `POST /api/v1/reviews/submit`: Submit expert approval/rejection decision.
- `GET /api/v1/reviews/pending`: List pending evidence records awaiting review.

### 5. Evaluation & Ablation (`/api/v1/evaluation`)
- `GET /api/v1/evaluation/latest`: Fetch latest genuine benchmark evaluation and ablation comparison.

### 6. Exports (`/api/v1/export`)
- `POST /api/v1/export/report?format=json|csv|txt`: Export research analysis report.
