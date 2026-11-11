from typing import Any, Dict


class FinalLLMParser:
    """
    Parses the Final LLM response into a predictable structure.
    """

    def parse(
        self,
        response: str,
    ) -> Dict[str, Any]:

        return {
            "response": response.strip(),
            "source": "final_llm",
        }