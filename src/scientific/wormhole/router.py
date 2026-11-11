from typing import Any, Dict
from shared.schemas.scientific_query import ScientificQuery

from scientific.wormhole.concept_bridge import ConceptBridge
from scientific.wormhole.context_mapper import ContextMapper
from scientific.wormhole.model_router import ModelRouter


class WormholeRouter:
    """
    Coordinates the scientific Wormhole routing layer.

    The Wormhole is a computational architecture metaphor.
    It routes structured scientific information between processing
    stages without claiming any physical wormhole behavior.
    """

    def __init__(
        self,
        concept_bridge: ConceptBridge | None = None,
        context_mapper: ContextMapper | None = None,
        model_router: ModelRouter | None = None,
    ):
        self.concept_bridge = concept_bridge or ConceptBridge()
        self.context_mapper = context_mapper or ContextMapper()
        self.model_router = model_router or ModelRouter()

    def route(self, scientific_query: ScientificQuery) -> Dict[str, Any]:
        """
        Route a structured scientific query through the Wormhole layer.

        Returns a structured routing result for downstream processing.
        """


        query_data = scientific_query.__dict__

        concept_result = self.concept_bridge.map(query_data)

        context_result = self.context_mapper.map(
            query_data,
            concept_result,
        )

        model_result = self.model_router.route(
            query_data,
            context_result,
        )

       

        return {
            "input_query": query_data,
            "concept_mapping": concept_result,
            "context_mapping": context_result,
            "model_route": model_result,
        }