from scientific.query.input_understanding import (
    InputUnderstandingProcessor,
)
from scientific.query.intent import QueryIntentClassifier
from scientific.query.processor import ScientificQueryProcessor

from shared.schemas.query_handler import QueryRoute


class QueryHandler:

    def __init__(
        self,
        intent_classifier=None,
        input_understanding=None,
        scientific_processor=None,
        knowledge_base_path="data/scientific/scientific_knowledge.json",
    ):
        self.intent_classifier = (
            intent_classifier
            or QueryIntentClassifier()
        )

        self.input_understanding = (
            input_understanding
            or InputUnderstandingProcessor()
        )

        self.scientific_processor = (
            scientific_processor
            or ScientificQueryProcessor(
                knowledge_base_path
            )
        )

    def handle(self, query: str) -> QueryRoute:

        intent = self.intent_classifier.classify(
            query
        )

        return QueryRoute(
            scientific=intent.scientific_requested,
            tamil=intent.tamil_requested,
            research=intent.research_requested,
            requested_dimensions=list(
                intent.requested_dimensions
            ),
            intent=intent.intent,
            original_query=intent.original_query,
            confidence=intent.confidence,
        )

    def understand(self, query: str):

        route = self.handle(query)

        scientific_query = None

        if route.scientific:
            scientific_query = (
                self.scientific_processor.process(
                    query
                )
            )

        return self.input_understanding.understand(
            route,
            scientific_query,
        )