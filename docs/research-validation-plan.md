# Rencana Riset Pengguna & Validasi

**Versi:** 1.0 (draft) · Sumber: proposal §3.3, §8.5–8.6, §11

## 1. Tujuan
Membuktikan urgensi **spesifik skripsi** di kampus sasaran (bukan memakai angka nasional sebagai klaim kausal) dan menguji hipotesis H1–H3.

## 2. Discovery Research (§11.1)

**Target:** 15–30 mahasiswa (sedang/baru skripsi) · 3–5 dosen pembimbing · 1–2 koordinator TA/staf.

**Pertanyaan riset**
- Tahap mana yang paling sering membuat mahasiswa berhenti bergerak?
- Berapa putaran revisi sebelum proposal diterima?
- Di mana feedback pembimbing disimpan?
- Berapa lama mengubah feedback menjadi daftar tindakan?
- Masalah alignment apa yang paling sering ditemukan dosen?
- Informasi apa yang perlu dilihat dosen sebelum bimbingan?

**Panduan wawancara (mahasiswa) — usulan**
1. Ceritakan perjalanan skripsimu dari awal sampai sekarang.
2. Kapan terakhir merasa "tersesat"? Apa pemicunya?
3. Bagaimana feedback dosen kamu terima & catat? Contoh yang membingungkan?
4. Setelah bimbingan, apa yang kamu lakukan dan berapa lama?
5. Pernah revisi satu bagian lalu bagian lain jadi tidak cocok? Kapan sadar?
6. Berapa kali revisi proposal sebelum diterima?
7. Alat apa yang dipakai (Word, WA, Drive, Notion)? Apa yang kurang?
8. Bagaimana perasaanmu tentang AI membantu skripsi? Batas yang nyaman?

**Panduan wawancara (dosen) — usulan**
1. Berapa mahasiswa bimbingan paralel? Bagaimana menyiapkan diri sebelum sesi?
2. Berapa lama merekonstruksi konteks?
3. Masalah alignment paling sering?
4. Apa yang harus ada di ringkasan pra-bimbingan?
5. Batas apa yang tidak boleh dilampaui AI?
6. Apa yang membuat Anda percaya/tidak percaya temuan AI?

**Etika:** consent tertulis, anonimisasi, boleh berhenti kapan saja, data tidak dipakai untuk training tanpa persetujuan terpisah.

## 3. Dataset Evaluasi (§11.2)
- 20–30 proposal anonim · 50–100 potongan feedback · label inkonsistensi oleh ≥2 evaluator · versi sebelum/sesudah revisi bila ada.
- Bila dokumen nyata tidak bisa dipakai: dataset sintetis berbasis template, **wajib berlabel "data simulasi"**.
- Hitung kesepakatan antar-evaluator (mis. Cohen's κ) dan laporkan.

## 4. Eksperimen (§11.3)

| Kondisi | Deskripsi |
|---|---|
| Baseline | Proposal langsung ke LLM dengan prompt "review consistency" |
| Treatment | Structured extraction + knowledge graph + constraint engine + retrieval |

**Metrik:** precision (dinilai valid oleh dosen) · recall pada gold set · evidence correctness · actionability · waktu penyelesaian tugas pengguna.

## 5. Pemetaan RQ/Hipotesis → Pengujian

| RQ/H | Pengujian | Metrik |
|---|---|---|
| RQ1 / H1 | Baseline vs Treatment pada gold set | Precision, recall |
| RQ2 / H2 | Waktu membuat action plan dengan vs tanpa tool (within-subject bila mungkin) | Waktu; ≥30% lebih cepat |
| RQ3 | Pengulangan isu antarsesi dengan decision memory | Jumlah isu berulang |
| RQ4 | Kesesuaian temuan dengan penilaian dosen | % temuan dinilai valid |
| H3 | Isu yang diputuskan per sesi dengan vs tanpa brief | Proporsi isu terselesaikan |

## 6. Success Metrics (target hipotesis, §11.4)

| Tujuan | Metrik | Target |
|---|---|---|
| Hemat waktu | Waktu action plan | ↓ ≥30% |
| Tindak lanjut | Feedback → action item | ≥80% |
| Ketepatan | Precision alignment | ≥75% |
| Provenance | Temuan bersumber valid | ≥90% |
| Kejelasan | Task completion | ≥80% |
| Usability | SUS | ≥70 |

> Target adalah hipotesis awal. Jangan dipresentasikan sebagai hasil sebelum diuji.

## 7. Pelaporan
Setiap angka dilabeli: **Terukur (n=…, metode)** / **Hipotesis** / **Simulasi**. Cantumkan keterbatasan (ukuran sampel kecil, satu kampus, evaluator terbatas).
