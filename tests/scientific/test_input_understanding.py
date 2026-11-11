from scientific.query.handler import QueryHandler


def test_time_dilation_understanding():

    handler = QueryHandler()

    route = handler.handle(
        "What is time dilation?"
    )

    understanding = handler.understand(
        "What is time dilation?")

    assert route.scientific is True

    assert (
        understanding.primary_concept
        == "Time Dilation"
    )

    assert (
        understanding.query_type
        == "SCIENTIFIC_EXPLANATION"
    )

    assert (
        understanding.source
        == "deterministic"
    )


def test_tamil_related_query():

    handler = QueryHandler()

    route = handler.handle(
        "Is there a Tamil literary idea related to time?"
    )

    understanding = handler.understand(
        "Is there a Tamil literary idea related to time?"
    )

    assert route.tamil is True

    assert (
        understanding.requires_tamil_retrieval
        is True
    )


def test_research_query():

    handler = QueryHandler()

    route = handler.handle(
        "Research scientific evidence for this concept"
    )

    understanding = handler.understand(
        "Research scientific evidence for this concept"
    )

    assert route.research is True

    assert (
        understanding.requires_research
        is True
    )


def test_dimensional_query():

    handler = QueryHandler()

    route = handler.handle(
        "Analyze this concept from 1D to 4D"
    )

    understanding = handler.understand(
        "Analyze this concept from 1D to 4D"
    )

    assert understanding.requested_dimensions == [
        "1D",
        "2D",
        "3D",
        "4D",
    ]