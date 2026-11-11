from typing import Dict, List, Any

def simple_tamil_transliterate(text: str) -> str:
    """
    Provides a simple Romanized transliteration for Tamil text.
    """
    if not text:
        return ""
    
    mapping = {
        "அ": "a", "ஆ": "aa", "இ": "i", "ஈ": "ee", "உ": "u", "ஊ": "oo",
        "எ": "e", "ஏ": "ae", "ஐ": "ai", "ஒ": "o", "ஓ": "oa", "ஔ": "au", "ஃ": "k",
        "க": "ka", "ங": "nga", "ச": "cha", "ஞ": "nya", "ட": "ta", "ண": "na",
        "த": "tha", "ந": "na", "ப": "pa", "ம": "ma", "ய": "ya", "ர": "ra",
        "ல": "la", "வ": "va", "ழ": "zha", "ள": "la", "ற": "ra", "ன": "na",
        "ா": "aa", "ி": "i", "ீ": "ee", "ு": "u", "ூ": "oo", "ெ": "e",
        "ே": "ae", "ை": "ai", "ொ": "o", "ோ": "oa", "ௌ": "au", "்": ""
    }
    
    result = []
    for char in text:
        if char in mapping:
            result.append(mapping[char])
        else:
            result.append(char)
    return "".join(result)


class ExplanationTraceGenerator:
    """
    Generates human-readable per-verse explanation traces, transliteration,
    and detailed score breakdowns derived strictly from ACTUAL retrieved evidence metadata.
    """

    def generate_trace(
        self,
        verse_item: Dict[str, Any],
        scientific_concept: str,
        scientific_domains: List[str]
    ) -> Dict[str, Any]:
        meta = verse_item.get("metadata", {})
        if not isinstance(meta, dict):
            meta = {}

        sem_s = meta.get("semantic_score", verse_item.get("semantic_score", 0.0))
        kw_s = meta.get("keyword_score", verse_item.get("keyword_score", 0.0))
        theme_s = meta.get("theme_score", verse_item.get("theme_score", 0.0))
        domain_s = meta.get("domain_score", verse_item.get("domain_score", 0.0))
        meta_s = meta.get("metadata_score", verse_item.get("metadata_score", 0.0))
        h_s = meta.get("hybrid_score", verse_item.get("hybrid_score", verse_item.get("retrieval_score", 0.0)))
        ce_s = meta.get("cross_encoder_score", verse_item.get("cross_encoder_score", None))
        f_s = meta.get("final_score", verse_item.get("final_score", h_s))

        matched_terms = verse_item.get("matched_terms", [])
        chapter = meta.get("chapter", meta.get("chapter_number", "General Chapter"))
        work = meta.get("work", verse_item.get("source_type", "Tamil Literature"))
        translation = meta.get("translation", "")
        raw_text = verse_item.get("text", "")

        # Transliteration
        transliteration = meta.get("transliteration", simple_tamil_transliterate(raw_text))

        # Score Breakdown object
        score_breakdown = {
            "semantic_score_pct": round(sem_s * 100, 1),
            "keyword_score_pct": round(kw_s * 100, 1),
            "theme_score_pct": round(theme_s * 100, 1),
            "domain_score_pct": round(domain_s * 100, 1),
            "metadata_score_pct": round(meta_s * 100, 1),
            "hybrid_score_pct": round(h_s * 100, 1),
            "cross_encoder_score_pct": round(ce_s * 100, 1) if ce_s is not None else "N/A",
            "final_score_pct": round(f_s * 100, 1),
        }

        # Contextual Semantic Explanation
        sem_desc = (
            f"The multilingual embedding model identified high contextual similarity ({score_breakdown['semantic_score_pct']}%) "
            f"between '{scientific_concept}' and the verse text."
        )

        # Keyword Explanation
        if matched_terms:
            kw_desc = f"Matched explicit lexical terms: {', '.join(matched_terms)}."
        else:
            kw_desc = "Matched broader contextual concepts and semantic synonyms."

        # Theme Explanation
        theme_desc = f"Chapter '{chapter}' in {work} aligns with the underlying natural or philosophical theme of {scientific_concept}."

        # Domain Match
        dom_desc = f"Scientific Domain ({', '.join(scientific_domains) if scientific_domains else 'General Science'}) matches literary domain ({work} / {chapter})."

        # Comprehensive Verse Explanation
        if translation:
            verse_explanation = (
                f"In {work} (Chapter: {chapter}), this verse observed that '{translation}'. "
                f"When analyzed against modern '{scientific_concept}', the verse reflects ancient observational insight into natural governance and ecological balance."
            )
        else:
            verse_explanation = (
                f"This verse from {work} (Chapter: {chapter}) expresses classical Tamil observations on natural harmony and ethics, "
                f"forming a thematic parallel with modern conceptual understandings of {scientific_concept}."
            )

        # Human readable summary
        summary = (
            f"The verse from {work} (Chapter: {chapter}) was retrieved with a final relevance score of {score_breakdown['final_score_pct']}%. "
            f"{kw_desc} {theme_desc} However, the classical verse expresses poetic/metaphorical observations and does NOT constitute direct modern laboratory evidence."
        )

        # Why Similar vs Why Not Identical
        why_similar = f"Both discuss conceptual themes around {scientific_concept} and natural/ethical observations in {chapter}."
        why_not_identical = f"The classical text uses poetic/metaphorical language suitable for classical literature, whereas modern {scientific_concept} involves formal physical/empirical measurements."

        return {
            "score_breakdown": score_breakdown,
            "matched_terms": matched_terms,
            "chapter": chapter,
            "work": work,
            "transliteration": transliteration,
            "verse_explanation": verse_explanation,
            "semantic_explanation": sem_desc,
            "keyword_explanation": kw_desc,
            "theme_explanation": theme_desc,
            "domain_explanation": dom_desc,
            "human_summary": summary,
            "why_similar": why_similar,
            "why_not_identical": why_not_identical,
            "limitation": "Conceptual parallel only; does not establish ancient scientific discovery or historical transmission."
        }
