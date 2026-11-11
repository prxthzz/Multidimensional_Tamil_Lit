# Platform Changelog

## [1.0.0] - Production Upgrade

### Added
- **Production Database Architecture**: SQLAlchemy ORM with SQLite/PostgreSQL dynamic engines and 25+ production tables.
- **3-Score Output System**: Implemented `retrieval_relevance`, `evidence_strength`, and `interpretation_confidence`.
- **Real Okapi BM25 Retrieval**: Replaced token substring matching with `rank_bm25` Okapi BM25 lexical retriever.
- **LLM Gateway & Hallucination Guard**: Added pluggable local LLM Gateway and post-generation citation validation.
- **Human Expert Review Workflow**: Added review statuses (`APPROVED`, `REJECTED`, `NEEDS_REVISION`) and role overrides.
- **Reproducible Evaluation & Ablation Suite**: Automated ground-truth benchmark suite calculating `Precision@5`, `Recall@5`, `MRR`, `nDCG@5`, `Latency`, and ablation comparisons.
- **RBAC & Authentication**: JWT authentication with password hashing and audit logging.
- **Research Web Portal UI**: Upgraded React frontend with 9 dedicated research and management tabs.
