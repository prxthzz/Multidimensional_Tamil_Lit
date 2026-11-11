# Database Architecture & Schema Reference

## Primary Transactional Database
The platform utilizes **SQLAlchemy ORM** supporting both **PostgreSQL (+ pgvector)** and **SQLite**.

## Core Schemas & Tables

1. **`users`**: Identity, credentials (`pbkdf2_sha256`), RBAC roles.
2. **`audit_logs`**: Immutable log of user actions, requests, and administrative operations.
3. **`scientific_concepts`**: Curated scientific ontology concepts, canonical names, Tamil translations, aliases.
4. **`scientific_domains`**: 8 scientific domains (Physics, Astronomy, Environment, Agriculture, Biology, Medicine, Computer Science, Psychology).
5. **`verses`**: Classical Tamil literary corpus (Thirukkural, Thiruvarutpa) with normalized text and chapter metadata.
6. **`evidence_records`**: First-class evidence entity storing retrieval relevance %, evidence strength, interpretation confidence %, and provenance metadata.
7. **`expert_reviews`**: Audit log of human expert overrides, approvals, and rejections.
8. **`evaluation_runs`**: Reproducible benchmark evaluation run history.
