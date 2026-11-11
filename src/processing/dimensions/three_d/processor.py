from typing import Any, Dict

from processing.dimensions.base import DimensionProcessor


class ThreeDProcessor(DimensionProcessor):
    """
    3D — Symbol / Concept.

    Examines whether the available evidence supports a symbolic
    or conceptual relationship between scientific concepts and
    literary elements.

    This processor does not independently declare a relationship.
    Relationship classification belongs to the relationship analyzer.
    """

    dimension = "3D"
    analysis_type = "SYMBOL_CONCEPT"

    def process(
        self,
        analysis_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        tamil_evidence = analysis_context.get("tamil_evidence", [])
        scientific_concepts = analysis_context.get(
            "scientific_concepts",
            [],
        )

        evidence_available = bool(tamil_evidence)
        concepts_available = bool(scientific_concepts)

        eligible = evidence_available and concepts_available

        return {
            "dimension": self.dimension,
            "analysis_type": self.analysis_type,
            "status": (
                "eligible_for_relationship_analysis"
                if eligible
                else "insufficient_evidence"
            ),
            "description": (
                "Evidence-based symbolic or conceptual analysis. "
                "This layer does not itself establish a relationship."
            ),
            "scientific_concepts": scientific_concepts,
            "literary_elements": [
                {
                    "source_id": evidence.get("source_id", ""),
                    "text": evidence.get("text", ""),
                    "metadata": evidence.get("metadata", {}),
                }
                for evidence in tamil_evidence
            ],
            "relationship_claim": None,
            "properties": {
                "scientific_concept_count": len(
                    scientific_concepts
                ),
                "literary_evidence_count": len(
                    tamil_evidence
                ),
                "relationship_determined": False,
            },
        }