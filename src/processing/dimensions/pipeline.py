from typing import Any, Dict

from processing.dimensions.one_d.processor import OneDProcessor
from processing.dimensions.two_d.processor import TwoDProcessor
from processing.dimensions.three_d.processor import ThreeDProcessor
from processing.dimensions.four_d.processor import FourDProcessor


class DimensionPipeline:
    """
    Runs the four interpretive analysis levels in sequence.

    These are levels of analysis, not physical dimensions.
    """

    def __init__(
        self,
        one_d=None,
        two_d=None,
        three_d=None,
        four_d=None,
    ):
        self.one_d = one_d or OneDProcessor()
        self.two_d = two_d or TwoDProcessor()
        self.three_d = three_d or ThreeDProcessor()
        self.four_d = four_d or FourDProcessor()

    def process(
        self,
        analysis_context: Dict[str, Any],
    ) -> Dict[str, Any]:

        results = {}

        one_d_result = self.one_d.process(
            analysis_context
        )
        results["1D"] = one_d_result

        context_2d = {
            **analysis_context,
            "dimension_results": results,
        }

        two_d_result = self.two_d.process(
            context_2d
        )
        results["2D"] = two_d_result

        context_3d = {
            **context_2d,
            "dimension_results": results,
        }

        three_d_result = self.three_d.process(
            context_3d
        )
        results["3D"] = three_d_result

        context_4d = {
            **context_3d,
            "dimension_results": results,
        }

        four_d_result = self.four_d.process(
            context_4d
        )
        results["4D"] = four_d_result

        return {
            "dimensions": results,
            "analysis_model": "interpretive_levels",
        }