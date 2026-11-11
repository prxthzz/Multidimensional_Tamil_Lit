# Model Governance & LLM Security Policy

## 1. Pluggable Model Registry
Models are registered in the `model_registry` table with explicit versioning and provider type (`EMBEDDING`, `RERANKER`, `LLM`).

## 2. Default Approved Local Infrastructure
- **Embedding Model**: `paraphrase-multilingual-MiniLM-L12-v2`
- **Reranker Model**: `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`
- **LLM Provider**: `Qwen2.5-7B-Instruct-Local` / Private Local Gateway

## 3. Boundary Policy
No queries or retrieved verses leave the local environment unless external LLM providers are explicitly enabled by Super Admin configuration.
