from typing import Any, Dict

from scientific.tiny_llm.interface import TinyLLMInterface


class PlaceholderTinyLLM(TinyLLMInterface):
    """
    Temporary implementation used to validate the Tiny LLM contract.

    This is NOT the final language model.
    """

    def interpret(
        self,
        scientific_query: Dict[str, Any]
    ) -> Dict[str, Any]:

        concepts = scientific_query.get("concepts", [])
        context_terms = scientific_query.get("context_terms", [])

        primary_concept = concepts[0] if concepts else None

        return {
            "primary_concept": primary_concept,
            "scientific_intent": "scientific_concept_understanding",
            "relevant_concepts": concepts,
            "relevant_context": context_terms,
            "interpretation_notes": (
                "Placeholder interpretation. "
                "A Tiny/Small LLM will replace this implementation "
                "in the model integration stage."
            ),
            "uncertainty": not bool(concepts),
        }