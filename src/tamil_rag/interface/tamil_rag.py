from shared.schemas.tamil_retrieval import (
    TamilRetrievalRequest,
    TamilRetrievalResult,
)

from tamil_rag.retrieval.semantic_retriever import SemanticTamilRetriever
from tamil_rag.reranking.reranker import TamilReranker


class TamilRAG:
    def __init__(
        self,
        retrieval_top_k: int = 10,
        final_top_k: int = 5,
    ):
        self.retriever = SemanticTamilRetriever(
            top_k=retrieval_top_k
        )

        self.reranker = TamilReranker(
            top_k=final_top_k
        )

    def _build_query(self, request: TamilRetrievalRequest) -> str:
        terms = (
            request.scientific_concepts
            + request.scientific_domains
            + request.context_terms
            + request.query_terms
        )

        return " ".join(
            term.strip()
            for term in terms
            if isinstance(term, str) and term.strip()
        )

    def retrieve(
        self,
        request: TamilRetrievalRequest,
    ) -> list[TamilRetrievalResult]:

        candidates = self.retriever.retrieve(request)

        if not candidates:
            return []

        query = self._build_query(request)

        return self.reranker.rerank(
            query,
            candidates,
        )