import logging
import math
from typing import List
from sentence_transformers import CrossEncoder

logger = logging.getLogger(__name__)

MODEL_NAME = "cross-encoder/mmarco-mMiniLMv2-L12-H384-v1"

# Configurable Reranking Combination Weight
RERANK_COMBINATION_WEIGHTS = {
    "hybrid_weight": 0.60,
    "cross_encoder_weight": 0.40
}


class TamilReranker:
    """
    Multilingual Cross-Encoder Reranker with transparent score combination.
    Preserves hybrid_score, sets cross_encoder_score, and calculates final_score.
    If unavailable, final_score = hybrid_score.
    """

    def __init__(self, top_k: int = 5):
        self.top_k = top_k
        self.model = None
        try:
            self.model = CrossEncoder(MODEL_NAME)
        except Exception as e:
            logger.warning(f"CrossEncoder failed to load: {e}. Preserving hybrid scores.")

    @staticmethod
    def _sigmoid(x: float) -> float:
        try:
            return 1.0 / (1.0 + math.exp(-x))
        except OverflowError:
            return 0.0 if x < 0 else 1.0

    def rerank(self, query: str, results: List):
        if not query.strip() or not results:
            return []

        if self.model is None:
            # Fallback: final_score = hybrid_score
            for result in results:
                result.cross_encoder_score = None
                result.final_score = getattr(result, "hybrid_score", getattr(result, "retrieval_score", 0.0))
                result.retrieval_score = result.final_score
                if hasattr(result, "metadata") and isinstance(result.metadata, dict):
                    result.metadata["cross_encoder_score"] = None
                    result.metadata["final_score"] = result.final_score

            results.sort(key=lambda r: getattr(r, "final_score", 0.0), reverse=True)
            return results[: self.top_k]

        try:
            pairs = [[query, result.text] for result in results]
            raw_scores = self.model.predict(pairs)

            ranked = []
            for result, raw_score in zip(results, raw_scores):
                ce_norm = self._sigmoid(float(raw_score))
                h_score = getattr(result, "hybrid_score", getattr(result, "retrieval_score", 0.0))

                # Transparent Combination Formula: 0.60 * Hybrid + 0.40 * CrossEncoder
                combined_final = (
                    RERANK_COMBINATION_WEIGHTS["hybrid_weight"] * h_score +
                    RERANK_COMBINATION_WEIGHTS["cross_encoder_weight"] * ce_norm
                )

                result.cross_encoder_score = round(ce_norm, 4)
                result.final_score = round(combined_final, 4)
                result.retrieval_score = round(combined_final, 4)

                if hasattr(result, "metadata") and isinstance(result.metadata, dict):
                    result.metadata["cross_encoder_raw"] = round(float(raw_score), 4)
                    result.metadata["cross_encoder_score"] = round(ce_norm, 4)
                    result.metadata["final_score"] = round(combined_final, 4)

                ranked.append(result)

            ranked.sort(key=lambda r: r.final_score, reverse=True)
            return ranked[: self.top_k]
        except Exception as e:
            logger.warning(f"Reranking prediction failed: {e}. Preserving hybrid scores.")
            for result in results:
                result.cross_encoder_score = None
                result.final_score = getattr(result, "hybrid_score", getattr(result, "retrieval_score", 0.0))
                result.retrieval_score = result.final_score
                if hasattr(result, "metadata") and isinstance(result.metadata, dict):
                    result.metadata["cross_encoder_score"] = None
                    result.metadata["final_score"] = result.final_score

            results.sort(key=lambda r: getattr(r, "final_score", 0.0), reverse=True)
            return results[: self.top_k]