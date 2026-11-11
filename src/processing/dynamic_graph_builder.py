from typing import Dict, List, Any

class DynamicKnowledgeGraphBuilder:
    """
    Constructs a query-aware, dynamic Knowledge Graph generated directly from
    the CURRENT USER QUERY and CURRENT RETRIEVED RESULTS.
    """

    def build_graph(
        self,
        query_str: str,
        analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        nodes = []
        edges = []
        seen_node_ids = set()

        def add_node(node_id: str, label: str, node_type: str, color: str, metadata: dict = None):
            if node_id not in seen_node_ids:
                seen_node_ids.add(node_id)
                nodes.append({
                    "id": node_id,
                    "label": label,
                    "type": node_type,
                    "color": color,
                    "metadata": metadata or {}
                })

        def add_edge(source: str, target: str, relationship: str, weight: float = 1.0):
            edges.append({
                "source": source,
                "target": target,
                "relationship": relationship,
                "weight": weight
            })

        concepts = analysis_result.get("scientific_concepts", [query_str])
        domains = analysis_result.get("scientific_domains", ["General Science"])
        rel_type = analysis_result.get("relationship_type", "UNSUPPORTED")
        evidence_level = analysis_result.get("evidence_level", "NONE")
        retrieved_evidence = analysis_result.get("tamil_evidence", [])

        primary_concept = concepts[0] if concepts else query_str

        # 1. Primary Concept Node
        concept_node_id = f"concept_{primary_concept.lower().replace(' ', '_')}"
        add_node(concept_node_id, primary_concept, "SCIENTIFIC_CONCEPT", "#10B981", {
            "query": query_str,
            "concepts": concepts
        })

        # 2. Domain Nodes
        for dom in domains:
            dom_id = f"domain_{dom.lower().replace(' ', '_')}"
            add_node(dom_id, dom, "DOMAIN", "#3B82F6", {"domain_name": dom})
            add_edge(concept_node_id, dom_id, "BELONGS_TO")

        # 3. Handling Unsupported Queries
        if rel_type == "UNSUPPORTED" or not retrieved_evidence:
            no_rel_id = "no_relationship_node"
            add_node(no_rel_id, "No Sufficiently Supported Tamil Relationship", "RELATIONSHIP", "#EF4444", {
                "reason": "Retrieved passages did not provide enough evidence for a defensible comparison."
            })
            add_edge(concept_node_id, no_rel_id, "CLASSIFIED_AS")
            return {"nodes": nodes, "edges": edges, "is_unsupported": True}

        # 4. Relationship Node
        rel_node_id = f"rel_{rel_type.lower()}"
        add_node(rel_node_id, f"Relationship: {rel_type}", "RELATIONSHIP", "#F59E0B", {
            "relationship_type": rel_type,
            "evidence_level": evidence_level,
            "confidence": analysis_result.get("relationship_confidence", 0.5)
        })
        add_edge(concept_node_id, rel_node_id, "CLASSIFIED_AS")

        # 5. Evidence Level Node
        ev_level_id = f"ev_level_{evidence_level.lower()}"
        add_node(ev_level_id, f"Evidence: {evidence_level}", "EVIDENCE", "#8B5CF6", {
            "level": evidence_level
        })
        add_edge(rel_node_id, ev_level_id, "SUPPORTS")

        # 6. Verses, Chapters, and Sources Nodes
        for idx, ev in enumerate(retrieved_evidence):
            source_id = str(ev.get("source_id", f"verse_{idx+1}"))
            source_type = str(ev.get("source_type", "Tamil Verse"))
            text = str(ev.get("text", ""))
            meta = ev.get("metadata", {})
            if not isinstance(meta, dict):
                meta = {}

            chapter = str(meta.get("chapter", meta.get("chapter_number", "Chapter")))
            work = str(meta.get("work", source_type))

            # Source Node (e.g. Thirukkural)
            source_node_id = f"source_{work.lower().replace(' ', '_')}"
            add_node(source_node_id, work, "SOURCE", "#EC4899", {"work_name": work})

            # Chapter Node
            chapter_node_id = f"chapter_{chapter.lower().replace(' ', '_')}"
            add_node(chapter_node_id, f"Chapter: {chapter}", "CHAPTER", "#6366F1", {"chapter_name": chapter})
            add_edge(chapter_node_id, source_node_id, "FOUND_IN")

            # Verse Node (Crucial for result card synchronization!)
            verse_node_id = f"verse_{source_id}"
            add_node(verse_node_id, f"Verse #{source_id}", "VERSE", "#10B981", {
                "verse_id": source_id,
                "text": text,
                "translation": meta.get("translation", ""),
                "final_score": meta.get("final_score", ev.get("retrieval_score", 0.0)),
                "trace": ev.get("explanation_trace", {})
            })
            add_edge(chapter_node_id, verse_node_id, "HAS_VERSE")
            add_edge(verse_node_id, rel_node_id, "THEMATICALLY_RELATED", weight=float(ev.get("retrieval_score", 1.0)))

        return {"nodes": nodes, "edges": edges, "is_unsupported": False}
