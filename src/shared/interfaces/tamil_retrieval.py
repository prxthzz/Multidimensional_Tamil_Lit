from abc import ABC, abstractmethod
from typing import List
from shared.schemas.tamil_retrieval import TamilRetrievalRequest, TamilRetrievalResult

class TamilRetrievalInterface(ABC):
    @abstractmethod
    def retrieve(self, request: TamilRetrievalRequest) -> List[TamilRetrievalResult]:
        pass
