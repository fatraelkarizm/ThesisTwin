from app.domain.status import Status
from app.domain.verification import Verdict, verify_quote

PAGES = {
    5: "Bagaimana pengaruh penggunaan platform video pendek terhadap konsentrasi belajar?",
    21: "Penelitian ini menggunakan survei cross-sectional satu kali.",
}


def test_exact_quote_verified():
    v = verify_quote("pengaruh penggunaan platform video pendek", 5, PAGES)
    assert v.ok and v.score == 1.0


def test_tolerates_case_whitespace_punctuation():
    v = verify_quote("PENGARUH  penggunaan, platform video-pendek", 5, PAGES)
    assert v.ok


def test_tolerates_small_ocr_error():
    v = verify_quote("pengaruh penggunaan platfom video pendek", 5, PAGES)
    assert v.ok


def test_page_missing():
    v = verify_quote("apa saja", 99, PAGES)
    assert v.verdict is Verdict.PAGE_MISSING and not v.ok


def test_quote_on_wrong_page_is_not_found():
    v = verify_quote("survei cross-sectional satu kali", 5, PAGES)
    assert v.verdict is Verdict.QUOTE_NOT_FOUND


def test_hallucinated_quote_downgrades_status():
    v = verify_quote("kalimat yang tidak pernah ada di dokumen ini sama sekali", 5, PAGES)
    assert v.status(Status.AI_SUGGESTED) is Status.NEEDS_USER_CONFIRMATION


def test_empty_quote():
    assert verify_quote("   ", 5, PAGES).verdict is Verdict.QUOTE_EMPTY
