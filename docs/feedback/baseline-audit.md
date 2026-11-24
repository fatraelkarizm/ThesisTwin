# Baseline Audit — Janji Abstrak vs Isi Repo

Diaudit 2026-11-24 terhadap [02-abstract.md](../source/02-abstract.md). "Baseline" di sini punya dua arti, keduanya diperiksa:
- **(A) Baseline janji:** semua yang dijanjikan abstrak untuk tahap sekarang.
- **(B) Baseline eksperimen:** perangkat untuk membandingkan dengan **LLM-only baseline** (abstrak §7).

**Kesimpulan: belum complete.** Fondasi teknis solid dan lulus semua pemeriksaan, tetapi hampir semua fitur yang dijanjikan abstrak belum ada, dan baseline eksperimen baru sekitar seperempat.

## 0. Pemeriksaan teknis (dijalankan hari ini)

| Pemeriksaan | Hasil |
|---|---|
| API `ruff check` | ✅ bersih |
| API `pytest` | ✅ 30 lulus |
| Web `typecheck`, `lint`, `build` | ✅ lolos |
| Branch `features` ter-push, `main` | `features` ✅; `main` **tertinggal** (belum disinkronkan sejak README) |
| Aplikasi berjalan end-to-end | ❌ belum dicoba (uvicorn dan browser belum dijalankan) |

## 1. (A) Janji abstrak vs repo

Legenda: ✅ ada · 🟡 sebagian · ❌ belum.

| # | Janji abstrak | Status | Yang ada | Yang kurang |
|---|---|---|---|---|
| A1 | Identitas tim | ✅ (setelah update ini) | README diisi dari abstrak | Deklarasi orisinalitas ditandatangani |
| A2 | Unggah draf **DOCX/PDF** + komentar terbaru pembimbing | 🟡 | Parser PDF → `{halaman: teks}` | **Tidak ada API upload**, **tidak ada parser DOCX**, komentar tidak dibaca |
| A3 | Ekstrak RQ, objective, variabel, metode, analisis → **dependency graph** | 🟡 | Skema ekstraksi, service (retry + verifikasi), tabel finding | **Tidak ada provider LLM sungguhan**, **tidak ada graph** (node/edge) |
| A4 | Tandai ketidaksesuaian (mis. pertanyaan kausal vs desain one-group pre/post-test [3]) + **bagian wajib panduan program** yang hilang | ❌ | Field `rule_id` di finding; `rules/` hanya berisi README | **Constraint engine belum ada**, aturan belum ditulis, tidak ada pemeriksaan panduan program |
| A5 | Pilih **rule set per program** (Matematika) | ❌ | — | Policy pack, pemilihan program |
| A6 | **Versioned record** + diff elemen antar revisi | ❌ | Prinsip append-only di docs | Tabel `document_versions`/`nodes`, diff, "komentar mana yang sudah ditangani" |
| A7 | **Supervision Brief** per revisi, kirim PDF/chat | ❌ | — | Generator brief, ekspor PDF/teks chat |
| A8 | **Defense Stress-Test**: 3–5 pertanyaan penguji dari tautan terlemah graph + minta justifikasi | ❌ | — | **Tidak ada di PRD/step-plan** sebelum audit ini; spesifikasi dan kode |
| A9 | **Dosen tanpa akun** | ⚠️ **konflik** | — | PRD FR-001/FR-111 mensyaratkan akun dosen; lihat §3 |
| A10 | Stack: Next.js ✅, FastAPI ✅, **PostgreSQL + pgvector** | ⚠️ **menyimpang** | SQLite dipakai sementara (keputusan tim 24 Nov) | Retrieval panduan (pgvector) belum ada; jalur migrasi ke PostgreSQL belum dites |
| A11 | Data berizin, tidak untuk training | 🟡 | Kebijakan ditulis di docs; template consent | Alur consent di aplikasi belum ada |
| A12 | **10 proposal anonim end-to-end per 30 Nov** (6 hari lagi) | ❌ | Komponen terpisah (parser PDF, ekstraksi, verifikasi) | Tidak ada proposal yang diproses; rantai belum tersambung |
| A13 | Brief + stress-test selesai **16 Des** (22 hari lagi) | ❌ | — | Lihat A7, A8 |
| A14 | Bukti: 7 mahasiswa + 1 pembimbing; "7–14 hari" tunggu feedback | 🟡 | Template log | **Catatan primer belum di repo**; survei lebih besar "sebelum semifinal" belum ada |

Ringkas: dari 14 butir, **✅1, 🟡4, ❌7, ⚠️2**.

## 2. (B) Baseline eksperimen: LLM-only vs ThesisTwin

Abstrak §7: tiga metrik, masing-masing "≥" **LLM-only baseline**, pilot 10 mahasiswa + 3 dosen.

| Komponen baseline | Status | Catatan |
|---|---|---|
| Metrik precision/recall per tipe elemen | ✅ | [metrics.py](../../apps/api/app/domain/metrics.py), 5 tes |
| Antarmuka LLM yang dipakai bersama kedua lengan | 🟡 | `LLMClient` ada; belum ada implementasi nyata |
| **Runner baseline LLM-only** (proposal → prompt "review consistency" → temuan) | ❌ | Belum ada kode maupun prompt baku |
| **Set emas**: 10 proposal anonim + label manual ≥2 anotator | ❌ | Belum ada data |
| Definisi **"extraction agreement"** (target 80%) | ❌ | Abstrak tidak mendefinisikan; usul: F1 per elemen vs anotasi manual, pencocokan konten + halaman |
| Pengukuran **waktu review per revisi** (target −50%) | ❌ | Butuh pilot 10+3 dan protokol pencatatan waktu |
| Rating relevansi stress-test (target 4/5) | ❌ | Butuh fitur A8 dan formulir rating dosen |
| Perlakuan **adil** untuk baseline | ❌ | Prompt, model, dan input harus sama; dicatat sebelum uji |

Ringkas: **1 dari 8 ✅**, 1 🟡, 6 ❌. Baseline belum bisa dijalankan.

## 3. Konflik dan keputusan yang harus diambil tim

| Isu | Abstrak | Repo/docs | Usulan ★ |
|---|---|---|---|
| Akun dosen | **Tidak perlu akun**; dosen menerima ringkasan | PRD FR-001 (auth dosen), FR-111 (workspace dosen), [data-model](../data-model.md) `supervisor_confirmed` oleh peran dosen | Ubah: dosen menerima tautan/PDF brief tanpa login. Konfirmasi dosen lewat tautan bertoken sekali pakai (usulan), atau tunda `supervisor_confirmed` ke P1 |
| Database | PostgreSQL + pgvector | SQLite sementara | Pertahankan SQLite untuk 30 Nov, tapi **tulis ADR** dan tes migrasi sebelum pilot; retrieval panduan bisa memakai pencarian teks dulu |
| Fitur lebar | 4 langkah inti: upload → graph+flag → brief → stress-test | PRD memuat Route Map, Decision Memory, multi-supervisor | Turunkan ketiganya ke "later" (sudah di [features.md](features.md)) |
| Stress-Test | Fitur inti langkah 4 | Tidak ada di PRD | Tambahkan FR dan UAT (usulan: FR-130..132) |
| Metrik | 50% review time, 80% agreement, 4/5 relevance | PRD NFR/BO: 30% action plan, precision ≥75% | Selaraskan ke angka abstrak; sisanya jadi sekunder |
| Cakupan bahasa | "Indonesian universities", 1 prodi Matematika | Proposal: umum | Fokus Matematika: **persamaan/simbol** jadi risiko ekstraksi nyata |

## 4. Urutan kerja yang menutup baseline (usulan ★)

Dibatasi dua tenggat: **30 Nov** (6 hari) dan **16 Des** (22 hari).

| Urut | Pekerjaan | Menutup | Target |
|---|---|---|---|
| 1 | Putuskan konflik §3 (terutama akun dosen, SQLite vs PostgreSQL) dan tulis ADR | A9, A10 | 25 Nov |
| 2 | Hubungkan **provider LLM** (ADR-003) + skrip CLI: PDF → halaman → ekstraksi → laporan verifikasi | A3, A12 | 26 Nov |
| 3 | Kumpulkan **10 proposal anonim berizin** (atau sintetis berlabel) + beri label manual ≥2 anotator | A12, B (set emas) | 27–28 Nov |
| 4 | **Runner baseline LLM-only** dengan prompt baku, keluaran dibandingkan dengan `metrics.py` | B | 28 Nov |
| 5 | Constraint engine + 5–10 aturan (termasuk kausal vs one-group pre/post, bagian wajib panduan Matematika) | A4, A5 | 29 Nov |
| 6 | Jalankan 10 proposal end-to-end, laporkan angka apa adanya | A12 | **30 Nov** |
| 7 | Versioned record + diff, lalu Supervision Brief (PDF/teks) | A6, A7 | s.d. 8 Des |
| 8 | Defense Stress-Test (spesifikasi → kode → formulir rating dosen) | A8 | s.d. 14 Des |
| 9 | Pilot 10+3, ukur waktu review, rating, agreement | B | s.d. 16 Des |

Catatan: butir 3 dan 9 butuh orang dan izin, bukan kode. Tanpa 10 proposal berlabel, klaim "80% agreement" tidak bisa dibuktikan.

## 5. Yang sengaja tidak diklaim

- Tidak ada angka akurasi: belum ada proposal nyata yang diproses.
- Tidak ada klaim superioritas atas LLM-only: pembandingnya belum dijalankan.
- Tes yang lulus memakai LLM palsu; itu membuktikan logika verifikasi, bukan kualitas ekstraksi LLM.
