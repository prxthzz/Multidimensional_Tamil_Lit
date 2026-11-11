from dataclasses import dataclass, field
from typing import List

@dataclass
class QueryIntent:
    intent: str = "GENERAL"
    original_query: str = ""
    scientific_requested: bool = True
    tamil_requested: bool = False
    research_requested: bool = False
    dimensional_requested: bool = False
    requested_dimensions: List[str] = field(default_factory=list)
    translation_requested: bool = False
    comparison_requested: bool = False
    confidence: float = 0.8
