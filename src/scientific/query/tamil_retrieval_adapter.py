from typing import List

from shared.schemas.evidence import Evidence
from shared.schemas.tamil_retrieval import TamilRetrievalRequest


class TamilRAGAdapter:
    """
    Adapts the existing Tamil RAG implementation to the
    project's unified Evidence representation.

    The underlying Tamil RAG implementation is not modified here.
    """

    def __init__(self, tamil_rag):
        self.tamil_rag = tamil_rag

    def retrieve(
        self,
        scientific_concepts: List[str],
        scientific_domains: List[str],
        context_terms: List[str],
        query_terms: List[str],
        top_k: int = 5,
    ) -> List[Evidence]:

        request = TamilRetrievalRequest(
            scientific_concepts=scientific_concepts,
            scientific_domains=scientific_domains,
            context_terms=context_terms,
            query_terms=query_terms,
        )

        results = self.tamil_rag.retrieve(request)

        evidence = []

        for result in results[:top_k]:
            evidence.append(
                Evidence(
                    source_id=result.source_id,
                    source_type="tamil_rag",
                    text=result.text,
                    retrieval_score=result.retrieval_score,
                    matched_terms=list(
                        result.matched_terms
                    ),
                    provenance={
                        "source_type": "tamil_rag",
                        **dict(result.metadata),
                    },
                    metadata=dict(result.metadata),
                )
            )

        return evidence