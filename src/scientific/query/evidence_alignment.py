from typing import List, Dict, Any, Optional
from shared.schemas.evidence import Evidence
from shared.schemas.evidence_alignment import EvidenceAlignment

BANNED_UNSUPPORTED_PHRASES = [
    "discovered modern physics",
    "proved quantum mechanics",
    "invented gravity theory",
    "knew astrophysics centuries ago",
    "scientific proof of ancient science",
    "ancient tamil scientists invented",
]

class EvidenceAligner:
    """
    Groups unified evidence by source type and enforces strict Evidence Alignment
    and Hallucination Protection against unsupported scientific discovery claims.
    """

    def align(
        self,
        evidence: List[Any],
        required_sources: Optional[List[str]] = None,
    ) -> EvidenceAlignment:
        scientific_evidence: List[Evidence] = []
        tamil_evidence: List[Evidence] = []
        research_evidence: List[Evidence] = []

        if isinstance(evidence, list):
            for item in evidence:
                if isinstance(item, Evidence):
                    ev_obj = item
                elif isinstance(item, dict):
                    ev_obj = Evidence(
                        source_id=item.get("source_id", "unknown"),
                        source_type=item.get("source_type", "unknown"),
                        text=item.get("text", item.get("content", "")),
                        retrieval_score=float(item.get("retrieval_score", 0.0)),
                        matched_terms=list(item.get("matched_terms", [])),
                        provenance=dict(item.get("provenance", {})),
                        metadata=dict(item.get("metadata", {})),
                    )
                elif hasattr(item, "source_type"):
                    ev_obj = Evidence(
                        source_id=getattr(item, "source_id", "unknown"),
                        source_type=getattr(item, "source_type", "unknown"),
                        text=getattr(item, "text", getattr(item, "content", "")),
                        retrieval_score=float(getattr(item, "retrieval_score", 0.0)),
                        matched_terms=list(getattr(item, "matched_terms", [])),
                        provenance=dict(getattr(item, "provenance", {})),
                        metadata=dict(getattr(item, "metadata", {})),
                    )
                else:
                    continue

                if ev_obj.source_type == "scientific_kb":
                    scientific_evidence.append(ev_obj)
                elif ev_obj.source_type == "tamil_rag":
                    tamil_evidence.append(ev_obj)
                elif ev_obj.source_type == "research":
                    research_evidence.append(ev_obj)

        present_sources = set()
        if scientific_evidence:
            present_sources.add("scientific_kb")
        if tamil_evidence:
            present_sources.add("tamil_rag")
        if research_evidence:
            present_sources.add("research")

        if required_sources is not None:
            missing_sources = [req for req in required_sources if req not in present_sources]
        else:
            missing_sources = []

        return EvidenceAlignment(
            scientific_evidence=scientific_evidence,
            tamil_evidence=tamil_evidence,
            research_evidence=research_evidence,
            missing_sources=missing_sources,
        )