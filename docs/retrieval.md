# Hybrid Retrieval Methodology

## Candidate Fusion Formula

The retrieval engine combines dense semantic representations with sparse lexical matching and metadata scores using transparent Candidate Fusion:

$$\text{Retrieval Relevance Score} = 0.40 \cdot S_{\text{semantic}} + 0.25 \cdot S_{\text{keyword}} + 0.15 \cdot S_{\text{theme}} + 0.10 \cdot S_{\text{domain}} + 0.10 \cdot S_{\text{metadata}}$$

Where:
- $S_{\text{semantic}}$: Cosine similarity of multilingual embeddings (`paraphrase-multilingual-MiniLM-L12-v2`) in $[0, 1]$.
- $S_{\text{keyword}}$: Lexical token match ratio across Tamil script, transliterations, and translations.
- $S_{\text{theme}}$: Chapter theme alignment ratio.
- $S_{\text{domain}}$: Domain compatibility (e.g. Environment $\leftrightarrow$ Vaan Chirappu).
- $S_{\text{metadata}}$: Source verification weight.

## Cross-Encoder Reranking
Candidates are reranked using `cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`. If model inference fails or runs offline, the system gracefully falls back to Candidate Fusion scores.
