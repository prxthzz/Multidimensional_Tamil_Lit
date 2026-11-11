from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class RelationshipResult:
    relationship_type: str = "THEMATIC"
    evidence_strength: str = "MEDIUM"
    retrieval_relevance: float = 0.5
    relationship_confidence: float = 0.5
    reason: str = ""
    evidence: List[Dict[str, Any]] = field(default_factory=list)
