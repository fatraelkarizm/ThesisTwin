# Features — Komentar Juri dan Fokus Fitur

Sumber: skor Preliminary ([gambar](images/preliminary-score.png)). Bagian "Fokus fitur" adalah **usulan penyusun** (★), bukan keputusan tim; validasi dulu.

## Komentar juri (verbatim)

> Wawancara tujuh mahasiswa dan satu pembimbing plus literatur relevan, tapi masih kecil. Revisi proposal, graf elemen penelitian, cek konsistensi, dan brief untuk supervisor menjawab proses skripsi di kampus. Pembeda lewat rekam versi dan brief jelas, tapi cuma dibandingkan dengan chatbot umum. Satu program studi, data berizin, target terukur, dan tonggak bertanggal cukup realistis, walaupun mitigasi kesalahan ekstraksi belum detail. Abstraknya rapi.

## Yang dipuji juri (pertahankan)

| Poin | Artinya untuk produk |
|---|---|
| Revisi proposal, graf elemen penelitian, cek konsistensi, brief supervisor menjawab proses skripsi | Empat hal ini adalah inti nilai |
| **Pembeda = rekam versi + brief** | Ini diferensiator yang dilihat juri; jangan tertutup fitur lain |
| Satu prodi, data berizin, target terukur | Scope sempit dan etika data dinilai realistis |
| **Tonggak bertanggal** | Wajib ada tanggal di rencana pengembangan |

## Yang dikritik juri

| Kritik | Kriteria | Dampak skor |
|---|---|---|
| Bukti masih kecil (7 mahasiswa + 1 pembimbing) | P1 | −6 |
| Hanya dibandingkan dengan chatbot umum | P3 | −5 |
| Mitigasi kesalahan ekstraksi belum detail | P4 | −3 |

Analisis lengkap dan status tiap kritik: [gap.md](gap.md).

## ★ Fokus fitur (usulan)

Juri memuji pembeda "rekam versi dan brief". README saat ini memperkenalkan enam fitur sekaligus. Usulan: kunci demo dan pitch pada inti, tahan sisanya.

| Tier | Fitur | Alasan |
|---|---|---|
| **Inti (demo wajib)** | Version record + version diff (FR-070, FR-071) | Pembeda yang dipuji juri |
| **Inti** | Supervision Brief (FR-100) | Pembeda yang dipuji juri |
| **Inti** | Dependency graph + Alignment Checker dengan evidence (FR-030, FR-040, FR-041) | Disebut juri sebagai jawaban proses skripsi |
| **Inti** | Feedback-to-Action (FR-060–062) | Menghubungkan feedback ke revisi |
| Pendukung | Human confirmation workflow (FR-110) | Sudah ada state machine-nya; syarat integritas |
| **Tahan dulu** | Thesis Route Map (FR-090) | Tidak disebut juri; melebarkan scope |
| **Tahan dulu** | Decision Memory (FR-080) | Tidak disebut juri; melebarkan scope |
| **Tahan dulu** | Multi-supervisor conflict (FR-113) | Sudah P1 di PRD |

Konsekuensi: README bagian "Distinguishing features" sebaiknya menonjolkan version record + brief di depan, bukan enam fitur sejajar.

## Item dari abstrak (sudah dibaca)

Abstrak kini ada di repo: [02-abstract.md](../source/02-abstract.md).

| Item | Isi di abstrak | Status |
|---|---|---|
| **Defense Stress-Test** | Sebelum seminar, ubah tautan terlemah graph jadi 3–5 pertanyaan penguji; minta mahasiswa membenarkan tiap pilihan | Terdefinisi; belum ada FR/UAT/kode |
| **Prodi Matematika** | Versi pertama untuk satu prodi Matematika | Di README; risiko: persamaan/simbol |
| **Dosen tanpa akun** | Dosen menerima ringkasan tanpa membuat akun | **Konflik dengan PRD** FR-001/FR-111, lihat [baseline-audit.md](baseline-audit.md) §3 |
| **Target** | Waktu review −50%, kesepakatan ekstraksi 80%, rating stress-test 4/5, masing-masing ≥ baseline LLM-only | Pengukuran belum ada |
| **Tenggat** | 10 proposal anonim end-to-end 30 Nov; brief + stress-test 16 Des | Lihat audit |
