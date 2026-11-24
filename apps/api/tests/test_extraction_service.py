import json

from app.domain.status import Status
from app.domain.verification import Verdict
from app.services.extraction import extract_elements

PAGES = {
    5: "Bagaimana pengaruh platform video pendek terhadap konsentrasi? Hubungi 081234567890.",
    21: "Desain: survei cross-sectional.",
}


class FakeLLM:
    def __init__(self, *replies: str) -> None:
        self.replies = list(replies)
        self.prompts: list[str] = []

    def complete_json(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.replies.pop(0)


def _el(quote: str, page: int, **over) -> dict:
    base = dict(
        element_type="research_question", content="RQ1", quote=quote, page=page, confidence=0.9
    )
    return {**base, **over}


def test_verified_and_hallucinated_elements_are_separated():
    good = _el("pengaruh platform video pendek terhadap konsentrasi", 5)
    fake = _el("kutipan karangan yang tidak ada", 21, element_type="method")
    llm = FakeLLM(json.dumps({"elements": [good, fake]}))
    r = extract_elements(llm, PAGES)
    assert [e.verdict for e in r.elements] == [Verdict.VERIFIED, Verdict.QUOTE_NOT_FOUND]
    assert r.elements[0].status is Status.AI_SUGGESTED
    assert r.elements[1].status is Status.NEEDS_USER_CONFIRMATION
    assert r.verified_ratio == 0.5


def test_retries_invalid_json_then_succeeds():
    ok = json.dumps({"elements": [_el("survei cross-sectional", 21)]})
    llm = FakeLLM("bukan json", json.dumps({"elements": [{"element_type": "x"}]}), ok)
    r = extract_elements(llm, PAGES)
    assert r.attempts == 3 and not r.schema_failed and len(r.elements) == 1


def test_gives_up_after_max_attempts_without_guessing():
    llm = FakeLLM("x", "y", "z")
    r = extract_elements(llm, PAGES, max_attempts=3)
    assert r.schema_failed and r.elements == [] and r.attempts == 3


def test_llm_never_sees_pii():
    llm = FakeLLM(json.dumps({"elements": []}))
    extract_elements(llm, PAGES)
    assert "081234567890" not in llm.prompts[0] and "[TELEPON]" in llm.prompts[0]
