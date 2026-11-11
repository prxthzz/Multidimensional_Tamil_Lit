from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class ScientificQuery:
    original_query: str
    normalized_query: str
    concepts: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    domains: List[str] = field(default_factory=list)
    context_terms: List[str] = field(default_factory=list)
    expanded_concepts: List[str] = field(default_factory=list)
