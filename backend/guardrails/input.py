import re
from dataclasses import dataclass

MAX_LENGTH = 500
INJECTION_PATTERNS = [
    r"ignore (previous|prior|all) instructions",
    r"jailbreak",
    r"forget your (system prompt|instructions|context)",
    r"you are now",
    r"act as (if you are|a different|an unrestricted)",
    r"disregard (your|the) (instructions|guidelines|rules)",
    r"(system|assistant)\s*:",
    r"<\|im_start\|>",
]


@dataclass
class GuardrailResult:
    passed: bool
    reason: str | None = None


class InputGuardrail:
    def __init__(self):
        self._injection_re = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)

    def check(self, question: str) -> GuardrailResult:
        if not question or not question.strip():
            return GuardrailResult(passed=False, reason="guardrail:empty_question")
        if len(question) > MAX_LENGTH:
            return GuardrailResult(passed=False, reason="guardrail:length_exceeded")
        if self._injection_re.search(question):
            return GuardrailResult(passed=False, reason="guardrail:prompt_injection")
        return GuardrailResult(passed=True)
