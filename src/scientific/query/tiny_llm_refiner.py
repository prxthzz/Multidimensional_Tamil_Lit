from typing import Any, Dict

from shared.schemas.input_understanding import (
    InputUnderstanding,
)


class TinyLLMRefiner:
    """
    Adapts Tiny LLM semantic interpretation into the
    project's InputUnderstanding schema.

    The Tiny LLM is used only for query understanding.
    It does not determine scientific-literary relationships,
    generate hypotheses, or validate evidence.
    """

    def __init__(self, model):
        self.model = model

    def refine(
        self,
        scientific_query: Dict[str, Any],
        base_understanding: InputUnderstanding,
    ) -> InputUnderstanding:

        result = self.model.interpret(
            scientific_query
        )

        primary_concept = (
            result.get("primary_concept")
            or base_understanding.primary_concept
        )

        related_concepts = (
            result.get("relevant_concepts")
            or base_understanding.related_concepts
        )

        context_terms = (
            result.get("relevant_context")
            or base_understanding.context_terms
        )

        scientific_intent = (
            result.get("scientific_intent")
            or base_understanding.query_type
        )

        uncertainty = []

        if result.get("uncertainty", False):
            uncertainty.append(
                result.get(
                    "interpretation_notes",
                    "Tiny LLM indicated uncertainty.",
                )
            )

        return InputUnderstanding(
            original_query=(
                base_understanding.original_query
            ),
            primary_concept=primary_concept,
            scientific_domain=(
                base_understanding.scientific_domain
            ),
            query_type=scientific_intent,
            related_concepts=related_concepts,
            context_terms=context_terms,
            target_text=(
                base_understanding.target_text
            ),
            requires_tamil_retrieval=(
                base_understanding.requires_tamil_retrieval
            ),
            requires_research=(
                base_understanding.requires_research
            ),
            requested_dimensions=list(
                base_understanding.requested_dimensions
            ),
            uncertainty=uncertainty,
            source="tiny_llm",
        )