from scientific.knowledge_base.retriever import (
    ScientificKBRetriever,
)


def test_scientific_kb_retrieval():
    retriever = ScientificKBRetriever()

    results = retriever.retrieve(
        ["Time Dilation"],
        top_k=5,
    )

    assert results
    assert results[0].source_type == "scientific_kb"
    assert results[0].text
    assert results[0].retrieval_score > 0
    assert "time dilation" in results[0].matched_terms


def test_unknown_term_returns_no_results():
    retriever = ScientificKBRetriever()

    results = retriever.retrieve(
        ["completely_unknown_scientific_concept_xyz"],
    )

    assert results == []


def test_top_k_is_respected():
    retriever = ScientificKBRetriever()

    results = retriever.retrieve(
        ["Physics"],
        top_k=2,
    )

    assert len(results) <= 2