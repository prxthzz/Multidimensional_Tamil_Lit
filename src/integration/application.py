from dataclasses import asdict

from integration.analysis_pipeline import AnalysisPipeline
from scientific.final_llm.qwen_synthesizer import (
    QwenFinalSynthesizer,
)
from scientific.query.handler import QueryHandler
from scientific.query.retrieval import UnifiedRetriever
from scientific.query.tamil_retrieval_adapter import (
    TamilRAGAdapter,
)
from scientific.tiny_llm.qwen_model import QwenTinyLLM
from tamil_rag.interface.tamil_rag import TamilRAG


class ScientificApplication:
    """
    Complete application orchestration layer.

    Default behavior preserves the original AnalysisResult API.

    Optional final synthesis:

        application.analyze(
            query,
            synthesize=True,
        )

    Flow:

    Query
        ↓
    Input Understanding
        ↓
    Scientific + Tamil Retrieval
        ↓
    Evidence Alignment
        ↓
    1D → 4D
        ↓
    Relationship Analysis
        ↓
    AnalysisResult
        ↓
    Final LLM Synthesis (optional)
    """

    def __init__(
        self,
        query_handler=None,
        analysis_pipeline=None,
        final_synthesizer=None,
    ):
        self.query_handler = (
            query_handler
            or QueryHandler()
        )

        if analysis_pipeline is None:
            tamil_rag = TamilRAG(
                retrieval_top_k=10,
                final_top_k=5,
            )

            tamil_adapter = TamilRAGAdapter(
                tamil_rag
            )

            retriever = UnifiedRetriever(
                tamil_retriever=tamil_adapter
            )

            analysis_pipeline = AnalysisPipeline(
                retriever=retriever
            )

        self.analysis_pipeline = (
            analysis_pipeline
        )

        self.final_synthesizer = (
            final_synthesizer
        )

        self._qwen_model = None

    def _get_final_synthesizer(self):
        if self.final_synthesizer is None:
            if self._qwen_model is None:
                self._qwen_model = QwenTinyLLM()

            self.final_synthesizer = (
                QwenFinalSynthesizer(
                    self._qwen_model
                )
            )

        return self.final_synthesizer

    def analyze(
        self,
        query: str,
        synthesize=False,
    ):
        """
        Analyze a query.

        By default, returns AnalysisResult for backward
        compatibility.

        When synthesize=True, returns:

        {
            "analysis": AnalysisResult,
            "final_response": {...}
        }
        """

        understanding = (
            self.query_handler.understand(
                query
            )
        )

        scientific_concepts = []

        if understanding.primary_concept:
            scientific_concepts.append(
                understanding.primary_concept
            )

        scientific_concepts.extend(
            understanding.related_concepts
        )

        analysis_result = (
            self.analysis_pipeline.analyze(
                query=query,
                scientific_concepts=(
                    scientific_concepts
                ),
                scientific_domains=(
                    [
                        understanding.scientific_domain
                    ]
                    if understanding.scientific_domain
                    else []
                ),
                context_terms=(
                    understanding.context_terms
                ),
                retrieve_tamil=(
                    understanding.requires_tamil_retrieval
                ),
                retrieve_research=(
                    understanding.requires_research
                ),
            )
        )

        if not synthesize:
            return analysis_result

        structured_result = asdict(
            analysis_result
        )

        structured_result["query"] = query

        final_llm = (
            self._get_final_synthesizer()
        )

        final_response = (
            final_llm.synthesize(
                structured_result
            )
        )

        return {
            "analysis": analysis_result,
            "final_response": final_response,
        }