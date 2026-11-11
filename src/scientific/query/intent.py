import re
from typing import List

from shared.schemas.query_intent import QueryIntent


class QueryIntentClassifier:
    """
    Conservative first-stage intent classifier.

    This classifier provides deterministic routing signals.
    The Tiny LLM can later refine ambiguous cases.
    """

    DIMENSIONS = {
        "1D",
        "2D",
        "3D",
        "4D",
    }

    def classify(
        self,
        query: str,
    ) -> QueryIntent:

        original_query = query.strip()

        normalized = re.sub(
            r"\s+",
            " ",
            original_query.lower(),
        )

        requested_dimensions: List[str] = []

        # Detect dimension ranges such as:
        # "1D to 4D"
        # "1d-4d"
        # "2D to 3D"
        dimension_range = re.search(
            r"\b([1-4])d\s*(?:to|-)\s*([1-4])d\b",
            normalized,
        )

        if dimension_range:
            start = int(dimension_range.group(1))
            end = int(dimension_range.group(2))

            if start <= end:
                requested_dimensions = [
                    f"{number}D"
                    for number in range(start, end + 1)
                ]

        else:
            # Detect individual dimensions:
            # "1D", "2D", "3D", "4D"
            for dimension in sorted(
                self.DIMENSIONS,
                key=lambda value: int(value[0]),
            ):
                if re.search(
                    rf"\b{dimension.lower()}\b",
                    normalized,
                ):
                    requested_dimensions.append(
                        dimension
                    )

        dimensional_requested = bool(
            requested_dimensions
        )

        translation_requested = any(
            term in normalized
            for term in (
                "translate",
                "translation",
                "meaning in english",
                "meaning in tamil",
            )
        )

        research_requested = any(
            term in normalized
            for term in (
                "research",
                "research paper",
                "research papers",
                "research study",
                "research studies",
                "paper",
                "papers",
                "study",
                "studies",
                "journal",
                "publication",
                "scientific literature",
            )
        )

        comparison_requested = any(
            term in normalized
            for term in (
                "compare",
                "comparison",
                "similar to",
                "related to",
                "relationship between",
                "connection between",
            )
        )

        scientific_validation = any(
            term in normalized
            for term in (
                "is this actually",
                "is this really",
                "scientifically valid",
                "scientifically true",
                "scientific evidence",
                "does science support",
            )
        )

        scientific_explanation = any(
            term in normalized
            for term in (
                "explain scientifically",
                "scientific explanation",
                "explain using physics",
                "physics explanation",
            )
        )

        literary_meaning = any(
            term in normalized
            for term in (
                "what does this kural mean",
                "what does this verse mean",
                "meaning of this kural",
                "meaning of this verse",
                "explain this kural",
                "explain this verse",
            )
        )

        tamil_literature_requested = any(
            term in normalized
            for term in (
                "tamil literature",
                "tamil literary",
                "classical tamil",
                "ancient tamil",
                "thirukkural",
                "thiruvarutpa",
            )
        )

        related_text = any(
            term in normalized
            for term in (
                "related kural",
                "related kurals",
                "similar kural",
                "similar kurals",
                "related verse",
                "related verses",
            )
        )

        if dimensional_requested:
            intent = "DIMENSIONAL_ANALYSIS"

        elif research_requested:
            intent = "RESEARCH_SEARCH"

        elif translation_requested:
            intent = "TRANSLATION"

        elif scientific_validation:
            intent = "SCIENTIFIC_VALIDATION"

        elif comparison_requested:
            intent = "CROSS_DOMAIN_COMPARISON"

        elif scientific_explanation:
            intent = "SCIENTIFIC_EXPLANATION"

        elif literary_meaning:
            intent = "LITERARY_MEANING"

        elif related_text:
            intent = "RELATED_TEXT"

        elif self._looks_like_scientific_concept(
            normalized
        ):
            intent = "SCIENTIFIC_CONCEPT"

        else:
            intent = "GENERAL_QUERY"

        scientific_requested = (
            intent
            in {
                "SCIENTIFIC_CONCEPT",
                "SCIENTIFIC_EXPLANATION",
                "SCIENTIFIC_VALIDATION",
                "CROSS_DOMAIN_COMPARISON",
                "DIMENSIONAL_ANALYSIS",
            }
        )

        tamil_requested = (
            intent
            in {
                "LITERARY_MEANING",
                "RELATED_TEXT",
                "TRANSLATION",
                "CROSS_DOMAIN_COMPARISON",
                "DIMENSIONAL_ANALYSIS",
            }
            or tamil_literature_requested
        )

        return QueryIntent(
            intent=intent,
            original_query=original_query,
            scientific_requested=scientific_requested,
            tamil_requested=tamil_requested,
            research_requested=research_requested,
            dimensional_requested=dimensional_requested,
            requested_dimensions=requested_dimensions,
            translation_requested=translation_requested,
            comparison_requested=comparison_requested,
            confidence=0.8,
        )

    @staticmethod
    def _looks_like_scientific_concept(
        normalized: str,
    ) -> bool:

        scientific_terms = (
            "what is",
            "define",
            "explain",
            "physics",
            "relativity",
            "quantum",
            "gravity",
            "spacetime",
            "time dilation",
            "electromagnetism",
            "energy",
            "wave",
            "particle",
        )

        return any(
            term in normalized
            for term in scientific_terms
        )