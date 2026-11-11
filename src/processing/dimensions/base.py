from abc import ABC, abstractmethod
from typing import Any, Dict


class DimensionProcessor(ABC):
    """
    Base interface for the four levels of knowledge analysis.

    The dimensions represent levels of interpretation, not
    mathematical or physical dimensions.

    1D — Text / Literal
    2D — Interpretation / Context
    3D — Symbol / Concept
    4D — Future / Hypothetical
    """

    dimension: str
    analysis_type: str

    @abstractmethod
    def process(
        self,
        analysis_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Process structured evidence at this level of analysis.
        """
        raise NotImplementedError