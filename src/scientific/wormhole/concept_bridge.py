from typing import Any, Dict, List


class ConceptBridge:
    """
    Converts structured scientific concepts into a normalized
    representation for Wormhole routing.

    This component does not create or claim relationships with
    Tamil literature. It only prepares scientific concepts for
    downstream processing.
    """

    def map(self, scientific_query: Dict[str, Any]) -> Dict[str, Any]:
        primary_concepts = self._unique(
            scientific_query.get("concepts", [])
        )

        expanded_concepts = self._extract_expanded_names(
            scientific_query.get("expanded_concepts", [])
        )

        # Keep only concepts that are additional to the primary concepts.
        primary_keys = {
            concept.lower()
            for concept in primary_concepts
        }

        expanded_concepts = [
            concept
            for concept in expanded_concepts
            if concept.lower() not in primary_keys
        ]

        all_concepts = self._unique(
            primary_concepts + expanded_concepts
        )

        return {
            "primary_concepts": primary_concepts,
            "expanded_concepts": expanded_concepts,
            "all_concepts": all_concepts,
            "concept_count": len(all_concepts),
        }

    @staticmethod
    def _extract_expanded_names(
        expanded_concepts: List[Dict[str, Any]],
    ) -> List[str]:
        names = []

        for concept in expanded_concepts:
            name = concept.get("name")

            if isinstance(name, str) and name.strip():
                names.append(name.strip())

            for related in concept.get("related_concepts", []):
                related_name = related.get("name")

                if (
                    isinstance(related_name, str)
                    and related_name.strip()
                ):
                    names.append(related_name.strip())

        return names

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