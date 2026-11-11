from typing import Any, Dict, List

from processing.dimensions.four_d.processor import FourDProcessor
from processing.dimensions.one_d.processor import OneDProcessor
from processing.dimensions.three_d.processor import ThreeDProcessor
from processing.dimensions.two_d.processor import TwoDProcessor


class DimensionRouter:
    """
    Routes evidence through the four levels of analysis.

    1D — Text / Literal
    2D — Interpretation / Context
    3D — Symbol / Concept
    4D — Future / Hypothetical

    These are analytical levels, not physical or mathematical
    dimensions.

    The router does not use scientific KB dimensional metadata.
    """

    def __init__(self):
        self.processors = {
            "1D": OneDProcessor(),
            "2D": TwoDProcessor(),
            "3D": ThreeDProcessor(),
            "4D": FourDProcessor(),
        }

    def route(
        self,
        scientific_query: Dict[str, Any],
        model_result: Dict[str, Any],
        tamil_evidence: List[Dict[str, Any]] | None = None,
        relationship_type: str = "UNSUPPORTED",
        hypothetical_request: bool = False,
    ) -> Dict[str, Any]:

        tamil_evidence = tamil_evidence or []

        scientific_concepts = scientific_query.get(
            "concepts",
            [],
        )

        scientific_domains = scientific_query.get(
            "domains",
            [],
        )

        context_terms = scientific_query.get(
            "context_terms",
            [],
        )

        analysis_context = {
            "query": scientific_query.get(
                "original_query",
                "",
            ),
            "scientific_concepts": scientific_concepts,
            "scientific_domains": scientific_domains,
            "context_terms": context_terms,
            "model_result": model_result,
            "tamil_evidence": tamil_evidence,
            "relationship_type": relationship_type,
            "hypothetical_request": hypothetical_request,
        }

        dimensional_analysis = []

        for dimension in (
            "1D",
            "2D",
            "3D",
            "4D",
        ):
            processor = self.processors[dimension]

            dimensional_analysis.append(
                processor.process(
                    analysis_context
                )
            )

        return {
            "status": "resolved",
            "dimensions": [
                "1D",
                "2D",
                "3D",
                "4D",
            ],
            "dimensional_analysis": dimensional_analysis,
            "dimension_count": 4,
            "analysis_model": (
                "interpretive_levels"
            ),
        }