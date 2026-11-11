from typing import Any, Dict


class ModelRouter:
    """
    Selects the appropriate model-processing route for a
    structured scientific query.

    This component decides routing only. It does not execute
    model inference or determine scientific-literary relationships.
    """

    DEFAULT_MODEL = "Qwen/Qwen2.5-0.5B-Instruct"

    def route(
        self,
        scientific_query: Dict[str, Any],
        context_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        concepts = context_result.get("concepts", [])
        domains = context_result.get("domains", [])

        if concepts:
            return {
                "status": "resolved",
                "model": self.DEFAULT_MODEL,
                "model_type": "tiny_llm",
                "reason": "Scientific concepts were identified.",
                "domains": domains,
            }

        return {
            "status": "unresolved",
            "model": None,
            "model_type": None,
            "reason": "No scientific concepts were identified.",
            "domains": domains,
        }