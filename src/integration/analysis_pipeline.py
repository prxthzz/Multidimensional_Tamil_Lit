from processing.dimensions.pipeline import DimensionPipeline
from processing.relationship.analyzer import RelationshipAnalyzer
from scientific.query.evidence_alignment import EvidenceAligner
from scientific.query.retrieval import UnifiedRetriever
from shared.schemas.analysis_result import AnalysisResult
from shared.schemas.retrieval import RetrievalRequest


class AnalysisPipeline:
    """
    Connects retrieval, evidence alignment, dimensional analysis,
    and relationship analysis into the shared AnalysisResult contract.

    Final LLM synthesis is intentionally outside this pipeline.
    """

    def __init__(
        self,
        retriever=None,
        aligner=None,
        dimension_pipeline=None,
        relationship_analyzer=None,
    ):
        self.retriever = retriever or UnifiedRetriever()
        self.aligner = aligner or EvidenceAligner()
        self.dimension_pipeline = (
            dimension_pipeline or DimensionPipeline()
        )
        self.relationship_analyzer = (
            relationship_analyzer
            or RelationshipAnalyzer()
        )

    def analyze(
        self,
        scientific_concepts,
        scientific_domains=None,
        context_terms=None,
        query="",
        retrieve_tamil=False,
        retrieve_research=False,
    ):

        scientific_domains = scientific_domains or []
        context_terms = context_terms or []

        request = RetrievalRequest(
            query=query,
            scientific_concepts=list(
                scientific_concepts
            ),
            scientific_domains=list(
                scientific_domains
            ),
            context_terms=list(
                context_terms
            ),
            retrieve_scientific=True,
            retrieve_tamil=retrieve_tamil,
            retrieve_research=retrieve_research,
        )

        evidence = self.retriever.retrieve(
            request
        )

        required_sources = [
            "scientific_kb"
        ]

        if retrieve_tamil:
            required_sources.append(
                "tamil_rag"
            )

        if retrieve_research:
            required_sources.append(
                "research"
            )

        alignment = self.aligner.align(
            evidence,
            required_sources=required_sources,
        )

        # Convert Evidence dataclasses into dictionaries
        # for the dimensional processors.
        dimension_context = {
            "query": query,
            "scientific_concepts": list(
                scientific_concepts
            ),
            "scientific_evidence": [
                {
                    "source_id": item.source_id,
                    "source_type": item.source_type,
                    "text": item.text,
                    "retrieval_score": (
                        item.retrieval_score
                    ),
                    "matched_terms": list(
                        item.matched_terms
                    ),
                    "provenance": dict(
                        item.provenance
                    ),
                    "metadata": dict(
                        item.metadata
                    ),
                }
                for item in alignment.scientific_evidence
            ],
            "tamil_evidence": [
                {
                    "source_id": item.source_id,
                    "source_type": item.source_type,
                    "text": item.text,
                    "retrieval_score": (
                        item.retrieval_score
                    ),
                    "matched_terms": list(
                        item.matched_terms
                    ),
                    "provenance": dict(
                        item.provenance
                    ),
                    "metadata": dict(
                        item.metadata
                    ),
                }
                for item in alignment.tamil_evidence
            ],
            "research_evidence": [
                {
                    "source_id": item.source_id,
                    "source_type": item.source_type,
                    "text": item.text,
                    "retrieval_score": (
                        item.retrieval_score
                    ),
                    "matched_terms": list(
                        item.matched_terms
                    ),
                    "provenance": dict(
                        item.provenance
                    ),
                    "metadata": dict(
                        item.metadata
                    ),
                }
                for item in alignment.research_evidence
            ],
        }

        dimension_result = (
            self.dimension_pipeline.process(
                dimension_context
            )
        )

        relationship = (
            self.relationship_analyzer.analyze(
                scientific_concepts=list(
                    scientific_concepts
                ),
                retrieved_results=[
                    {
                        "source_id": item.source_id,
                        "source_type": item.source_type,
                        "text": item.text,
                        "retrieval_score": (
                            item.retrieval_score
                        ),
                        "metadata": item.metadata,
                    }
                    for item in evidence
                ],
            )
        )

        dimensional_analysis = list(
            dimension_result[
                "dimensions"
            ].values()
        )

        tamil_evidence = [
            {
                "source_id": item.source_id,
                "source_type": item.source_type,
                "text": item.text,
                "retrieval_score": (
                    item.retrieval_score
                ),
                "matched_terms": list(
                    item.matched_terms
                ),
                "provenance": dict(
                    item.provenance
                ),
            }
            for item in alignment.tamil_evidence
        ]

        return AnalysisResult(
            scientific_concepts=list(
                scientific_concepts
            ),
            scientific_domains=list(
                scientific_domains
            ),
            dimensional_analysis=(
                dimensional_analysis
            ),
            tamil_evidence=tamil_evidence,
            relationship_type=relationship[
                "relationship_type"
            ],
            relationship_confidence=relationship[
                "relationship_confidence"
            ],
            reasoning=relationship[
                "reason"
            ],
            uncertainty=bool(
                alignment.missing_sources
                or relationship[
                    "relationship_type"
                ]
                in {
                    "UNSUPPORTED",
                    "INTERPRETATION",
                    "ANALOGY",
                    "HYPOTHESIS",
                }
            ),
        )