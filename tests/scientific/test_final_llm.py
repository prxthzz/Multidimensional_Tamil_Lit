from scientific.final_llm.qwen_synthesizer import (
    QwenFinalSynthesizer,
)


class FakeModel:
    def interpret(self, data):
        assert "analysis_result" in data
        assert "final_prompt" in data

        return {
            "response": (
                "The structured analysis identifies "
                "an interpretation based on the supplied evidence."
            )
        }


def test_final_llm_synthesizer():
    synthesizer = QwenFinalSynthesizer(
        FakeModel()
    )

    result = synthesizer.synthesize(
        {
            "query": "What is time dilation?",
            "scientific_concepts": [
                "Time Dilation"
            ],
            "scientific_domains": [
                "Physics"
            ],
            "tamil_evidence": [],
            "relationship_type": "UNSUPPORTED",
            "relationship_confidence": 0.0,
            "reasoning": (
                "Insufficient evidence."
            ),
            "uncertainty": True,
        }
    )

    assert result["source"] == "final_llm"
    assert result["response"]