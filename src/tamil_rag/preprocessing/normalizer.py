import re
import unicodedata


ZERO_WIDTH_CHARS = "\u200b\u200c\u200d\ufeff"


def normalize_tamil_text(text: str) -> str:
    """
    Create a retrieval-oriented normalized version of Tamil text.

    The original source text must never be modified by this function.
    """

    if not isinstance(text, str):
        raise TypeError("text must be a string")

    # 1. Unicode normalization.
    text = unicodedata.normalize("NFC", text)

    # 2. Remove invisible zero-width formatting characters.
    text = text.translate(
        str.maketrans("", "", ZERO_WIDTH_CHARS)
    )

    # 3. Normalize tabs/newlines and repeated whitespace.
    text = re.sub(r"\s+", " ", text)

    # 4. Remove leading/trailing whitespace.
    text = text.strip()

    return text