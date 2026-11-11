from scientific.query.retrieval import UnifiedRetriever
from shared.schemas.evidence import Evidence
from shared.schemas.retrieval import RetrievalRequest


def test_unified_scientific_retrieval():
    retriever = UnifiedRetriever()

    request = RetrievalRequest(
        query="What is time dilation?",
        scientific_concepts=[
            "Time Dilation",
        ],
        scientific_domains=[
            "Physics",
        ],
        context_terms=[
            "relativity",
            "clock",
        ],
    )

    results = retriever.retrieve(request)

    assert results
    assert results[0].source_type == "scientific_kb"
    assert results[0].source_id == "time_dilation"


def test_unified_retrieval_can_disable_scientific_source():
    retriever = UnifiedRetriever()

    request = RetrievalRequest(
        query="test",
        retrieve_scientific=False,
    )

    results = retriever.retrieve(request)

    assert results == []


class FakeTamilRetriever:
    def retrieve(
        self,
        scientific_concepts,
        scientific_domains,
        context_terms,
        query_terms,
        top_k,
    ):
        return [
            Evidence(
                source_id="tamil_test_001",
                source_type="tamil_rag",
                text="Synthetic Tamil evidence.",
                retrieval_score=0.8,
            )
        ]


def test_unified_retrieval_with_tamil_source():
    retriever = UnifiedRetriever(
        tamil_retriever=FakeTamilRetriever()
    )

    request = RetrievalRequest(
        query="Time dilation in Tamil literature",
        scientific_concepts=["Time Dilation"],
        scientific_domains=["Physics"],
        context_terms=["relativity"],
        retrieve_tamil=True,
    )

    results = retriever.retrieve(request)

    assert results

    source_types = {
        result.source_type
        for result in results
    }

    assert "scientific_kb" in source_types
    assert "tamil_rag" in source_types


def test_tamil_source_is_not_used_when_disabled():
    retriever = UnifiedRetriever(
        tamil_retriever=FakeTamilRetriever()
    )

    request = RetrievalRequest(
        query="Time dilation",
        scientific_concepts=["Time Dilation"],
        retrieve_tamil=False,
    )

    results = retriever.retrieve(request)

    assert all(
        result.source_type != "tamil_rag"
        for result in results
    )

class FakeResearchRetriever:
    def retrieve(
        self,
        query,
        scientific_concepts,
        context_terms,
        top_k,
    ):
        return [
            Evidence(
                source_id="research_test_001",
                source_type="research",
                text="Synthetic research evidence.",
                retrieval_score=0.9,
                provenance={
                    "synthetic": True,
                },
            )
        ]


def test_unified_retrieval_with_research_source():
    retriever = UnifiedRetriever(
        research_retriever=FakeResearchRetriever()
    )

    request = RetrievalRequest(
        query="Research time dilation",
        scientific_concepts=["Time Dilation"],
        context_terms=["relativity"],
        retrieve_research=True,
    )

    results = retriever.retrieve(request)

    assert results

    source_types = {
        result.source_type
        for result in results
    }

    assert "research" in source_types


def test_research_source_is_not_used_when_disabled():
    retriever = UnifiedRetriever(
        research_retriever=FakeResearchRetriever()
    )

    request = RetrievalRequest(
        query="Time dilation",
        scientific_concepts=["Time Dilation"],
        retrieve_research=False,
    )

    results = retriever.retrieve(request)

    assert all(
        result.source_type != "research"
        for result in results
    )