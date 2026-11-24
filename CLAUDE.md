@AGENTS.md

# Khusus Claude Code

## Skill yang terpasang di `.claude/skills/` (proyek ini)
Pakai sesuai konteks, jangan semuanya sekaligus:

| Situasi | Skill |
|---|---|
| Rencana fitur / pecah task dari step-plan | `brainstorming` → `writing-plans` → `executing-plans` |
| Implementasi logika domain | `test-driven-development`, `ponytail` (perubahan minimal) |
| Bug / test gagal | `systematic-debugging` (akar masalah dulu, baru fix) |
| Sebelum bilang "selesai" | `verification-before-completion` |
| Review | `requesting-code-review`, `ponytail-review` |
| UI baru / ubah UI | `ui-ux-pro-max`, `antislop-ui`, `antislop-human`, `ui-styling` |
| Teks UI / copy | `antislop-copywriting` |
| React/Next.js | `vercel-react-best-practices`, `vercel-composition-patterns` |
| FastAPI | `fastapi-expert` |
| Skema / migrasi / query Postgres | `supabase-postgres-best-practices` |
| Tes browser / UAT | `webapp-testing` |
| Hemat token | `caveman` (opsional, atas permintaan) |

## Cara kerja
- Mulai sesi: `git branch --show-current`. Di `main` → buat `feature/...` dulu.
- Sebelum menambah komponen/folder: baca [docs/worktree.md](docs/worktree.md) dan ikuti kontrak per layer.
- Untuk pertanyaan arsitektur/dokumen, baca `docs/` dulu (jangan menebak). Konflik antar dokumen → proposal menang.
- Bila docs dan kode berbeda, tanyakan; jangan diam-diam mengubah salah satunya.
