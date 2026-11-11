from scientific.query.handler import QueryHandler


def test_scientific_query_routes_to_scientific():

    handler = QueryHandler()

    result = handler.handle(
        "What is time dilation?"
    )

    assert result.intent == "SCIENTIFIC_CONCEPT"
    assert result.scientific is True
    assert result.tamil is False
    assert result.research is False


def test_literary_query_routes_to_tamil():

    handler = QueryHandler()

    result = handler.handle(
        "What does this Kural mean?"
    )

    assert result.intent == "LITERARY_MEANING"
    assert result.scientific is False
    assert result.tamil is True


def test_research_query_routes_to_research():

    handler = QueryHandler()

    result = handler.handle(
        "Find research papers about time dilation."
    )

    assert result.intent == "RESEARCH_SEARCH"
    assert result.research is True


def test_dimensional_query_routes_correctly():

    handler = QueryHandler()

    result = handler.handle(
        "Analyze this using 1D to 4D."
    )

    assert result.intent == "DIMENSIONAL_ANALYSIS"

    assert result.scientific is True
    assert result.tamil is True

    assert result.requested_dimensions == [
        "1D",
        "2D",
        "3D",
        "4D",
    ]


def test_comparison_routes_to_both_domains():

    handler = QueryHandler()

    result = handler.handle(
        "Compare this Kural with relativity."
    )

    assert result.intent == "CROSS_DOMAIN_COMPARISON"

    assert result.scientific is True
    assert result.tamil is True


def test_translation_routes_to_tamil():

    handler = QueryHandler()

    result = handler.handle(
        "Translate this Kural into English."
    )

    assert result.intent == "TRANSLATION"
    assert result.tamil is True
    assert result.scientific is False


def test_general_query_has_no_specialized_route():

    handler = QueryHandler()

    result = handler.handle(
        "Hello"
    )

    assert result.intent == "GENERAL_QUERY"

    assert result.scientific is False
    assert result.tamil is False
    assert result.research is False