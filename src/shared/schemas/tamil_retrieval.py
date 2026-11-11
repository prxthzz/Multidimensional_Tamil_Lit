from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class TamilRetrievalRequest:
    query_terms: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    scientific_concepts: List[str] = field(default_factory=list)
    scientific_domains: List[str] = field(default_factory=list)
    context_terms: List[str] = field(default_factory=list)
    sources: List[str] = field(default_factory=lambda: ["Thirukkural", "Thiruvarutpa"])
    top_k: int = 5
    retrieval_reason: str = ""

@dataclass
class TamilRetrievalResult:
    source_id: str
    source_type: str
    text: str
    retrieval_score: float = 0.0
    semantic_score: float = 0.0
    keyword_score: float = 0.0
    theme_score: float = 0.0
    domain_score: float = 0.0
    metadata_score: float = 0.0
    hybrid_score: float = 0.0
    cross_encoder_score: Optional[float] = None
    final_score: float = 0.0
    matched_terms: List[str] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)
