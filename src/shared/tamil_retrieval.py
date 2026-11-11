from abc import ABC, abstractmethod

from shared.schemas.tamil_retrieval import (
    TamilRetrievalRequest,
    TamilRetrievalResult,
)


class TamilRetrievalInterface(ABC):
    """
    Shared interface between the scientific branch and the Tamil RAG.

    The scientific branch sends a TamilRetrievalRequest.
    The Tamil RAG implementation returns a TamilRetrievalResult.

    Retrieval output does not determine whether a scientific-literary
    relationship is valid. That belongs to later analysis stages.
    """

    @abstractmethod
    def retrieve(
        self,
        request: TamilRetrievalRequest,
    ) -> list[TamilRetrievalResult]:
        """
        Retrieve potentially relevant Tamil-literature candidates.
        """
        raise NotImplementedError