from typing import List

from shared.interfaces.tamil_retrieval import TamilRetrievalInterface
from shared.schemas.tamil_retrieval import (
    TamilRetrievalRequest,
    TamilRetrievalResult,
)


class MockTamilRetrieval(TamilRetrievalInterface):
    """
    Synthetic Tamil retrieval implementation used only for
    integration testing.

    These records are NOT real Tamil-literature evidence.
    """

    def retrieve(
        self,
        request: TamilRetrievalRequest,
    ) -> List[TamilRetrievalResult]:
        results = []

        if request.query_terms:
            results.append(
                TamilRetrievalResult(
                    source_id="synthetic-001",
                    source_type="synthetic_test",
                    text="Synthetic Tamil retrieval record for integration testing.",
                    matched_terms=request.query_terms[:2],
                    retrieval_score=0.42,
                    metadata={
                        "purpose": "integration_test",
                    },
                )
            )

        if request.scientific_domains:
            results.append(
                TamilRetrievalResult(
                    source_id="synthetic-002",
                    source_type="synthetic_test",
                    text="Synthetic domain-context record for integration testing.",
                    matched_terms=request.scientific_domains[:2],
                    retrieval_score=0.31,
                    metadata={
                        "purpose": "integration_test",
                    },
                )
            )

        return results