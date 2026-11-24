from app.domain.structure import extract_by_structure
from app.domain.verification import verify_quote
from app.parsing.pdf import normalize

PAGES = {
    1: "DAFTAR ISI 1.2 Rumusan Masalah 5 1.3 Tujuan Penelitian 6 3.2.2 Variabel Penelitian 20",
    5: (
        "1.1 Latar Belakang Pertumbuhan model besar menimbulkan masalah energi. "
        "1.2 Rumusan Masalah Berdasarkan uraian di atas, rumusan masalah adalah: "
        "1. Bagaimana besaran emisi karbon model BERT selama pelatihan? "
        "2. Model manakah yang paling efisien tanpa mengorbankan akurasi? "
        "1.3 Tujuan Penelitian Penelitian ini bertujuan untuk: "
        "1. Mengukur emisi karbon model BERT dan DistilBERT. "
        "2. Mengidentifikasi model paling efisien. 3. Memberikan rekomendasi praktik Green AI."
    ),
    9: "Tabel 2.1 Penelitian Terdahulu Penulis Sumber Data Temuan Kunci",
    20: (
        "3.2 Desain dan Variabel Penelitian 3.2.1 Desain Penelitian Penelitian ini dirancang "
        "menggunakan metode eksperimental dengan pendekatan komparatif. Eksperimen membandingkan "
        "dua skenario. 3.2.2 Variabel Penelitian Pertama, Variabel Bebas. Dalam penelitian ini, "
        "variabel bebasnya adalah jenis arsitektur model bahasa. Kedua, Variabel Terikat. "
        "Penelitian ini mengukur emisi sebagai variabel terikat, yaitu emisi karbon dan akurasi. "
        "3.3 Analisis Data Analisis dilakukan dengan membandingkan rata-rata metrik kedua model."
    ),
}


def test_extracts_numbered_items_and_definitions_from_real_headings():
    got = [(e.type, e.page) for e in extract_by_structure(PAGES)]
    assert got.count(("research_question", 5)) == 2
    assert got.count(("objective", 5)) == 3
    assert ("method", 20) in got and ("analysis", 20) in got
    assert got.count(("variable", 20)) == 2  # bebas + terikat, kalimat definisinya


def test_table_of_contents_and_table_cells_are_not_sections():
    els = extract_by_structure(PAGES)
    assert all(e.page != 1 for e in els)  # daftar isi dilewati
    assert not any(e.type == "population" for e in els)  # "Sumber Data" di sel tabel bukan judul


def test_research_questions_end_at_question_mark_and_quotes_verify():
    els = extract_by_structure(PAGES)
    rqs = [e for e in els if e.type == "research_question"]
    assert rqs[0].content.endswith("pelatihan?")
    assert all(verify_quote(e.quote, e.page, PAGES).ok for e in els)


def test_word_per_line_pdf_text_is_joined():
    raw = "1.2\n \nRumusan\n \nMasalah\n \nBagaimana\n \nemisi?\n"
    assert normalize(raw) == "1.2 Rumusan Masalah Bagaimana emisi?"
    assert normalize("Baris satu panjang sekali.\nBaris dua juga panjang.").startswith("Baris satu")


def test_lowercase_mention_in_prose_is_not_a_heading():
    pages = {1: "Dalam bab ini rumusan masalah dibahas singkat tanpa daftar sama sekali."}
    assert extract_by_structure(pages) == []


def test_forbidden_section_finding_points_to_its_page_not_the_toc():
    from app.domain.rules import evaluate
    from app.services.rules import load_rules

    rule = next(r for r in load_rules() if r.id == "R-PROPOSAL-RESULTS")
    pages = {
        3: "DAFTAR ISI BAB IV HASIL DAN PEMBAHASAN 30",
        31: "BAB IV HASIL DAN PEMBAHASAN 4.1 ...",
    }
    [f] = evaluate(rule, [], "\n".join(pages.values()), pages)
    assert [(e.element, e.page) for e in f.evidence] == [("section:Hasil dan Pembahasan", 31)]
    assert f.status.value == "ai_suggested"


def test_count_finding_names_what_is_counted():
    from app.domain.rules import Element, evaluate
    from app.services.rules import load_rules

    rule = next(r for r in load_rules() if r.id == "R-RQ-OBJ-COUNT")
    els = [Element(f"r{i}", "research_question", "Apa?", 1) for i in range(3)] + [
        Element(f"o{i}", "objective", "Mengukur.", 1) for i in range(4)
    ]
    [f] = evaluate(rule, els)
    assert f.title.endswith("3 rumusan masalah, 4 tujuan")
