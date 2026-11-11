from abc import ABC, abstractmethod
from typing import List

from shared.schemas.evidence import Evidence


class ResearchRetriever(ABC):
    """
    Contract for external research/web evidence retrieval.

    This interface does not generate or validate scientific claims.
    Implementations must return source-backed Evidence objects.
    """

    @abstractmethod
    def retrieve(
        self,
        query: str,
        scientific_concepts: List[str],
        context_terms: List[str],
        top_k: int = 5,
    ) -> List[Evidence]:
        raise NotImplementedError