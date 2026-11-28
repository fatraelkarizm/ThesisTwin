from app.domain.structure import extract_by_structure
from app.domain.verification import verify_quote
from app.parsing.pdf import normalize
from app.services.config import extraction

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


def extract(pages):
    return extract_by_structure(pages, extraction())


def test_extracts_numbered_items_and_definitions_from_real_headings():
    got = [(e.type, e.page) for e in extract(PAGES)]
    assert got.count(("research_question", 5)) == 2
    assert got.count(("objective", 5)) == 3
    assert ("method", 20) in got and ("analysis", 20) in got
    assert got.count(("variable", 20)) == 2  # bebas + terikat, kalimat definisinya


def test_table_of_contents_and_table_cells_are_not_sections():
    els = extract(PAGES)
    assert all(e.page != 1 for e in els)  # daftar isi dilewati
    assert not any(e.type == "population" for e in els)  # "Sumber Data" di sel tabel bukan judul


def test_research_questions_end_at_question_mark_and_quotes_verify():
    els = extract(PAGES)
    rqs = [e for e in els if e.type == "research_question"]
    assert rqs[0].content.endswith("pelatihan?")
    assert all(verify_quote(e.quote, e.page, PAGES).ok for e in els)


def test_word_per_line_pdf_text_is_joined():
    raw = "1.2\n \nRumusan\n \nMasalah\n \nBagaimana\n \nemisi?\n"
    assert normalize(raw) == "1.2 Rumusan Masalah Bagaimana emisi?"
    assert normalize("Baris satu panjang sekali.\nBaris dua juga panjang.").startswith("Baris satu")


def test_lowercase_mention_in_prose_is_not_a_heading():
    pages = {1: "Dalam bab ini rumusan masalah dibahas singkat tanpa daftar sama sekali."}
    assert extract(pages) == []


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


def test_single_numbered_objective_is_extracted():
    # Satu tujuan bernomor dulu jatuh ke pemecah kalimat dan tersisa "1" -> temuan palsu R-RQ-OBJ.
    pages = {
        1: (
            "Rumusan Masalah\n1. Bagaimana pengaruh model PBL terhadap pemecahan masalah siswa?\n"
            "Tujuan Penelitian\n1. Mengukur kemampuan pemecahan masalah siswa sebelum dan "
            "sesudah PBL.\nDesain Penelitian\nPenelitian ini memakai desain one-group pre-test."
        )
    }
    got = [e for e in extract(pages) if e.type in {"objective", "research_question"}]
    assert [e.type for e in got] == ["research_question", "objective"]
    assert got[1].content.startswith("Mengukur kemampuan")


def test_objective_heading_without_penelitian_is_detected():
    pages = {
        6: "Bagaimana batas bawahnya? \n1.3 Tujuan \nSesuai rumusan masalah ini: \n"
        "1. Membangun model matematis untuk teka-teki. \n"
        "2. Menganalisis struktur grup gerak keping. \n1.4 Manfaat \nManfaat teoretis."
    }
    objectives = [e for e in extract(pages) if e.type == "objective"]
    assert [e.page for e in objectives] == [6, 6]
    assert objectives[0].content == "Membangun model matematis untuk teka-teki."


def test_longer_heading_starting_with_tujuan_is_not_the_objective():
    pages = {
        8: "2.1 Tujuan Pembelajaran Matematika \n"
        "Pembelajaran matematika bertujuan melatih penalaran siswa secara bertahap."
    }
    assert extract(pages) == []


def test_numbered_procedure_and_analysis_become_one_element_per_item():
    pages = {
        13: "III METODE \n3.3 Prosedur Kerja \n"
        "Prosedur penelitian disusun ke dalam dua tahapan utama berikut: \n"
        "1. Pemodelan Geometri: Mendefinisikan dodekahedron reguler di ruang tiga dimensi. \n"
        "2. Klasifikasi Stiker: Mengelompokkan seluruh keping berdasarkan jumlah stiker. \n"
        "3.4 Analisis Data \nData yang dianalisis berupa struktur aljabar dan permutasi. "
        "Kebenaran hasil divalidasi melalui dua tahap: \n"
        "1. Pembuktian Analitik: Setiap klaim diturunkan dari definisi dan aksioma grup. \n"
        "2. Verifikasi Numerik: Skrip Python menguji koordinat titik sampel tiap stiker."
    }
    got = [(e.type, e.content.split(":")[0]) for e in extract(pages)]
    assert got == [
        ("method", "Pemodelan Geometri"),
        ("method", "Klasifikasi Stiker"),
        ("analysis", "Data yang dianalisis berupa struktur aljabar dan permutasi."),
        ("analysis", "Pembuktian Analitik"),
        ("analysis", "Verifikasi Numerik"),
    ]


def test_rest_of_a_longer_heading_line_is_not_content():
    pages = {
        13: "Bab tiga. \n3.2 Objek Kajian dan Perangkat Komputasi \n"
        "Penelitian ini memadukan pembuktian analitik dengan verifikasi komputasional."
    }
    (got,) = [e for e in extract(pages) if e.type == "population"]
    assert got.content.startswith("Penelitian ini memadukan")
