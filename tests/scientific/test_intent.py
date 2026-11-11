from scientific.query.intent import QueryIntentClassifier


def test_scientific_concept_intent():

    result = QueryIntentClassifier().classify(
        "What is time dilation?"
    )

    assert result.intent == "SCIENTIFIC_CONCEPT"
    assert result.scientific_requested is True
    assert result.tamil_requested is False


def test_literary_meaning_intent():

    result = QueryIntentClassifier().classify(
        "What does this Kural mean?"
    )

    assert result.intent == "LITERARY_MEANING"
    assert result.tamil_requested is True


def test_research_intent():

    result = QueryIntentClassifier().classify(
        "Find research papers about time dilation."
    )

    assert result.intent == "RESEARCH_SEARCH"
    assert result.research_requested is True


def test_dimensional_intent():

    result = QueryIntentClassifier().classify(
        "Analyze this using 1D to 4D."
    )

    assert result.intent == "DIMENSIONAL_ANALYSIS"
    assert result.dimensional_requested is True
    assert result.requested_dimensions == [
        "1D",
        "2D",
        "3D",
        "4D",
    ]


def test_comparison_intent():

    result = QueryIntentClassifier().classify(
        "Compare this Kural with relativity."
    )

    assert result.intent == "CROSS_DOMAIN_COMPARISON"
    assert result.comparison_requested is True


def test_translation_intent():

    result = QueryIntentClassifier().classify(
        "Translate this Kural."
    )

    assert result.intent == "TRANSLATION"
    assert result.translation_requested is True


def test_scientific_validation_intent():

    result = QueryIntentClassifier().classify(
        "Is this actually quantum physics?"
    )

    assert result.intent == "SCIENTIFIC_VALIDATION"
    assert result.scientific_requested is True