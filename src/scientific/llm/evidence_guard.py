import re
from typing import Dict, List, Any

BANNED_UNSUPPORTED_CLAIMS = [
    "discovered modern physics",
    "proved quantum mechanics",
    "invented gravity theory",
    "knew astrophysics centuries ago",
    "scientific proof of ancient science",
    "ancient tamil scientists invented",
]

class HallucinationGuard:
    """
    Post-Generation Validation Layer:
    1. Verifies that every cited verse and source ID exists in retrieved evidence.
    2. Strips or sanitizes fabricated quotations or ungrounded claims.
    3. Prevents unsupported claims from being presented as historical scientific facts.
    """

    def validate_and_sanitize(
        self,
        llm_output: Dict[str, Any],
        retrieved_evidence: List[Dict[str, Any]],
        relationship_type: str
    ) -> Dict[str, Any]:
        valid_source_ids = {item.get("source_id") for item in retrieved_evidence if item.get("source_id")}
        
        raw_text = llm_output.get("text", "")
        citations = llm_output.get("citations", [])

        # 1. Filter Citations
        valid_citations = [c for c in citations if c in valid_source_ids]

        # 2. Check Banned Unsupported Claims
        sanitized_text = raw_text
        has_unsupported_claim = False
        for banned in BANNED_UNSUPPORTED_CLAIMS:
            if banned.lower() in sanitized_text.lower():
                has_unsupported_claim = True
                pattern = re.compile(re.escape(banned), re.IGNORECASE)
                sanitized_text = pattern.sub("offered metaphorical literary reflections", sanitized_text)

        # 3. If relationship is UNSUPPORTED, enforce warning flag
        if relationship_type == "UNSUPPORTED":
            sanitized_text += " [SYSTEM NOTE: Insufficient evidence to establish a scientific or literary relationship.]"

        validated = dict(llm_output)
        validated["text"] = sanitized_text
        validated["citations"] = valid_citations
        validated["hallucination_detected"] = (len(valid_citations) < len(citations)) or has_unsupported_claim
        validated["guard_status"] = "PASSED_WITH_SANITIZATION" if validated["hallucination_detected"] else "PASSED"

        return validated
