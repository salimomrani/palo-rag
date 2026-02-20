import re

_EMAIL_RE = re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b")
_PHONE_RE = re.compile(
    r"(\+33|0033|0)[1-9](\s?\d{2}){4}"
    r"|(\+32|0032|0)[4-9]\d{7}"
    r"|\b0[6-9]\d{8}\b"
)


def mask_pii(text: str) -> str:
    text = _EMAIL_RE.sub("[EMAIL]", text)
    text = _PHONE_RE.sub("[PHONE]", text)
    return text
