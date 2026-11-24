# Technical Design

**Versi:** 1.0 (draft) · Sumber: proposal §9 · Rujukan: [data-model.md](data-model.md), [alignment-rules.md](alignment-rules.md)

## 1. Pipeline

```
Proposal / Guideline / Feedback / Version History
        ↓ Document Ingestion (DOCX/PDF → struktur + halaman + hash)
        ↓ Structured Extraction (LLM → JSON tervalidasi)
        ↓ Thesis Knowledge Graph (node + edge + provenance)
   ┌────┼──────────────┐
 LLM Reasoning  Constraint Engine  Retrieval
   └────┼──────────────┘
        ↓ Findings + Evidence + Confidence
        ↓ Human Confirmation Workflow
        ↓ Route Map / Action Plan / Decision Memory / Brief
```

## 2. Komponen

| Komponen | Tanggung jawab | Catatan desain |
|---|---|---|
| Ingestion | Parse DOCX/PDF; heading, paragraf, tabel, komentar, halaman; hash+versi | Simpan lokasi sumber per elemen; file di object storage |
| Redaction | Mask NIM, telepon, email, data peserta sebelum ke LLM | Pre-processor deterministik (regex) |
| Extractor | LLM → JSON `{element_type, content, source, status, confidence}` | Validasi skema; retry; tolak output tak valid |
| Graph store | Node/edge + status verifikasi + versi | Relational (PostgreSQL); Neo4j opsional |
| Constraint engine | Aturan alignment deterministik, configurable | LLM **tidak** memutuskan; hanya menjelaskan |
| Retrieval | pgvector di atas panduan, rubrik, feedback, literatur pengguna | Tanpa sumber → "memerlukan konfirmasi" |
| Feedback mapper | Feedback teks → node terdampak → aksi | Selalu tampilkan interpretasi + minta konfirmasi |
| Diff/impact | Bandingkan versi di level node; propagasi dampak | Aturan propagasi per tipe node |
| Confirmation | Status machine temuan | AI-suggested → Student-confirmed → Supervisor-confirmed / Rejected / Resolved |
| Brief generator | Ringkasan 1 halaman | Hanya merangkum state, tidak menulis konten penelitian |
| AuthZ/Audit | RBAC, consent gate, audit log | Pisahkan identitas dari isi penelitian |

## 3. Stack MVP (§9.3) — keputusan terbuka

| Layer | Opsi | Rekomendasi sementara* |
|---|---|---|
| Frontend | Next.js PWA / Flutter Web | Next.js (ekosistem visualisasi graph) |
| Backend | FastAPI / Node.js | FastAPI (ekosistem parser DOCX/PDF & AI) |
| DB | PostgreSQL | **SQLite dulu** (keputusan tim, 2026-11-24); PostgreSQL + pgvector saat butuh retrieval/produksi |
| Graph | Relational; Neo4j opsional | Relational dulu |
| Storage | S3-compatible | S3-compatible |
| Retrieval | pgvector / vector DB | pgvector |
| AI | LLM + structured JSON | Provider TBD (ADR-003) |
| Security | Enkripsi, RBAC, audit | Wajib |

\*Rekomendasi = saran penyusun dokumen, bukan keputusan proposal; finalkan via ADR di M0.

## 4. Status Temuan (state machine)

```
AI-suggested ──► Student-confirmed ──► Supervisor-confirmed ──► Resolved
      │                 │                      │
      └────────────────►└──────────────────────┴──► Rejected
```

## 5. Kontrak Data Kunci

**Extracted element**
```json
{
  "element_type": "research_question",
  "content": "Apakah X memengaruhi Y pada populasi Z?",
  "source": {"document": "proposal_v3", "page": 7},
  "status": "needs_user_confirmation",
  "confidence": 0.86
}
```

**Finding**
```json
{
  "id": "F-001",
  "rule_id": "R-CAUSAL-01",
  "priority": "high",
  "title": "Potential alignment issue",
  "why_flagged": "Desain mungkin hanya mengidentifikasi asosiasi, bukan dampak kausal.",
  "evidence": [{"element": "RQ1", "page": 5}, {"element": "Design", "page": 21}, {"element": "Analysis", "page": 29}],
  "suggested_clarification": "Diskusikan apakah RQ dirumuskan ulang sebagai asosiasi...",
  "confidence": 0.8,
  "status": "ai_suggested",
  "ai_generated": true
}
```

**Feedback action**
```json
{
  "original": "Metodenya coba diperjelas dan sesuaikan dengan tujuan kedua.",
  "interpretation": "Objective 2 dan research design mungkin belum selaras.",
  "affected": ["Objective 2", "Research design", "Data collection", "Analysis method"],
  "actions": ["Tentukan tipe Objective 2", "Tuliskan justifikasi desain", "Petakan Objective 2 ke data dan analisis"],
  "status": "waiting_student_confirmation"
}
```

## 6. Keamanan & Privasi (§12.2)

- Consent eksplisit sebelum upload; enkripsi transit/at-rest; RBAC; audit log.
- Redaction sebelum kirim ke LLM; kirim minimum konteks.
- Hapus permanen; retention policy; tidak ada training tanpa persetujuan terpisah.
- Pastikan kontrak penyedia LLM: tidak menyimpan/melatih dari data (**perlu diverifikasi**).

## 7. Strategi Evaluasi

Baseline (LLM-only "review consistency") vs Treatment (extraction + graph + constraint + retrieval). Metrik: precision, recall, evidence correctness, actionability, waktu (§11.3). Detail di [research-validation-plan.md](research-validation-plan.md).

## 8. Risiko Teknis

| Risiko | Mitigasi |
|---|---|
| Parser PDF salah halaman/struktur | Uji beragam format; fallback koreksi manual |
| LLM output tidak valid | Validasi skema + retry + konfirmasi pengguna |
| Halusinasi evidence | Evidence harus menunjuk elemen/halaman yang ada; verifikasi otomatis |
| Latensi/biaya LLM | Cache, batching, model lebih kecil untuk ekstraksi |
| API gagal saat demo | Data cache + rekaman (T10.4) |
