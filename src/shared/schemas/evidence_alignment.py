from dataclasses import dataclass, field
from typing import List
from shared.schemas.evidence import Evidence

@dataclass
class EvidenceAlignment:
    """
    Organizes retrieved evidence by source type.
    Preserves retrieval information, missing sources, and provenance.
    """
    scientific_evidence: List[Evidence] = field(default_factory=list)
    tamil_evidence: List[Evidence] = field(default_factory=list)
    research_evidence: List[Evidence] = field(default_factory=list)
    missing_sources: List[str] = field(default_factory=list)

    @property
    def evidence_count(self) -> int:
        return (
            len(self.scientific_evidence)
            + len(self.tamil_evidence)
            + len(self.research_evidence)
        )

    @property
    def sources_present(self) -> List[str]:
        sources = []
        if self.scientific_evidence:
            sources.append("scientific_kb")
        if self.tamil_evidence:
            sources.append("tamil_rag")
        if self.research_evidence:
            sources.append("research")
        return sources
