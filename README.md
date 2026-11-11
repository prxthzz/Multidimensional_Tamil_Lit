# AI-Assisted Tamil Literary and Scientific Knowledge, Evidence and Research Platform

> **An Evidence-Aware Semantic Framework & Production Platform Mapping Modern Scientific Concepts to Classical Tamil Literature**

---

## Central Academic Principle

$$\text{SEMANTIC SIMILARITY} \neq \text{SCIENTIFIC PROOF}$$

This system does **NOT** claim that ancient Tamil authors discovered, predicted, or proved modern science. Instead, it provides an evidence-aware, academically defensible framework for exploring thematic, structural, and metaphorical parallels between modern scientific concepts and classical Tamil literature (*Thirukkural* and *Thiruvarutpa*).

---

## 3-Score Evaluation Architecture

The platform separates retrieval matching from evidence support and interpretation confidence:

1. **Retrieval Relevance (%)**: Surface vector + BM25 lexical query match.
2. **Evidence Strength (`HIGH`, `MEDIUM`, `LOW`, `NONE`)**: How strongly the source supports the proposed relationship.
3. **Interpretation Confidence (%)**: System confidence in the generated classification.

---

## Canonical Relationship Categories
- `DIRECT`
- `STRONG_ANALOGY`
- `THEMATIC`
- `METAPHORICAL`
- `UNSUPPORTED`

---

## System Features

- **Multilingual Support**: Accepts English (`Astrophysics`), Tamil (`விண்வெளி இயற்பியல்`), and Tanglish (`vinveli iyarpiyal`).
- **Expanded Scientific Ontology**: 54 curated concepts across 8 domains (Physics, Astronomy, Environment, Agriculture, Biology, Medicine, Computer Science, Psychology).
- **Authentic Tamil Corpus**: 1,900 indexed verses (1,330 Thirukkural + 570 Thiruvarutpa) with normalized text, translations, and copyright governance (`PUBLIC_DOMAIN`).
- **Real Okapi BM25 Hybrid Retrieval**: Combines BM25 lexical search, dense multilingual embeddings (`paraphrase-multilingual-MiniLM-L12-v2`), and CrossEncoder reranking (`mmarco-mMiniLMv2`).
- **LLM Gateway & Hallucination Guard**: Post-generation citation validation layer ensuring zero fabricated claims.
- **Human Expert Review Workflow**: Role-based approval pipeline (`DRAFT`, `PENDING_REVIEW`, `APPROVED`, `REJECTED`, `NEEDS_REVISION`). AI never overwrites human approved knowledge.
- **Production Database Architecture**: SQLAlchemy ORM supporting PostgreSQL (+ pgvector) and SQLite with 25+ production tables.
- **RBAC & Security**: JWT Authentication, PBKDF2 password hashing, and immutable Audit Logging.
- **Reproducible Evaluation & Ablation**: Benchmark evaluation suite calculating Precision@5, Recall@5, MRR, nDCG@5, and latency without hard-coded numbers.
- **Research Web Portal**: Full-featured React web application with 9 research, review, corpus, and audit tabs.

---

## Quick Start & Running Locally

### Prerequisites
- Python >= 3.11
- Node.js >= 18

### 1. Backend Setup & Database Seeding
```bash
# Install dependencies
pip install -e .

# Initialize and seed production database
python -m src.database.seed

# Run reproducible evaluation benchmark
python -c "import sys; sys.path.extend(['.', 'src']); import scripts.evaluate_system; scripts.evaluate_system.evaluate_ablation()"

# Start FastAPI server
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

### 2. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

---

## Documentation Quick Links

- [Architecture Specification](docs/ARCHITECTURE.md)
- [System Requirements (SRS)](docs/SRS.md)
- [REST API Reference](docs/API.md)
- [Database Schema](docs/DATABASE.md)
- [Security Policy](docs/SECURITY.md)
- [Deployment Guide](docs/DEPLOYMENT.md)
- [Operations Manual](docs/OPERATIONS.md)
- [Evaluation & Benchmark Suite](docs/EVALUATION.md)
- [Disaster Recovery](docs/DISASTER_RECOVERY.md)
- [User Manual](docs/USER_MANUAL.md)
- [Admin Manual](docs/ADMIN_MANUAL.md)
- [Changelog](docs/CHANGELOG.md)
