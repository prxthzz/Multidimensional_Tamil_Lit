# System Requirements Specification (SRS)

## Project Title
AI-Assisted Tamil Literary and Scientific Knowledge, Evidence and Research Platform

## 1. Functional Requirements (FR)
- **FR-01 (Multilingual Search)**: System shall support English, Tamil, and Tanglish queries.
- **FR-02 (Hybrid Retrieval)**: System shall combine Okapi BM25 lexical search with dense vector embeddings (`paraphrase-multilingual-MiniLM-L12-v2`).
- **FR-03 (3-Score Output)**: System shall expose `retrieval_relevance`, `evidence_strength`, and `interpretation_confidence` separately.
- **FR-04 (Evidence Guard)**: System shall sanitize LLM outputs to prevent unsupported historical claims.
- **FR-05 (Expert Review Workflow)**: System shall support review statuses (`DRAFT`, `PENDING_REVIEW`, `UNDER_REVIEW`, `APPROVED`, `REJECTED`, `NEEDS_REVISION`).
- **FR-06 (RBAC & Auth)**: System shall enforce RBAC for 9 roles (`SUPER_ADMIN`, `ADMIN`, `DOMAIN_EXPERT`, `LITERARY_EXPERT`, `REVIEWER`, `RESEARCHER`, `OPERATOR`, `AUDITOR`, `GENERAL_USER`).

## 2. Non-Functional Requirements (NFR)
- **NFR-01 (Performance)**: Mean query response time < 500 ms.
- **NFR-02 (Security)**: JWT authentication, password hashing (`pbkdf2_sha256`), audit logging.
- **NFR-03 (Auditability)**: Immutable log of search, review, and admin operations.
- **NFR-04 (Data Isolation)**: Support 100% offline deployment for sensitive enterprise environments.
