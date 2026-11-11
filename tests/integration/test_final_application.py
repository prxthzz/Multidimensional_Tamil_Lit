from integration.application import (
    ScientificApplication,
)


class FakeFinalSynthesizer:
    def synthesize(self, analysis_result):
        assert (
            analysis_result["scientific_concepts"]
        )

        assert (
            "relationship_type"
            in analysis_result
        )

        return {
            "response": (
                "Final grounded explanation."
            ),
            "source": "final_llm",
        }


def test_application_final_llm_wiring():
    application = ScientificApplication(
        final_synthesizer=FakeFinalSynthesizer()
    )

    result = application.analyze(
        "What is time dilation in Tamil literature?",
        synthesize=True,
    )

    assert "analysis" in result
    assert "final_response" in result

    assert (
        result["final_response"]["source"]
        == "final_llm"
    )