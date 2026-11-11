from typing import Any, Dict


def build_final_prompt(
    analysis_result: Dict[str, Any],
) -> str:
    """
    Builds a strictly grounded prompt for the Final LLM.

    The Final LLM explains the structured analysis.
    It must never upgrade, invent, or strengthen a relationship.
    """

    return f"""
You are the final explanation layer of a scientific-literary
research system.

Your job is ONLY to explain the structured analysis supplied below.

CRITICAL GROUNDING RULES:

1. Do NOT add scientific facts that are not explicitly present
   in the structured analysis.

2. Do NOT claim that a Tamil text describes, contains, predicts,
   proves, or represents a scientific concept unless the
   structured analysis explicitly says so.

3. The retrieved Tamil evidence is retrieval evidence only.
   Retrieval similarity does NOT establish a scientific relationship.

4. NEVER infer a relationship from the Tamil text yourself.

5. NEVER upgrade:
   INTERPRETATION → FACT
   ANALOGY → FACT
   HYPOTHESIS → FACT

6. NEVER change the supplied relationship_type.

7. NEVER change the supplied relationship_confidence.

8. If relationship_type is INTERPRETATION, explicitly describe
   the result as an interpretation or possible conceptual reading.

9. If relationship_type is UNSUPPORTED, explicitly state that
   the available evidence does not establish a meaningful
   scientific-literary relationship.

10. If relationship_type is ANALOGY, clearly call it an analogy.

11. If relationship_type is HYPOTHESIS, clearly call it a hypothesis
    and preserve its speculative nature.

12. If the retrieved Tamil passages do not explicitly discuss the
    scientific concept, say that the passages were retrieved as
    potentially relevant evidence but do not themselves establish
    the scientific concept.

13. Do NOT infer meaning from the Tamil text beyond information
    explicitly supplied by the structured analysis.

14. Do NOT translate or interpret Tamil passages unless such an
    interpretation is explicitly supplied in the structured analysis.

15. Every claim about evidence must be traceable to the supplied
    source identifier.

16. Preserve uncertainty and limitations.

17. It is acceptable and preferred to say:
    "The available evidence is insufficient to establish this
    relationship."

STRUCTURED ANALYSIS
===================

Scientific Concepts:
{analysis_result.get("scientific_concepts", [])}

Scientific Domains:
{analysis_result.get("scientific_domains", [])}

Dimensional Analysis:
{analysis_result.get("dimensional_analysis", [])}

Tamil Evidence:
{analysis_result.get("tamil_evidence", [])}

Relationship Type:
{analysis_result.get("relationship_type", "UNSUPPORTED")}

Relationship Confidence:
{analysis_result.get("relationship_confidence", 0.0)}

Reasoning:
{analysis_result.get("reasoning", "")}

Uncertainty:
{analysis_result.get("uncertainty", True)}

REQUIRED RESPONSE FORMAT
========================

1. Scientific Concept
   State only the supplied scientific concept.

2. Retrieved Tamil Evidence
   State that these passages were retrieved as relevant evidence.
   Do NOT claim that they describe the scientific concept unless
   explicitly supported by the structured analysis.

3. Relationship Classification
   State the exact supplied relationship type and confidence.

4. Interpretation
   Explain only what the structured analysis permits.

5. Limitations
   Clearly state what cannot be concluded from the available evidence.

6. Sources
   List the supplied source identifiers.

FINAL RULE:

The structured analysis is authoritative.

If the structured analysis does not establish a scientific-literary
relationship, your response MUST NOT establish one.
"""