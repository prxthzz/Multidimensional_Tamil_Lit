# Evaluation & Benchmark Framework

## 1. Ground Truth Benchmark
The evaluation suite runs over `data/evaluation_benchmark.json` containing ground-truth query relevance pairs across 8 scientific domains.

## 2. Benchmark Metrics
- **Precision@5**: Percentage of top-5 retrieved verses that are relevant.
- **Recall@5**: Percentage of ground-truth relevant verses retrieved in top-5.
- **MRR (Mean Reciprocal Rank)**: Reciprocal rank of the first relevant verse.
- **nDCG@5 (Normalized Discounted Cumulative Gain)**: Graded relevance score.
- **Unsupported Claim Rate (%)**: Percentage of reasoning strings containing banned unsupported claims.
- **Mean Latency (ms)**: End-to-end execution time per query.

## 3. Ablation Comparison Modes
1. Lexical / BM25 Only
2. Semantic Vector Only
3. Hybrid Candidate Fusion
4. Full Pipeline (Hybrid + CrossEncoder Rerank)
