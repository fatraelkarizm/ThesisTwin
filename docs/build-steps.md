# Build Steps — Rencana Kerja Langkah demi Langkah

Rencana eksekusi yang dipecah jadi **langkah kecil bernomor**. Satu langkah = satu tujuan = satu commit (atau beberapa commit kecil) = push ke `features`. **Kerjakan satu langkah, verifikasi, baru lanjut.** Jangan menggabungkan beberapa langkah dalam satu putaran kerja.

Rujukan: [step-plan.md](step-plan.md) (milestone M0–M11) · [feedback/baseline-audit.md](feedback/baseline-audit.md) (janji abstrak) · [design/README.md](design/README.md) (referensi UI) · [worktree.md](worktree.md) (aturan struktur)

## Cara memakai dokumen ini

1. Ambil langkah teratas yang statusnya ⬜ dan tidak terblokir.
2. Baca kolom **Selesai jika**: itu definisi selesai, bukan perkiraan.
3. Jalankan **Verifikasi**, simpan buktinya (output perintah) di pesan commit/PR.
4. Ubah status di tabel ini ke ✅ pada commit yang sama.
5. Langkah bertanda 👥 butuh orang/keputusan tim; AI agent tidak boleh mengarang hasilnya.

Status: ⬜ belum · 🔄 dikerjakan · ✅ selesai · ⛔ terblokir · 👥 butuh tim

## Tenggat dari abstrak

| Tenggat | Komitmen | Langkah terkait |
|---|---|---|
| **30 Nov 2026** (semifinal) | Upload, ekstraksi, cek konsistensi end-to-end pada 10 proposal anonim | 1–15 |
| **16 Des 2026** (Final Day) | Supervision Brief + Defense Stress-Test + pilot | 16–27 |

---

## Fase 0 — Keputusan (paralel, 👥)

| # | Langkah | Selesai jika | Status |
|---|---|---|---|
| 0.1 👥 | Putuskan **akun dosen** (abstrak: tanpa akun) vs PRD FR-001/FR-111 | Keputusan tertulis di `docs/adr/ADR-005-supervisor-access.md` | ⬜ |
| 0.2 👥 | Putuskan **SQLite vs PostgreSQL** untuk pilot | `docs/adr/ADR-004-database.md` | ⬜ |
| 0.3 👥 | Pilih **provider LLM** + anggaran token | `docs/adr/ADR-003-llm-provider.md`; API key tersedia di `.env` (tidak di-commit) | ⬜ |
| 0.4 👥 | Sumber **10 proposal anonim berizin** + 2 anotator | Daftar sumber + consent tercatat di luar repo | ⬜ |
| 0.5 👥 | Ambil **panduan proposal prodi Matematika** (bagian wajib) | Teks panduan tersedia untuk Langkah 10 | ⬜ |

---

## Fase 1 — Tampilan dasar (UI shell)

### Langkah 1 — Referensi desain & design tokens
- **Tujuan:** menetapkan bahasa visual dari referensi (Notalx) sebelum membangun layar.
- **Output:** `docs/design/README.md`, `docs/design/references/*`, token warna/radius/shadow di `apps/web/src/app/globals.css`.
- **Selesai jika:** brief desain menjelaskan apa yang diambil dan **apa yang sengaja tidak diambil** dari tiap referensi; token baru dipakai komponen yang ada.
- **Verifikasi:** `npm run typecheck && npm run lint && npm run build`.
- **Status:** ✅ (2026-11-24)

### Langkah 2 — App shell: sidebar + topbar
- **Tujuan:** kerangka navigasi seperti Notalx: sidebar kiri, topbar dengan pencarian dan aksi utama.
- **Output:** `components/features/shell/` (Sidebar, Topbar), `app/layout.tsx` memakai shell. Menu yang belum dibangun tampil non-aktif dengan label "Segera", bukan tautan mati.
- **Selesai jika:** shell responsif (sidebar tersembunyi di layar kecil), fokus keyboard terlihat, tidak ada tautan 404.
- **Verifikasi:** typecheck, lint, build; buka di browser desktop + lebar 375px.
- **Status:** ✅ (2026-11-24) — dicek di browser: desktop terang/gelap, 375px, fokus Tab, konsol bersih. Catatan: di < 768px belum ada menu navigasi (baru satu rute).

### Langkah 3 — Dashboard: kartu proposal, panel Tools, statistik, temuan
- **Tujuan:** layar utama berbasis konsep Notalx: kartu ringkasan proposal, **panel "Tools"** (ikon + judul + status + deskripsi + chevron), ubin statistik, daftar temuan dengan aksi konfirmasi, riwayat versi.
- **Output:** `components/features/dashboard/*`, `components/ui/Card.tsx`, data simulasi berlabel.
- **Selesai jika:** semua angka berlabel **data simulasi**; tidak ada skor/persentase karangan yang tampak seperti hasil nyata; Tools yang belum ada berstatus "Segera".
- **Verifikasi:** typecheck, lint, build; cek kontras teks (WCAG AA).
- **Status:** ✅ (2026-11-24) — dicek di browser: desktop terang, 375px gelap, klik Konfirmasi/Tolak mengubah status, konsol bersih. Keterbatasan: angka "Temuan terbuka" di kartu versi statis (tidak ikut berubah saat temuan ditolak); diperbaiki saat data API tersambung (Langkah 10+).

### Langkah 4 — Tes komponen web (vitest + Testing Library)
- **Tujuan:** memenuhi aturan [worktree.md](worktree.md) §3.11.
- **Selesai jika:** `StatusBadge`, `FindingCard`, `EvidenceChip`, panel Tools punya tes render; `npm test` lulus.
- **Status:** ✅ (2026-11-24) — 12 tes. Jalankan lewat `npm test` (scripts/vitest.mjs menormalkan huruf drive Windows).

---

## Fase 2 — Unggah dokumen (menuju 30 Nov)

### Langkah 5 — Tabel proyek, dokumen, versi (append-only)
- **Output:** model `projects`, `documents`, `document_versions` (hash SHA-256, nomor versi), service `add_version`.
- **Selesai jika:** versi tidak pernah ditimpa; file sama (hash sama) tidak membuat versi baru; tes lulus.
- **Status:** ✅ (2026-11-24) — 5 tes. Isi sama dengan versi terakhir tidak membuat versi baru; kembali ke isi lama tetap versi baru.

### Langkah 6 — API upload PDF + consent gate
- **Output:** `POST /projects/{id}/documents` (multipart), penyimpanan file lokal di folder yang di-ignore git, tolak bila consent belum diberikan.
- **Selesai jika:** upload tanpa consent → 403; PDF valid → versi tersimpan + halaman terparse; tes API lulus.
- **Status:** ✅ (2026-11-24) — 6 tes API + uji asap uvicorn dengan PDF abstrak nyata (403 tanpa consent, 201 v1 dua halaman). Tipe file dideteksi dari isi, bukan nama. Error service dipetakan ke HTTP di `app/api/errors.py`.

### Langkah 7 — Parser DOCX + komentar pembimbing
- **Output:** `parsing/docx.py`: paragraf, heading, tabel, **komentar** (penulis, teks, anchor).
- **Selesai jika:** komentar DOCX terbaca; keterbatasan halaman DOCX terdokumentasi (DOCX tidak punya halaman tetap → pakai nomor bagian/paragraf).
- **Status:** ✅ (2026-11-24) — 12 tes. Lokasi DOCX = **nomor bagian** (dipotong per heading, `unit: "section"`), bukan halaman. XML dibaca dengan defusedxml + batas ukuran. Belum diuji dengan file Word/Google Docs nyata. Catatan privasi: nama penulis komentar (dosen) ikut tersimpan.

### Langkah 8 — Layar unggah di web
- **Output:** halaman `/upload`: pilih prodi (rule set), centang consent, unggah DOCX/PDF, status hasil.
- **Selesai jika:** alur berjalan ke API lokal; error tampil jelas dalam bahasa Indonesia.
- **Status:** ✅ (2026-11-24) — 4 tes komponen + uji end-to-end di browser (web :3123 → API :8000, PDF abstrak nyata → v1, 2 halaman). Proyek aktif disimpan di localStorage. Untuk dev: set `NEXT_PUBLIC_API_URL` bila API bukan di :8000, dan `THESISTWIN_CORS_ORIGINS` bila web bukan di :3000.

---

## Fase 3 — Ekstraksi & graph

### Langkah 9 — Adapter provider LLM
- **Output:** implementasi `LLMClient` untuk provider ADR-003, timeout, log latensi/error (NFR-09).
- **Selesai jika:** satu panggilan nyata berhasil dari skrip; tes tetap memakai LLM palsu.
- **Status:** ⛔ (butuh 0.3)

### Langkah 10 — Ekstraksi end-to-end satu proposal
- **Output:** CLI `python -m app.cli.extract <file>` → elemen + laporan verifikasi (VERIFIED / QUOTE_NOT_FOUND / PAGE_MISSING).
- **Selesai jika:** satu proposal nyata/sintetis diproses; rasio terverifikasi dilaporkan apa adanya.
- **Status:** ⛔ (butuh 9)

### Langkah 11 — Simpan elemen sebagai node + edge
- **Output:** tabel `nodes`, `edges` sesuai [data-model.md](data-model.md); inferensi edge `addresses`, `requires`, `measured_by`, `analyzed_with`.
- **Selesai jika:** node tanpa evidence hanya berstatus `needs_user_confirmation`; tes lulus.
- **Status:** ⬜

### Langkah 12 — Tampilan dependency graph
- **Output:** halaman `/graph`: node + edge, klik node → panel sumber/status.
- **Status:** ⬜ (butuh 11)

---

## Fase 4 — Cek konsistensi

### Langkah 13 — Rule engine membaca `rules/*.yaml`
- **Output:** engine deterministik; tiap finding membawa `rule_id` (abstrak: "each flag cites a rule").
- **Selesai jika:** menambah aturan = menambah file data + tes, tanpa mengubah engine.
- **Status:** ⬜

### Langkah 14 — 5–10 aturan pertama
- **Output:** termasuk **pertanyaan kausal vs desain one-group pre/post-test** (abstrak [3]), RQ→objective, objective→analisis, variabel→instrumen, **bagian wajib panduan Matematika**.
- **Selesai jika:** tiap aturan punya contoh lulus + gagal; bahasa temuan berupa pertanyaan.
- **Status:** ⬜ (bagian panduan butuh 0.5)

### Langkah 15 — Jalankan 10 proposal + laporan (tenggat 30 Nov)
- **Output:** `docs/reports/2026-11-30-extraction.md`: rasio verifikasi, precision/recall vs label manual, kegagalan.
- **Selesai jika:** angka dilaporkan jujur, termasuk yang buruk; data sintetis berlabel.
- **Status:** 👥 ⛔ (butuh 0.4, 10, 14)

---

## Fase 5 — Baseline LLM-only

### Langkah 16 — Set emas berlabel
- **Output:** format anotasi (JSON) + 10 proposal berlabel oleh 2 anotator + kesepakatan antar-anotator.
- **Status:** 👥

### Langkah 17 — Runner baseline LLM-only
- **Output:** prompt baku "review consistency", model sama, hasil dibandingkan dengan `metrics.py`.
- **Selesai jika:** baseline dan ThesisTwin dijalankan pada input yang sama; prompt dicatat sebelum uji.
- **Status:** ⬜ (butuh 9, 16)

---

## Fase 6 — Rekam versi & brief (menuju 16 Des)

### Langkah 18 — Diff elemen antar versi
- **Output:** bandingkan node v(n) vs v(n-1): berubah / baru / hilang / isu selesai / dampak baru.
- **Status:** ⬜

### Langkah 19 — Pelacakan komentar yang ditangani
- **Output:** komentar DOCX v(n-1) → apakah bagian terkait berubah di v(n) → status "kemungkinan ditangani" (butuh konfirmasi mahasiswa).
- **Status:** ⬜ (butuh 7, 18)

### Langkah 20 — Supervision Brief
- **Output:** ringkasan 1 halaman: apa yang berubah, komentar yang ditangani, keputusan terbuka; ekspor **PDF** dan **teks chat**.
- **Selesai jika:** brief hanya merangkum state, tidak menulis konten penelitian.
- **Status:** ⬜

### Langkah 21 — Akses brief untuk dosen tanpa akun
- **Output:** sesuai keputusan 0.1 (mis. tautan bertoken).
- **Status:** ⛔ (butuh 0.1)

### Langkah 22 — Defense Stress-Test
- **Output:** pilih 3–5 tautan terlemah graph (deterministik) → pertanyaan penguji (LLM, berlabel AI) → kolom justifikasi mahasiswa.
- **Selesai jika:** pemilihan tautan bisa dijelaskan; pertanyaan tidak berisi jawaban.
- **Status:** ⬜

### Langkah 23 — Formulir rating dosen untuk stress-test
- **Output:** skala 1–5 relevansi per pertanyaan (target abstrak 4/5).
- **Status:** ⬜ (butuh 21, 22)

---

## Fase 7 — Pengerasan & pilot

### Langkah 24 — Privasi & audit
- **Output:** cakupan redaction diuji, audit log semua aksi, hapus permanen (FR-122).
- **Status:** ⬜

### Langkah 25 — Protokol pilot 10 mahasiswa + 3 dosen
- **Output:** cara mencatat waktu review per revisi (target −50%), formulir, consent.
- **Status:** 👥

### Langkah 26 — Pilot & laporan
- **Status:** 👥

### Langkah 27 — Demo Final Day
- **Output:** skrip demo 8 langkah ([pitch-and-demo-script.md](pitch-and-demo-script.md)), data cadangan, 3× uji tanpa gagal.
- **Status:** ⬜
