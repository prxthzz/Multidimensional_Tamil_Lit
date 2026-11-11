from dataclasses import dataclass, field
from typing import List
from shared.schemas.query_intent import QueryIntent
from shared.schemas.input_understanding import InputUnderstanding

@dataclass
class QueryRoute:
    scientific: bool = True
    tamil: bool = False
    research: bool = False
    requested_dimensions: List[str] = field(default_factory=list)
    intent: str = "GENERAL"
    original_query: str = ""
    confidence: float = 1.0

@dataclass
class QueryHandlerResult:
    intent: QueryIntent
    understanding: InputUnderstanding
    route: QueryRoute
