from typing import Any, Dict, List

from shared.schemas.tamil_retrieval import TamilRetrievalRequest


class ScientificToTamilBridge:
    """
    Converts scientific routing information into a shared
    TamilRetrievalRequest.

    This bridge prepares a retrieval request only.
    It does not retrieve Tamil literature and does not claim
    that any scientific concept corresponds to a Tamil text.
    """

    def build_request(
        self,
        scientific_query: Dict[str, Any],
        wormhole_result: Dict[str, Any],
    ) -> TamilRetrievalRequest:
        concept_mapping = wormhole_result.get(
            "concept_mapping",
            {},
        )

        context_mapping = wormhole_result.get(
            "context_mapping",
            {},
        )

        scientific_concepts = self._unique(
            concept_mapping.get("all_concepts", [])
        )

        scientific_domains = self._unique(
            context_mapping.get("domains", [])
        )

        context_terms = self._unique(
            context_mapping.get("context_terms", [])
        )

        query_terms = self._unique(
            scientific_concepts
            + context_terms
        )

        return TamilRetrievalRequest(
            scientific_concepts=scientific_concepts,
            scientific_domains=scientific_domains,
            context_terms=context_terms,
            query_terms=query_terms,
            retrieval_reason=(
                "Search Tamil literature for potentially relevant "
                "conceptual and contextual evidence."
            ),
        )

    @staticmethod
    def _unique(items: List[str]) -> List[str]:
        result = []
        seen = set()

        for item in items:
            if not isinstance(item, str):
                continue

            cleaned = item.strip()

            if not cleaned:
                continue

            key = cleaned.lower()

            if key not in seen:
                seen.add(key)
                result.append(cleaned)

        return result