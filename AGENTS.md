# AGENTS.md — Aturan untuk semua AI agent & kontributor

ThesisTwin = AI-powered navigation & consistency engine untuk skripsi (STACK 2026 · Case 1).
> *"ThesisTwin tidak menulis skripsi mahasiswa. ThesisTwin mencegah mahasiswa tersesat ketika menyelesaikannya."*

Source of truth produk: [docs/source/01-proposal-full.md](docs/source/01-proposal-full.md). Peta dokumen: [docs/README.md](docs/README.md).
Struktur folder + aturan komponen: **[docs/worktree.md](docs/worktree.md)** (wajib dibaca sebelum menambah file).

## 1. Git — WAJIB
- **Jangan pernah commit/kerja langsung di `main`.** Selalu branch `feature/<slug-pendek>` (bug: `fix/<slug>`, docs: `docs/<slug>`, chore: `chore/<slug>`).
- Cek `git branch --show-current` sebelum mengedit. Kalau `main`, buat branch dulu.
- Commit kecil, Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`, `test:`, `refactor:`).
- Jangan push, merge, force-push, atau ubah `main` tanpa diminta. PR ke `main`.
- Jangan commit `.env`, secret, dokumen mahasiswa asli, atau data peserta.

## 2. Stack (keputusan sementara, finalisasi via ADR di `docs/adr/`)
| Layer | Pilihan |
|---|---|
| Frontend | Next.js (App Router) + TypeScript + Tailwind — `apps/web` |
| Backend | FastAPI + Pydantic v2 + SQLAlchemy 2 async — `apps/api` |
| DB | PostgreSQL + pgvector. Graph = relasional dulu |
| AI | LLM → JSON terstruktur, provider di balik adapter (ADR-003) |

Mengganti stack/dependensi besar = tulis ADR dulu, jangan diam-diam.

## 3. Guardrail Produk (tidak boleh dilanggar kode apa pun)
1. AI **tidak menulis konten skripsi**. Hanya navigasi, konsistensi, pertanyaan klarifikasi.
2. **LLM tidak memutuskan alignment.** Constraint engine deterministik yang memutuskan; LLM hanya mengekstrak & menjelaskan.
3. Setiap `node` dan `finding` **wajib punya evidence** (dokumen + halaman) atau status `needs_user_confirmation`. Dilarang mengarang evidence.
4. Bahasa temuan = **pertanyaan/peringatan, bukan vonis** ("Potential alignment issue", bukan "Salah").
5. Semua keluaran AI berlabel `ai_generated: true` dan lewat **human confirmation** (state machine di [docs/technical-design.md](docs/technical-design.md) §4). `supervisor_confirmed` hanya oleh peran `supervisor`.
6. **Redaction** (NIM, telepon, email, data peserta) sebelum teks dikirim ke LLM. Kirim konteks minimum.
7. Versi dokumen **append-only**; node lama ditandai `superseded_by`, tidak dihapus.
8. Aturan alignment = **data/konfigurasi**, bukan hard-code di logic.
9. Target metrik di docs = hipotesis. Data simulasi wajib berlabel. Jangan menyatakan hasil yang belum diukur.

## 4. Aturan Kode
- **Reuse dulu.** Cari komponen/fungsi yang sudah ada sebelum membuat baru. Buat baru hanya bila dipakai ≥2 tempat atau jelas akan dipakai ulang.
- Perubahan sekecil mungkin yang menyelesaikan task. Tanpa abstraksi spekulatif, tanpa fitur di luar permintaan.
- TypeScript `strict`, tanpa `any` (pakai `unknown` + narrowing). Python: type hints penuh, `ruff` + `mypy`-clean.
- Validasi di batas sistem (input API, output LLM) dengan Zod / Pydantic. Di dalam, percayai tipe.
- Tidak ada komentar yang hanya mengulang kode. Komentar = *kenapa*, bukan *apa*.
- Teks UI Bahasa Indonesia; identifier/kode Bahasa Inggris. Istilah teknis tetap Inggris.
- Test untuk logika domain (state machine, constraint engine, redaction) **sebelum/bersama** implementasi.
- Jangan klaim "selesai/lulus" tanpa menjalankan perintah verifikasi dan melihat output-nya.

## 5. Traceability
Setiap fitur merujuk ID kebutuhan (`FR-xxx`, `NFR-xx`) dan task (`Txx.x`) di [docs/traceability-matrix.md](docs/traceability-matrix.md). Cantumkan di pesan commit/PR.

## 6. Perintah
```bash
# web
cd apps/web && npm install && npm run dev        # http://localhost:3000
npm run lint && npm run typecheck && npm test

# api
cd apps/api && python -m venv .venv && . .venv/Scripts/activate   # Windows Git Bash
pip install -e ".[dev]" && uvicorn app.main:app --reload          # http://localhost:8000/docs
ruff check . && pytest
```
