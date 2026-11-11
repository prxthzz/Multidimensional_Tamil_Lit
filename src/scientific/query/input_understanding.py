from shared.schemas.input_understanding import (
    InputUnderstanding,
)


class InputUnderstandingProcessor:

    def understand(
        self,
        query_route,
        scientific_query=None,
    ) -> InputUnderstanding:

        primary_concept = ""

        related_concepts = []

        scientific_domain = ""

        context_terms = []

        if scientific_query is not None:

            concepts = list(
                scientific_query.concepts
            )

            if concepts:
                primary_concept = concepts[0]

            related_concepts = list(
                concepts[1:]
            )

            domains = list(
                scientific_query.domains
            )

            if domains:
                scientific_domain = domains[0]

            context_terms = list(
                scientific_query.context_terms
            )

        query_type = query_route.intent

        if (
            query_route.intent == "SCIENTIFIC_CONCEPT"
            and primary_concept
        ):
            query_type = "SCIENTIFIC_EXPLANATION"

        return InputUnderstanding(
            original_query=query_route.original_query,
            primary_concept=primary_concept,
            scientific_domain=scientific_domain,
            query_type=query_type,
            related_concepts=related_concepts,
            context_terms=context_terms,
            requires_tamil_retrieval=query_route.tamil,
            requires_research=query_route.research,
            requested_dimensions=list(
                query_route.requested_dimensions
            ),
            source="deterministic",
        )