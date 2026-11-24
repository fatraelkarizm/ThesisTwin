# ThesisTwin

AI-powered navigation & consistency engine untuk perjalanan skripsi (STACK 2026 · Case 1).

- Dokumentasi: [docs/README.md](docs/README.md)
- Aturan kontributor & AI agent: [AGENTS.md](AGENTS.md) · [CLAUDE.md](CLAUDE.md)
- Struktur folder & aturan komponen: [docs/worktree.md](docs/worktree.md)

## Menjalankan

```bash
# Frontend  → http://localhost:3000
cd apps/web && npm install && npm run dev

# Backend   → http://localhost:8000/docs
cd apps/api && python -m venv .venv && . .venv/Scripts/activate
pip install -e ".[dev]" && uvicorn app.main:app --reload
```

Cek kualitas: `npm run lint && npm run typecheck && npm run build` (web), `ruff check . && pytest` (api).

## Alur kerja
Jangan kerja di `main`. Buat branch `feature/<nama>`, commit kecil, buka PR. Detail di [AGENTS.md](AGENTS.md).

## Status
Scaffold awal: UI komponen domain (StatusBadge, EvidenceChip, FindingCard) dengan data simulasi, dan backend dengan state machine status + invarian evidence. Belum ada ingestion, ekstraksi LLM, atau database.
