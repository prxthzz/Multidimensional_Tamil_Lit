from abc import ABC, abstractmethod
from typing import Any, Dict


class FinalLLMInterface(ABC):
    """
    Interface for final response synthesis.

    The Final LLM explains structured analysis results.
    It must not independently determine scientific-literary
    relationships or invent evidence.
    """

    @abstractmethod
    def synthesize(
        self,
        analysis_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        raise NotImplementedError