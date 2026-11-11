import time
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional

class LLMProviderInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str, evidence_package: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        pass

class MockLocalProvider(LLMProviderInterface):
    """Local offline deterministic provider for air-gapped environment."""
    def generate(self, prompt: str, evidence_package: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        query = evidence_package.get("query", "")
        concept = evidence_package.get("scientific_concept", "Scientific Concept")
        evidence = evidence_package.get("evidence", [])
        rel_type = evidence_package.get("relationship_type", "THEMATIC")
        
        top_verse = evidence[0]["text"] if evidence else "No verse retrieved"
        top_id = evidence[0]["source_id"] if evidence else "N/A"

        synthesis = (
            f"Analysis of query '{query}' against classical Tamil literature highlights the concept of '{concept}'. "
            f"The top evidence verse [{top_id}] states: '{top_verse}'. "
            f"The connection is classified as {rel_type}. "
            "Academic Principle: Semantic similarity between ancient poetic expressions and modern scientific concepts "
            "does NOT constitute historical scientific discovery or proof."
        )

        return {
            "text": synthesis,
            "citations": [top_id] if evidence else [],
            "model_name": "Qwen2.5-7B-Instruct-Local",
            "model_version": "2.5.0",
            "provider": "local_private",
            "inference_config": config or {"temperature": 0.2, "top_p": 0.95},
            "prompt_version": "v1.0",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "evidence_ids": [e.get("source_id") for e in evidence]
        }

class LLMGateway:
    """
    Production LLM Gateway managing configurable model providers.
    Ensures query and evidence stay within approved security boundary.
    """
    def __init__(self, provider_name: str = "local"):
        self.provider_name = provider_name
        self.providers: Dict[str, LLMProviderInterface] = {
            "local": MockLocalProvider(),
            "qwen": MockLocalProvider(),
        }

    def register_provider(self, name: str, provider: LLMProviderInterface):
        self.providers[name] = provider

    def generate_explanation(self, evidence_package: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        provider = self.providers.get(self.provider_name, MockLocalProvider())
        prompt = f"Synthesize academic evidence for query: {evidence_package.get('query')}"
        return provider.generate(prompt, evidence_package, config)
