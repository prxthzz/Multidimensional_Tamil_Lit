from abc import ABC, abstractmethod
from typing import Any, Dict


class TinyLLMInterface(ABC):
    """
    Interface for the Tiny/Small LLM used by the scientific branch.

    The model interprets structured scientific queries and returns
    structured semantic information.

    It does NOT determine whether a scientific-literary relationship
    is true or valid.
    """

    @abstractmethod
    def interpret(self, scientific_query: Dict[str, Any]) -> Dict[str, Any]:
        """
        Interpret a structured scientific query.

        Args:
            scientific_query:
                Structured output produced by the scientific query
                processing pipeline.

        Returns:
            Structured semantic interpretation.
        """
        raise NotImplementedError