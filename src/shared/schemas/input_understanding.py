from dataclasses import dataclass, field
from typing import List

@dataclass
class InputUnderstanding:
    query: str = ""
    original_query: str = ""
    primary_concept: str = ""
    concepts: List[str] = field(default_factory=list)
    related_concepts: List[str] = field(default_factory=list)
    scientific_domain: str = ""
    domains: List[str] = field(default_factory=list)
    context_terms: List[str] = field(default_factory=list)
    target_text: str = ""
    uncertainty: List[str] = field(default_factory=list)
    query_type: str = "SCIENTIFIC_EXPLANATION"
    source: str = "deterministic"
    requires_tamil_retrieval: bool = True
    requires_research: bool = False
    requested_dimensions: List[str] = field(default_factory=lambda: ["1D", "2D", "3D", "4D"])

    def __post_init__(self):
        if not self.query and self.original_query:
            self.query = self.original_query
        elif not self.original_query and self.query:
            self.original_query = self.query
