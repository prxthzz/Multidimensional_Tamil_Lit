import json
from pathlib import Path
from typing import Dict, List


class ScientificConceptExpander:
    """
    Expands detected scientific concepts using relationships and
    contextual information already present in the scientific KB.

    This component does not generate new scientific knowledge.
    """

    def __init__(self, knowledge_base_path: str | Path):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.knowledge_base = self._load_knowledge_base()
        self.concepts = self._index_concepts()

    def _load_knowledge_base(self) -> dict:
        with self.knowledge_base_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def _index_concepts(self) -> Dict[str, dict]:
        """Create a lookup table using concept IDs and names."""
        index = {}

        for domain in self.knowledge_base.get("domains", []):
            for subdomain in domain.get("subdomains", []):
                for concept in subdomain.get("concepts", []):
                    concept_id = concept.get("id")
                    concept_name = concept.get("name")

                    if concept_id:
                        index[concept_id] = concept

                    if concept_name:
                        index[concept_name.lower()] = concept

        return index

    def _resolve_related_concept(self, concept_id: str):
        """Resolve a related concept ID from the KB."""
        return self.concepts.get(concept_id)

    def expand(self, concept_names: List[str]) -> List[dict]:
        """
        Expand detected concept names into structured scientific
        concept information.
        """

        expanded = []

        for concept_name in concept_names:
            concept = self.concepts.get(concept_name.lower())

            if not concept:
                continue

            related = []

            for related_id in concept.get("related_concepts", []):
                related_concept = self._resolve_related_concept(related_id)

                if related_concept:
                    related.append(
                        {
                            "id": related_concept.get("id"),
                            "name": related_concept.get("name"),
                        }
                    )

            expanded.append(
                {
                    "id": concept.get("id"),
                    "name": concept.get("name"),
                    "definition": concept.get("definition"),
                    "keywords": concept.get("keywords", []),
                    "context_terms": concept.get("context_terms", []),
                    "dimensions": concept.get("dimensions", {}),
                    "related_concepts": related,
                }
            )

        return expanded