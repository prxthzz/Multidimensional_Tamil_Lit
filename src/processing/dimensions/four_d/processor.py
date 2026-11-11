from typing import Any, Dict

from processing.dimensions.base import DimensionProcessor


class FourDProcessor(DimensionProcessor):
    """
    4D — Future / Hypothetical.

    Represents explicitly labelled analogy, speculation,
    hypothetical interpretation, or possible future extension.

    It never converts speculation into fact.
    """

    dimension = "4D"
    analysis_type = "FUTURE_HYPOTHETICAL"

    def process(
        self,
        analysis_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        hypothetical_request = analysis_context.get(
            "hypothetical_request",
            False,
        )

        existing_relationship = analysis_context.get(
            "relationship_type",
            "UNSUPPORTED",
        )

        allowed_relationships = {
            "ANALOGY",
            "HYPOTHESIS",
        }

        eligible = (
            hypothetical_request
            or existing_relationship in allowed_relationships
        )

        return {
            "dimension": self.dimension,
            "analysis_type": self.analysis_type,
            "status": (
                "eligible"
                if eligible
                else "not_activated"
            ),
            "description": (
                "Explicitly labelled hypothetical, speculative, "
                "analogical, or future-oriented interpretation."
            ),
            "hypothetical_request": hypothetical_request,
            "existing_relationship_type": existing_relationship,
            "allowed_relationship_types": sorted(
                allowed_relationships
            ),
            "hypothetical_interpretation": None,
            "properties": {
                "speculation_present": False,
                "hypothesis_generated": False,
                "scientific_fact_claim": False,
            },
        }