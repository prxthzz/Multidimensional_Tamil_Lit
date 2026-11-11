from typing import Any, Dict

from processing.dimensions.base import DimensionProcessor


class TwoDProcessor(DimensionProcessor):
    """
    2D — Interpretation / Context.

    Organizes semantic meaning and contextual information without
    asserting a scientific-literary correspondence.
    """

    dimension = "2D"
    analysis_type = "INTERPRETATION_CONTEXT"

    def process(
        self,
        analysis_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        tamil_evidence = analysis_context.get("tamil_evidence", [])
        scientific_concepts = analysis_context.get(
            "scientific_concepts",
            [],
        )
        context_terms = analysis_context.get(
            "context_terms",
            [],
        )

        has_evidence = bool(tamil_evidence)

        return {
            "dimension": self.dimension,
            "analysis_type": self.analysis_type,
            "status": "resolved" if has_evidence else "pending_evidence",
            "description": (
                "Semantic interpretation and contextual relationships "
                "derived from the available evidence."
            ),
            "scientific_concepts": scientific_concepts,
            "context_terms": context_terms,
            "interpretation_context": [
                {
                    "source_id": evidence.get("source_id", ""),
                    "text": evidence.get("text", ""),
                    "metadata": evidence.get("metadata", {}),
                }
                for evidence in tamil_evidence
            ],
            "properties": {
                "evidence_count": len(tamil_evidence),
                "context_term_count": len(context_terms),
                "scientific_concept_count": len(
                    scientific_concepts
                ),
                "contains_relationship_claim": False,
            },
        }