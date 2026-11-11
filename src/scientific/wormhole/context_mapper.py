from typing import Any, Dict, List


class ContextMapper:
    """
    Maps scientific concepts to their available scientific context.

    This component only organizes context already supplied by the
    scientific query-processing stage. It does not generate new
    scientific knowledge or establish Tamil-literary relationships.
    """

    def map(
        self,
        scientific_query: Dict[str, Any],
        concept_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        domains = self._unique(
            scientific_query.get("domains", [])
        )

        context_terms = self._unique(
            scientific_query.get("context_terms", [])
        )

        expanded_context = self._extract_expanded_context(
            scientific_query.get("expanded_concepts", [])
        )

        all_context_terms = self._unique(
            context_terms + expanded_context
        )

        return {
            "domains": domains,
            "context_terms": all_context_terms,
            "concepts": concept_result.get(
                "all_concepts",
                [],
            ),
        }

    @staticmethod
    def _extract_expanded_context(
        expanded_concepts: List[Dict[str, Any]],
    ) -> List[str]:
        context_terms = []

        for concept in expanded_concepts:
            for term in concept.get("context_terms", []):
                if isinstance(term, str) and term.strip():
                    context_terms.append(term.strip())

        return context_terms

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