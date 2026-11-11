from typing import Any, Dict

from processing.dimensions.base import DimensionProcessor


class OneDProcessor(DimensionProcessor):
    """
    1D — Text / Literal.

    Captures directly observable textual information without
    creating scientific or literary interpretations.
    """

    dimension = "1D"
    analysis_type = "TEXT_LITERAL"

    def process(
        self,
        analysis_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        tamil_evidence = analysis_context.get("tamil_evidence", [])
        query = analysis_context.get("query", "")

        textual_items = []

        for evidence in tamil_evidence:
            text = evidence.get("text", "")
            if text:
                textual_items.append(
                    {
                        "source_id": evidence.get("source_id", ""),
                        "source_type": evidence.get("source_type", ""),
                        "text": text,
                        "metadata": evidence.get("metadata", {}),
                        "retrieval_score": evidence.get(
                            "retrieval_score",
                            0.0,
                        ),
                    }
                )

        return {
            "dimension": self.dimension,
            "analysis_type": self.analysis_type,
            "status": "resolved" if textual_items else "pending_evidence",
            "description": (
                "Directly observable textual information from the "
                "retrieved literary sources."
            ),
            "query": query,
            "textual_evidence": textual_items,
            "properties": {
                "evidence_count": len(textual_items),
                "contains_interpretation": False,
                "contains_relationship_claim": False,
            },
        }