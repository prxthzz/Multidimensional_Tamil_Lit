import json
import csv
import io
from typing import Dict, List, Any

class ExportService:
    @staticmethod
    def export_json(data: Any) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def export_csv(evidence_list: List[Dict[str, Any]]) -> str:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "Source ID", "Work", "Verse Text", "Relationship",
            "Retrieval Relevance", "Evidence Strength", "Interpretation Confidence", "Review Status"
        ])
        for item in evidence_list:
            writer.writerow([
                item.get("source_id", ""),
                item.get("source_type", ""),
                item.get("text", "").replace("\n", " "),
                item.get("relationship_type", ""),
                item.get("retrieval_relevance", item.get("retrieval_score", 0.0)),
                item.get("evidence_strength", "MEDIUM"),
                item.get("interpretation_confidence", item.get("confidence", 0.5)),
                item.get("review_status", "DRAFT")
            ])
        return output.getvalue()

    @staticmethod
    def export_summary_text(analysis: Dict[str, Any]) -> str:
        lines = [
            "=" * 65,
            " MULTIDIMENSIONAL TAMIL KNOWLEDGE RESEARCH PLATFORM ",
            " EVIDENCE-AWARE SEMANTIC RETRIEVAL REPORT ",
            "=" * 65,
            f"Query:                   {analysis.get('query')}",
            f"Normalized Concept:      {analysis.get('normalized_concept')}",
            f"Scientific Domains:      {', '.join(analysis.get('scientific_domains', []))}",
            f"Relationship Category:   {analysis.get('relationship_type')}",
            f"Evidence Strength:       {analysis.get('evidence_level', analysis.get('evidence_strength'))}",
            f"Retrieval Relevance:     {analysis.get('retrieval_relevance', 'N/A')}",
            f"Interpretation Conf.:    {analysis.get('relationship_confidence')}",
            "-" * 65,
            "RETRIEVED LITERARY EVIDENCE:",
        ]
        for idx, ev in enumerate(analysis.get("tamil_evidence", []), 1):
            lines.append(f"\n[{idx}] Source ID: {ev.get('source_id')} ({ev.get('source_type')})")
            lines.append(f"    Text: {ev.get('text')}")
            lines.append(f"    Relevance: {ev.get('retrieval_score')} | Semantic: {ev.get('semantic_score')}")
        lines.append("\nACADEMIC LIMITATIONS:")
        for lim in analysis.get("limitations", []):
            lines.append(f" - {lim}")
        lines.append("=" * 65)
        return "\n".join(lines)
