from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class RetrievalRequest:
    query: str
    scientific_concepts: List[str] = field(default_factory=list)
    scientific_domains: List[str] = field(default_factory=list)
    context_terms: List[str] = field(default_factory=list)
    retrieve_scientific: bool = True
    retrieve_tamil: bool = True
    retrieve_research: bool = False
    top_k: int = 5
