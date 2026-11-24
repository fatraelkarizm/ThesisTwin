# Step Plan — Breakdown Eksekusi

> Rencana kerja harian yang dipecah per langkah bernomor ada di **[build-steps.md](build-steps.md)**. Dokumen ini tetap menjadi peta milestone.

**Produk:** ThesisTwin · **Versi:** 1.0 (draft) · **Tanggal:** 2026-11-20
Mengikuti fase STACK 2026: Preliminary → Semifinal → Pre-final → Final Day → Post-hackathon (proposal §14).

> **Catatan:** tanggal/durasi spesifik belum ada di proposal; di bawah memakai estimasi **relatif (hari kerja / "efforts")** dan harus disesuaikan dengan kalender resmi STACK 2026. Estimasi = asumsi, bukan komitmen.

Legenda: **P0** wajib demo · **P1** sebaiknya · **P2** bonus. Dependensi ditulis `← ID`.

---

## Milestone Overview

| M | Nama | Fase STACK | Output utama | Exit criteria |
|---|---|---|---|---|
| M0 | Foundation & keputusan stack | Semifinal | Repo, stack terpilih, ontologi v0 | Q2, Q3, Q6 di PRD terjawab |
| M1 | Discovery & validasi masalah | Preliminary/Semifinal | Hasil wawancara, evidence | ≥15 mahasiswa, 3 dosen terwawancara |
| M2 | Ingestion + Extraction | Pre-final | Parser + structured extraction | Bab 1–3 → JSON valid dengan halaman |
| M3 | Graph + Visualisasi | Pre-final | Knowledge graph + UI graph | Self-review bisa confirm/reject |
| M4 | Constraint engine | Pre-final | 5–10 aturan | Aturan lolos review dosen metodologi |
| M5 | Feedback-to-Action | Pre-final | Mapping feedback | UAT-030..033 lulus |
| M6 | Version diff + Impact | Pre-final | Diff & impact | UAT-040..042 lulus |
| M7 | Route map + Brief + Dosen | Pre-final/Final | Dashboard, brief, workspace dosen | UAT-051, 060–062 lulus |
| M8 | Hardening: privasi, guardrail, QA | Final Day | RBAC, redaction, audit | UAT-070..075 lulus |
| M9 | Evaluasi & UAT | Final Day | Hasil eksperimen baseline vs treatment | Metrik tercatat jujur |
| M10 | Demo & pitch | Final Day | Demo 8 langkah, deck, script | UAT-100 lulus 3× berturut |
| M11 | Pilot | Post-hackathon | Uji 1 prodi | Laporan pilot |

---

## M0 — Foundation (estimasi 2–3 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T0.1 | Putuskan Frontend (Next.js PWA vs Flutter Web) | P0 | — | ADR-001 |
| T0.2 | Putuskan Backend (FastAPI vs Node) | P0 | — | ADR-002 |
| T0.3 | Pilih LLM provider + anggaran token; uji structured JSON | P0 | — | ADR-003 |
| T0.4 | Putuskan graph: relational vs Neo4j (default: relational) | P0 | — | ADR-004 |
| T0.5 | Setup repo, CI lint/test, env management, secrets | P0 | T0.1–2 | Repo siap |
| T0.6 | Skema DB v0 dari [data-model.md](data-model.md) | P0 | T0.4 | Migrasi awal |
| T0.7 | Tetapkan kampus/prodi target & format panduan MVP | P0 | — | Policy pack v0 |

## M1 — Discovery & Validasi (paralel, 5–7 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T1.1 | Susun guide wawancara dari [research-validation-plan.md](research-validation-plan.md) | P0 | — | Guide |
| T1.2 | Rekrut 15–30 mahasiswa, 3–5 dosen, 1–2 koordinator | P0 | T1.1 | Jadwal |
| T1.3 | Lakukan wawancara + catat consent | P0 | T1.2 | Transkrip/ringkasan |
| T1.4 | Sintesis: bottleneck, putaran revisi, lokasi feedback | P0 | T1.3 | Insight report |
| T1.5 | Kumpulkan 20–30 proposal anonim + 50–100 feedback (atau sintetis berlabel) | P1 | T1.2 | Dataset v0 |
| T1.6 | Labeling inkonsistensi oleh ≥2 evaluator | P1 | T1.5 | Gold set |

## M2 — Ingestion + Extraction (6–8 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T2.1 | Upload API + object storage + hash/versi | P0 | T0.5 | Endpoint upload |
| T2.2 | Parser DOCX (heading, paragraf, tabel, komentar, halaman) | P0 | T2.1 | Struktur dokumen |
| T2.3 | Parser PDF + pemetaan halaman | P0 | T2.1 | Struktur dokumen |
| T2.4 | Redaction NIM/telepon/email | P1 | T2.2 | Pre-processor |
| T2.5 | Prompt + skema ekstraksi (RQ, objective, variabel, populasi, metode, instrumen, analisis) | P0 | T0.3 | Prompt v1 |
| T2.6 | Validasi skema + retry + log kualitas | P0 | T2.5 | Extractor andal |
| T2.7 | Evidence linking: tiap elemen → dokumen+halaman | P0 | T2.2–3, T2.5 | `source` valid |
| T2.8 | Uji ID & campuran ID–EN | P0 | T2.6 | Laporan akurasi |

## M3 — Knowledge Graph + UI (6–8 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T3.1 | Persist node/edge sesuai ontologi | P0 | T0.6, T2.6 | Graph store |
| T3.2 | Inferensi edge (addresses, requires, measured_by, analyzed_with) | P0 | T3.1 | Edge awal |
| T3.3 | UI visualisasi graph (klik node → panel detail) | P0 | T3.1 | Graph view |
| T3.4 | Self-review: accept/reject/edit node + audit | P0 | T3.3 | Verified graph |

## M4 — Constraint Engine (4–6 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T4.1 | Engine aturan (data-driven) | P0 | T3.1 | Rule runner |
| T4.2 | Implementasi 5–10 aturan dari [alignment-rules.md](alignment-rules.md) | P0 | T4.1 | Rules |
| T4.3 | Format temuan (judul, prioritas, evidence, saran, confidence) | P0 | T4.1 | Finding schema |
| T4.4 | Lapisan LLM penjelas bahasa non-vonis | P1 | T4.3 | Penjelasan |
| T4.5 | Review aturan bersama dosen metodologi | P0 | T4.2 | Sign-off aturan |
| T4.6 | Retrieval (pgvector) panduan/rubrik/feedback/literatur | P1 | T0.6 | Retriever |

## M5 — Feedback-to-Action (3–4 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T5.1 | UI input feedback (manual/tempel teks) | P0 | T3.3 | Form |
| T5.2 | Pemetaan feedback → node terdampak | P0 | T3.1, T5.1 | Mapper |
| T5.3 | Generasi interpretasi + proposed actions + status | P0 | T5.2 | Action items |
| T5.4 | Flow konfirmasi mahasiswa | P0 | T5.3 | Status workflow |

## M6 — Version Diff + Change Impact (4–5 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T6.1 | Diff antarversi di level node | P0 | T3.1 | Diff engine |
| T6.2 | Deteksi isu terselesaikan & dampak baru | P0 | T6.1, T4.1 | Resolusi |
| T6.3 | Change impact (aturan propagasi per tipe node) | P0 | T3.2 | Impact list |
| T6.4 | Unresolved dependency (mis. abstrak vs RQ) | P1 | T6.1 | Flag |

## M7 — Route Map, Brief, Supervisor (5–6 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T7.1 | Route map (bottleneck, blocked, next action) | P0 | T3.2, T4.2 | Dashboard |
| T7.2 | Decision memory (CRUD + tautan ke node) | P1 | T3.1 | Modul |
| T7.3 | Generator bimbingan brief + ekspor | P0 | T5.3, T6.2, T7.2 | Brief |
| T7.4 | Workspace dosen: ringkasan, valid/tidak relevan, konfirmasi | P0 | T7.3 | UI dosen |
| T7.5 | Conflict flag multi-pembimbing | P2 | T5.2 | Flag |

## M8 — Hardening (4–5 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T8.1 | Auth + RBAC + consent gate | P0 | T0.5 | Akses aman |
| T8.2 | Enkripsi transit & at-rest; retention & hapus permanen | P0 | T2.1 | Kontrol privasi |
| T8.3 | Audit trail | P0 | T8.1 | Log |
| T8.4 | Guardrail anti-auto-writing & anti-fabricated-reference + label AI | P0 | T4.4, T5.3 | Prompt/policy |
| T8.5 | Observabilitas (latensi, error, kualitas ekstraksi) | P1 | T2.6 | Dashboard |

## M9 — Evaluasi & UAT (4–6 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T9.1 | Eksperimen: baseline LLM-only vs treatment (precision, recall, evidence, actionability, waktu) | P0 | T1.6, T4.2 | Tabel hasil |
| T9.2 | Eksekusi [UAT.md](UAT.md) (A–J) | P0 | M2–M8 | Laporan UAT |
| T9.3 | SUS + task completion | P0 | T9.2 | Skor |
| T9.4 | Perbaikan defect S1/S2 | P0 | T9.2 | Build stabil |

## M10 — Demo & Pitch (3–4 hari)

| ID | Task | Pri | Dep | Output |
|---|---|---|---|---|
| T10.1 | Dataset demo (skenario Nadia §16) + reset script | P0 | M7 | Data demo |
| T10.2 | Rehearsal 8 langkah, 3× berturut tanpa error | P0 | T10.1 | Demo siap |
| T10.3 | Deck + script dari [pitch-and-demo-script.md](pitch-and-demo-script.md) | P0 | T10.2 | Deck |
| T10.4 | Fallback: rekaman demo + data cache bila API gagal | P0 | T10.2 | Plan B |
| T10.5 | Audit klaim: semua angka berlabel hasil/hipotesis/simulasi | P0 | T9.1 | Checklist |

## M11 — Pilot (pasca-hackathon)

Pilot 1 prodi; perbaikan model; campus policy pack; evaluasi Fase 2 (supervisor workspace) & Fase 3 (integrasi prodi) — proposal §13–14.

---

## Critical Path

`M0 → M2 → M3 → M4 → M6 → M7 → M8 → M9 → M10`
M1 berjalan paralel dan memberi masukan ke M4 (aturan) & M9 (dataset). M5 bisa paralel dengan M4 setelah M3.

## Prioritas Engineering (proposal §14)
1. Structured extraction stabil → 2. Evidence linking → 3. Dependency visualization → 4. Rule-based alignment → 5. Feedback-to-action → 6. Version comparison.

## Definition of Done (per task)
- Kode ter-review + test relevan lulus.
- Dampak ke UAT terkait dicek.
- Guardrail (tidak auto-write, ada evidence, ada label AI) tidak dilanggar.
- Dokumen di `docs/` diperbarui bila perilaku berubah.
