import re
from typing import Any, Dict, List


class TinyLLMOutputParser:
    """
    Converts Tiny LLM textual output into the structured interpretation
    expected by the scientific branch.

    The parser does not invent missing information.
    """

    REQUIRED_FIELDS = (
        "primary_concept",
        "scientific_intent",
        "relevant_concepts",
        "relevant_context",
        "interpretation_notes",
        "uncertainty",
    )

    def _extract_field(self, response: str, field_name: str) -> str:
        """
        Extract a field from numbered or unnumbered model output.

        Example:
            1. primary_concept: Time Dilation
        """

        pattern = (
            rf"(?:^|\n)\s*"
            rf"(?:\d+\.\s*)?"
            rf"{re.escape(field_name)}\s*:\s*"
            rf"(.*?)(?=\n\s*(?:\d+\.\s*)?[a-z_]+\s*:|\Z)"
        )

        match = re.search(
            pattern,
            response,
            flags=re.IGNORECASE | re.DOTALL,
        )

        if not match:
            return ""

        return match.group(1).strip()

    def _parse_list(self, value: str) -> List[str]:
        """Convert comma-separated model output into a unique list."""

        if not value:
            return []

        items = []

        for item in value.split(","):
            cleaned = item.strip()

            if cleaned and cleaned not in items:
                items.append(cleaned)

        return items

    def _parse_uncertainty(self, value: str) -> bool:
        """
        Convert the model's uncertainty field into a boolean.

        Natural-language uncertainty statements are treated as True.
        """

        if not value:
            return True

        normalized = value.strip().lower()

        if normalized in {"true", "yes", "uncertain"}:
            return True

        if normalized in {"false", "no", "certain"}:
            return False

        uncertainty_terms = (
            "ambigu",
            "uncertain",
            "uncertainty",
            "not clear",
            "unclear",
            "may refer",
            "could refer",
            "possibly",
        )

        return any(
            term in normalized
            for term in uncertainty_terms
        )

    def parse(self, response: str) -> Dict[str, Any]:
        """
        Parse and validate a Tiny LLM response.
        """

        if not response or not response.strip():
            raise ValueError("Tiny LLM returned an empty response.")

        primary_concept = self._extract_field(
            response,
            "primary_concept",
        )

        scientific_intent = self._extract_field(
            response,
            "scientific_intent",
        )

        relevant_concepts_raw = self._extract_field(
            response,
            "relevant_concepts",
        )

        relevant_context_raw = self._extract_field(
            response,
            "relevant_context",
        )

        interpretation_notes = self._extract_field(
            response,
            "interpretation_notes",
        )

        uncertainty_raw = self._extract_field(
            response,
            "uncertainty",
        )

        result = {
            "primary_concept": (
                primary_concept
                if primary_concept
                else None
            ),
            "scientific_intent": scientific_intent,
            "relevant_concepts": self._parse_list(
                relevant_concepts_raw
            ),
            "relevant_context": self._parse_list(
                relevant_context_raw
            ),
            "interpretation_notes": interpretation_notes,
            "uncertainty": self._parse_uncertainty(
                uncertainty_raw
            ),
        }

        self.validate(result)

        return result

    def validate(self, result: Dict[str, Any]) -> None:
        """
        Validate the structured Tiny LLM output.

        Raises:
            ValueError: if required fields are missing or malformed.
        """

        missing_fields = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in result
        ]

        if missing_fields:
            raise ValueError(
                "Missing Tiny LLM output fields: "
                + ", ".join(missing_fields)
            )

        if result["primary_concept"] is not None and not isinstance(
            result["primary_concept"],
            str,
        ):
            raise ValueError(
                "primary_concept must be a string or None."
            )

        if not isinstance(
            result["scientific_intent"],
            str,
        ):
            raise ValueError(
                "scientific_intent must be a string."
            )

        if not isinstance(
            result["relevant_concepts"],
            list,
        ):
            raise ValueError(
                "relevant_concepts must be a list."
            )

        if not isinstance(
            result["relevant_context"],
            list,
        ):
            raise ValueError(
                "relevant_context must be a list."
            )

        if not isinstance(
            result["interpretation_notes"],
            str,
        ):
            raise ValueError(
                "interpretation_notes must be a string."
            )

        if not isinstance(
            result["uncertainty"],
            bool,
        ):
            raise ValueError(
                "uncertainty must be a boolean."
            )