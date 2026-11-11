# Security Specification & Policy

## 1. Authentication & Authorization
- **Authentication**: JWT Bearer Tokens (`HS256`) with 8-hour expiration.
- **Password Hashing**: PBKDF2 with SHA-256 (`passlib`).
- **RBAC**: 9 explicit roles (`SUPER_ADMIN`, `ADMIN`, `DOMAIN_EXPERT`, `LITERARY_EXPERT`, `REVIEWER`, `RESEARCHER`, `OPERATOR`, `AUDITOR`, `GENERAL_USER`).

## 2. LLM Data Security & Boundary Protection
- System operates in 100% offline local/private mode by default.
- No protected queries or literary text leave the private server environment without explicit admin authorization.

## 3. Post-Generation Hallucination Guard
- Strict check enforcing valid citations.
- Banned claim sanitization prevents fabricated historical assertions.
