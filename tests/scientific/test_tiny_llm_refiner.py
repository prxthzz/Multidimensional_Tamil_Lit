from scientific.query.tiny_llm_refiner import (
    TinyLLMRefiner,
)

from shared.schemas.input_understanding import (
    InputUnderstanding,
)


class FakeTinyLLM:

    def interpret(self, scientific_query):

        return {
            "primary_concept": "Time Dilation",
            "scientific_intent": (
                "SCIENTIFIC_EXPLANATION"
            ),
            "relevant_concepts": [
                "Special Relativity",
                "Clock",
            ],
            "relevant_context": [
                "motion",
                "time",
                "clock",
            ],
            "interpretation_notes": (
                "The query appears to ask for "
                "an explanation of time dilation."
            ),
            "uncertainty": False,
        }


def test_tiny_llm_refinement():

    base = InputUnderstanding(
        original_query=(
            "Why do moving clocks appear slower?"
        ),
        primary_concept="",
        scientific_domain="Physics",
        query_type="SCIENTIFIC_CONCEPT",
        requires_tamil_retrieval=False,
        requires_research=False,
    )

    refiner = TinyLLMRefiner(
        FakeTinyLLM()
    )

    result = refiner.refine(
        {
            "original_query": (
                "Why do moving clocks appear slower?"
            )
        },
        base,
    )

    assert (
        result.primary_concept
        == "Time Dilation"
    )

    assert (
        result.query_type
        == "SCIENTIFIC_EXPLANATION"
    )

    assert (
        "Special Relativity"
        in result.related_concepts
    )

    assert (
        "motion"
        in result.context_terms
    )

    assert result.source == "tiny_llm"


def test_deterministic_values_are_preserved():

    base = InputUnderstanding(
        original_query="Research time dilation",
        primary_concept="Time Dilation",
        scientific_domain="Physics",
        query_type="RESEARCH_SEARCH",
        requires_tamil_retrieval=False,
        requires_research=True,
        requested_dimensions=["1D", "2D"],
    )

    class EmptyTinyLLM:

        def interpret(self, scientific_query):

            return {
                "primary_concept": None,
                "scientific_intent": "",
                "relevant_concepts": [],
                "relevant_context": [],
                "interpretation_notes": "",
                "uncertainty": False,
            }

    result = TinyLLMRefiner(
        EmptyTinyLLM()
    ).refine(
        {},
        base,
    )

    assert (
        result.primary_concept
        == "Time Dilation"
    )

    assert (
        result.query_type
        == "RESEARCH_SEARCH"
    )

    assert result.requires_research is True

    assert result.requested_dimensions == [
        "1D",
        "2D",
    ]