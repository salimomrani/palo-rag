import re

_EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b")
_PHONE_RE = re.compile(
    r"(\+33|0033|0)[1-9](\s?\d{2}){4}"
    r"|(\+32|0032|0)[4-9]\d{7}"
    r"|\b0[6-9]\d{8}\b"
)


def mask_pii(text: str) -> str:
    """Replace emails and French/Belgian phone numbers with placeholder tokens.

    Example:
        >>> mask_pii("Contact alice@example.com ou 06 12 34 56 78")
        'Contact [EMAIL] ou [PHONE]'
    """
    text = _EMAIL_RE.sub("[EMAIL]", text)
    text = _PHONE_RE.sub("[PHONE]", text)
    return text
