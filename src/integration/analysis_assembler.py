from typing import Any, Dict, List

from shared.schemas.analysis_result import AnalysisResult

EPOCH_MAP = {
    "thirukkural": {
        "epoch": "Post-Sangam / Thirukkural Era (c. 31 BCE – 500 CE)",
        "lens": "Ethical Governance & Universal Order (Aram, Porul, Inbam)",
        "distance_to_proof": 25.0
    },
    "thiruvarutpa": {
        "epoch": "Modern Vallalar Era (19th Century CE)",
        "lens": "Universal Compassion, Light Cosmology & Spiritual Harmony",
        "distance_to_proof": 65.0
    },
    "sangam": {
        "epoch": "Classical Sangam Era (c. 300 BCE – 300 CE)",
        "lens": "Empirical Eco-Zone Observations (Ainthinai Natural Order)",
        "distance_to_proof": 20.0
    }
}

class AnalysisAssembler:
    """
    Combines scientific processing, dimensional analysis,
    Tamil retrieval evidence, and relationship analysis into
    the shared AnalysisResult contract.
    """

    def assemble_dimensions(
        self,
        query_obj: Any,
        wormhole: Dict[str, Any],
        aligned_evidence: List[Dict[str, Any]],
        relationship_analysis: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        concepts = getattr(query_obj, "concepts", [])
        raw_q = getattr(query_obj, "raw_query", "Query Concept")
        primary_concept = concepts[0] if concepts else raw_q
        rel_type = relationship_analysis.get("relationship_type", "THEMATIC")
        evidence_strength = relationship_analysis.get("evidence_strength", "MEDIUM")
        rel_conf = relationship_analysis.get("relationship_confidence", 0.5)
        retrieval_rel = relationship_analysis.get("retrieval_relevance", 0.0)

        top_ev = aligned_evidence[0] if aligned_evidence else {}
        top_verse_text = top_ev.get("text", "")
        top_verse_id = top_ev.get("source_id", "N/A")
        source_type = top_ev.get("source_type", "thirukkural").lower()
        matched_terms = top_ev.get("matched_terms", [])
        chapter_name = top_ev.get("metadata", {}).get("chapter", "Classical Chapter")

        # 4D Historical Epoch Lookup
        epoch_info = EPOCH_MAP.get(source_type, EPOCH_MAP["thirukkural"])
        epoch_title = epoch_info["epoch"]
        epoch_lens = epoch_info["lens"]
        proof_distance = epoch_info["distance_to_proof"] if rel_type != "DIRECT" else 15.0

        step1 = {
            "dimension_name": "1D — TEXT / LITERAL",
            "focus": f"Observable Tamil Text & Lexical Terms for '{primary_concept}'",
            "question": "What does the text literally contain?",
            "details": f"Original Tamil verse [{top_verse_id}] containing matched lexical terms: {', '.join(matched_terms) if matched_terms else 'semantic vector match'}.",
            "evidence": [{"text": top_verse_text, "source_id": top_verse_id}] if top_verse_text else []
        }

        step2 = {
            "dimension_name": "2D — CONTEXT / INTERPRETATION",
            "focus": "Chapter Context & Commentary Alignment",
            "question": "What does the text mean in context?",
            "details": f"Analyzes verse meaning within its classical chapter framework ({chapter_name} commentary).",
            "evidence": []
        }

        step3 = {
            "dimension_name": "3D — RELATIONSHIP / CONCEPT",
            "focus": f"{primary_concept} ↔ Classical Tamil Verse",
            "question": "How is the scientific concept related to the literary idea?",
            "details": f"Canonical Relationship: {rel_type} | Evidence Level: {evidence_strength} | Confidence: {int(rel_conf * 100)}% | Retrieval Relevance: {(retrieval_rel * 100):.1f}%.",
            "evidence": []
        }

        step4 = {
            "dimension_name": "4D — HISTORICAL & EPOCH TIMELINE",
            "focus": f"Temporal Evolution: {epoch_title}",
            "question": "How did this concept evolve across 2,000+ years of Tamil literary history?",
            "details": f"Epoch Lens: {epoch_lens}. Distance to Empirical Proof: {proof_distance:.0f}% (Academic Guardrail: Semantic similarity ≠ scientific proof).",
            "epoch_info": epoch_info,
            "evidence": []
        }

        return [step1, step2, step3, step4]

    def assemble(
        self,
        scientific_query: Dict[str, Any],
        wormhole_result: Dict[str, Any],
        tamil_results: List[Dict[str, Any]],
        relationship_result: Dict[str, Any],
    ) -> AnalysisResult:

        concept_mapping = wormhole_result.get("concept_mapping", {})
        context_mapping = wormhole_result.get("context_mapping", {})
        dimension_route = wormhole_result.get("dimension_route", {})

        return AnalysisResult(
            scientific_concepts=concept_mapping.get("all_concepts", []),
            scientific_domains=context_mapping.get("domains", []),
            dimensional_analysis=dimension_route.get("dimensional_analysis", []),
            tamil_evidence=tamil_results,
            relationship_type=relationship_result.get("relationship_type", "UNSUPPORTED"),
            relationship_confidence=relationship_result.get("relationship_confidence", 0.0),
            reasoning=relationship_result.get("reason", ""),
            uncertainty=(relationship_result.get("relationship_type", "UNSUPPORTED") != "FACT"),
        )