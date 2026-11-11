from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class AnalysisResult:
    scientific_concepts: List[str] = field(default_factory=list)
    scientific_domains: List[str] = field(default_factory=list)
    dimensional_analysis: List[Dict[str, Any]] = field(default_factory=list)
    tamil_evidence: List[Dict[str, Any]] = field(default_factory=list)
    relationship_type: str = "THEMATIC"
    relationship_confidence: float = 0.5
    reasoning: str = ""
    uncertainty: bool = False
