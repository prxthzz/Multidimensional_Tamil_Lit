import json
import re
from pathlib import Path
from typing import List

from shared.schemas.evidence import Evidence


class ScientificKBRetriever:
    """
    Retrieves scientific evidence from the local scientific knowledge base.

    Retrieval only. This component does not determine relationships,
    hypotheses, or scientific-literary correspondence.
    """

    def __init__(
        self,
        knowledge_base_path="data/scientific/scientific_knowledge.json",
    ):
        self.knowledge_base_path = Path(knowledge_base_path)
        self.entries = self._load_knowledge_base()

    def _load_knowledge_base(self):
        with self.knowledge_base_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

        entries = []

        for domain in data.get("domains", []):
            for subdomain in domain.get("subdomains", []):
                for concept in subdomain.get("concepts", []):
                    entries.append(
                        {
                            **concept,
                            "domain": domain.get("name", ""),
                            "subdomain": subdomain.get("name", ""),
                        }
                    )

        return entries

    def retrieve(
        self,
        query_terms: List[str],
        top_k: int = 5,
    ) -> List[Evidence]:

        normalized_terms = [
            term.strip().lower()
            for term in query_terms
            if isinstance(term, str) and term.strip()
        ]

        if not normalized_terms:
            return []

        candidates = []

        for entry in self.entries:
            concept_name = str(entry.get("name", ""))
            definition = str(entry.get("definition", ""))

            keywords = entry.get("keywords", [])
            context_terms = entry.get("context_terms", [])

            searchable_text = " ".join(
                [
                    concept_name,
                    definition,
                    " ".join(str(k) for k in keywords),
                    " ".join(str(c) for c in context_terms),
                ]
            ).lower()

            matched_terms = []

            for term in normalized_terms:
                if re.search(
                    rf"\b{re.escape(term)}\b",
                    searchable_text,
                ):
                    matched_terms.append(term)

            if not matched_terms:
                continue

            unique_matches = list(set(matched_terms))

            score = len(unique_matches) / len(
                set(normalized_terms)
            )

            candidates.append(
                Evidence(
                    source_id=str(
                        entry.get(
                            "id",
                            concept_name or "unknown",
                        )
                    ),
                    source_type="scientific_kb",
                    text=definition,
                    retrieval_score=score,
                    matched_terms=unique_matches,
                    provenance={
                        "source": str(
                            self.knowledge_base_path
                        ),
                        "domain": entry.get(
                            "domain",
                            "",
                        ),
                        "subdomain": entry.get(
                            "subdomain",
                            "",
                        ),
                        "concept": concept_name,
                    },
                    metadata=entry,
                )
            )

        candidates.sort(
            key=lambda item: item.retrieval_score,
            reverse=True,
        )

        return candidates[:top_k]