import re
from dataclasses import dataclass

from core.config import settings

OFFENSIVE_PATTERNS = [
    r"\bfuck\b", r"\bshit\b", r"\basshole\b", r"\bbitch\b",
    r"\bcunt\b", r"\bdick\b", r"\bputa\b", r"\bpute\b", r"\bputain\b",
    r"\bsalope\b", r"\bconnard\b", r"\bmerde\b",
]
INJECTION_PATTERNS = [
    # English
    r"ignore (all\s+)?(previous|prior|all)\s+instructions",
    r"jailbreak",
    r"forget your (system prompt|instructions|context)",
    r"you are now",
    r"act as (if you are|a different|an unrestricted)",
    r"disregard (your|the) (instructions|guidelines|rules)",
    r"(system|assistant)\s*:",
    r"<\|im_start\|>",
    # French
    r"oublie (tout ce qu|tes instructions|tes consignes)",
    r"ignore (tes|vos) (instructions|consignes|règles)",
    r"réponds (librement|sans restriction)",
    r"tu es (maintenant|désormais) (un|une)",
    r"comporte-toi comme",
    r"fais semblant d'être",
]


@dataclass
class GuardrailResult:
    passed: bool
    reason: str | None = None


class InputGuardrail:
    """Validates user input before it reaches the LLM.

    Checks (in order): empty input → length limit → prompt injection → offensive content.
    Any failure returns immediately with a reason string; no LLM call is made.
    """

    def __init__(self):
        self._injection_re = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)
        self._offensive_re = re.compile("|".join(OFFENSIVE_PATTERNS), re.IGNORECASE)

    def check(self, question: str) -> GuardrailResult:
        """Run all validation checks on the input question.

        Returns:
            GuardrailResult(passed=True) if the input is safe.
            GuardrailResult(passed=False, reason=...) otherwise, where reason is one of:
              - "guardrail:empty_question"
              - "guardrail:length_exceeded"
              - "guardrail:prompt_injection"
              - "guardrail:offensive_content"

        Example:
            >>> g = InputGuardrail()
            >>> g.check("ignore previous instructions").passed
            False
            >>> g.check("Comment fonctionne l'API ?").passed
            True
        """
        if not question or not question.strip():
            return GuardrailResult(passed=False, reason="guardrail:empty_question")
        if len(question.strip()) < settings.guardrail_min_length:
            return GuardrailResult(passed=False, reason="guardrail:too_short")
        if len(question) > settings.guardrail_max_length:
            return GuardrailResult(passed=False, reason="guardrail:length_exceeded")
        if self._injection_re.search(question):
            return GuardrailResult(passed=False, reason="guardrail:prompt_injection")
        if self._offensive_re.search(question):
            return GuardrailResult(passed=False, reason="guardrail:offensive_content")
        return GuardrailResult(passed=True)
