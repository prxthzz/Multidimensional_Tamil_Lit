from typing import List, Dict, Any, Optional

class RelationshipAnalyzer:
    """
    Analyzes retrieved literary and scientific evidence to determine relationship category,
    evidence strength, retrieval relevance, and interpretation confidence.
    Enforces the central principle: SEMANTIC SIMILARITY != SCIENTIFIC PROOF.
    """

    def analyze(
        self,
        scientific_concepts: List[str],
        retrieved_results: List[Any],
    ) -> Dict[str, Any]:

        # Parse retrieved_results list
        processed_evidence = []
        has_tamil_or_synthetic = False
        top_retrieval_score = 0.0

        for item in retrieved_results:
            if isinstance(item, dict):
                ev = item
            elif hasattr(item, "__dict__"):
                ev = item.__dict__
            else:
                continue

            processed_evidence.append(ev)
            s_type = str(ev.get("source_type", "")).lower()
            if s_type in ["thirukkural", "thiruvarutpa", "sangam", "tamil_rag", "synthetic_test", "research"]:
                has_tamil_or_synthetic = True

            score = float(ev.get("retrieval_score", 0.0))
            if score > top_retrieval_score:
                top_retrieval_score = score

        if not processed_evidence or not has_tamil_or_synthetic:
            return {
                "relationship_type": "UNSUPPORTED",
                "evidence_strength": "NONE",
                "evidence_level": "NONE",
                "retrieval_relevance": top_retrieval_score,
                "relationship_confidence": 0.0,
                "interpretation_confidence": 0.0,
                "reason": "Insufficient evidence was found in classical Tamil sources to support a relationship.",
                "evidence": processed_evidence,
            }

        # Check explicit metadata overrides
        explicit_rel = None
        for ev in processed_evidence:
            meta = ev.get("metadata", {})
            if isinstance(meta, dict) and "relationship_type" in meta:
                explicit_rel = meta["relationship_type"]
                break

        if explicit_rel:
            rel_type = explicit_rel
        else:
            rel_type = "INTERPRETATION"

        # Separate scores logic (Part 12)
        if rel_type in ["DIRECT", "STRONG_ANALOGY"]:
            ev_strength = "HIGH"
            rel_conf = 0.85
        elif rel_type in ["INTERPRETATION", "THEMATIC"]:
            ev_strength = "MEDIUM"
            rel_conf = 0.50
        elif rel_type in ["METAPHORICAL", "ANALOGY", "HYPOTHESIS"]:
            ev_strength = "LOW"
            rel_conf = 0.40
        else:
            ev_strength = "NONE"
            rel_conf = 0.0

        reason_map = {
            "DIRECT": "Direct parallel identified between classical verse imagery and modern scientific concept.",
            "STRONG_ANALOGY": "Strong structural analogy between classical literature and scientific principles.",
            "THEMATIC": "Related by theme or idea, but not evidence of scientific equivalence.",
            "METAPHORICAL": "Poetic metaphor depicting natural phenomena.",
            "INTERPRETATION": "Interpretive thematic alignment based on semantic analysis.",
            "UNSUPPORTED": "Insufficient evidence was found to support the proposed connection.",
            "ANALOGY": "Analogous literary representation.",
            "HYPOTHESIS": "Hypothetical thematic correlation requiring further expert literary review.",
        }

        return {
            "relationship_type": rel_type,
            "evidence_strength": ev_strength,
            "evidence_level": ev_strength,
            "retrieval_relevance": top_retrieval_score,
            "relationship_confidence": rel_conf,
            "interpretation_confidence": rel_conf,
            "reason": reason_map.get(rel_type, "Thematic connection identified."),
            "evidence": processed_evidence,
        }
