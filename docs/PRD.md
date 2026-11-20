# PRD — Product Requirements Document

**Produk:** ThesisTwin · **Versi:** 1.0 (draft) · **Tanggal:** 2026-11-20
**Sumber:** [source/01-proposal-full.md](source/01-proposal-full.md) · Turunan dari [BRD.md](BRD.md)

---

## 1. Ringkasan Produk

ThesisTwin adalah AI-powered navigation & consistency engine yang membuat *digital twin* perjalanan skripsi: model hidup berisi struktur penelitian, feedback, keputusan, dan milestone. Menjawab 4 pertanyaan: **Where am I? What is inconsistent? What changes if I revise this? What should I do next?** (§5.1)

**Prinsip produk (non-negotiable):**
1. Navigasi, bukan penulisan (tidak auto-write, tidak mengarang referensi).
2. Setiap temuan = pertanyaan/peringatan yang **dapat diverifikasi**, bukan vonis.
3. Setiap output punya **evidence** (dokumen + halaman) dan **confidence**.
4. **Human-in-the-loop**: AI-suggested ≠ persetujuan akademik.

## 2. Persona

| Persona | Deskripsi | Kebutuhan utama |
|---|---|---|
| **Nadia** (Mahasiswa) | S1 semester akhir, proposal Bab 1–3, 1–2 pembimbing | Tahu posisi & langkah berikut; paham feedback abstrak |
| **Pak/Bu Dosen** (Pembimbing) | Membimbing banyak mahasiswa paralel | Ringkasan perubahan & isu terbuka; tak baca ulang semua |
| **Peer mentor** (pendukung) | Asisten akademik | Melihat status untuk membantu |
| **Koordinator TA** (Fase 3) | Prodi | Bottleneck agregat tanpa lihat isi skripsi |

## 3. Cakupan Rilis

### MVP (STACK 2026) — in scope
Proposal Bab 1–3 · satu format panduan kampus · ekstraksi (RQ, objective, variable/concept, population, method, instrument, analysis) · visualisasi graph · 5–10 aturan alignment · input feedback manual/teks · feedback-to-action · change impact sederhana · bimbingan brief (§10.1).

### Out of scope
Auto-writing, statistik lanjutan, integrasi penuh LMS/SIAKAD, auto-kelayakan sidang, plagiarism sebagai fitur utama, fine-tuning besar (§10.2).

## 4. Functional Requirements

Prioritas: **M**ust / **S**hould / **C**ould. Rilis: **MVP** / **P1** (pasca-hackathon).

### 4.1 Onboarding & Project
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-001 | Autentikasi & peran (mahasiswa, dosen) | M | MVP |
| FR-002 | Buat project skripsi; pilih prodi; unggah/muat panduan kampus & milestone | M | MVP |
| FR-003 | Consent eksplisit sebelum upload dokumen | M | MVP |

### 4.2 Document Ingestion (§9.2A)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-010 | Unggah DOCX dan PDF (Bab 1–3) | M | MVP |
| FR-011 | Ekstrak heading, paragraf, tabel, komentar, nomor halaman | M | MVP |
| FR-012 | Simpan hash & versi dokumen | M | MVP |
| FR-013 | Pertahankan lokasi sumber (dokumen+halaman) tiap elemen | M | MVP |
| FR-014 | Redaction otomatis NIM, telepon, email, data peserta | S | MVP |

### 4.3 Structured Extraction (§9.2B)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-020 | LLM mengekstrak elemen riset ke JSON terstruktur (`element_type, content, source, status, confidence`) | M | MVP |
| FR-021 | Validasi skema output; retry/fallback bila invalid | M | MVP |
| FR-022 | Dukung bahasa Indonesia & campuran Indonesia–Inggris | M | MVP |

### 4.4 Thesis Knowledge Graph & Self-review (§5.2, §9.2C)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-030 | Bangun graph dengan tipe node & edge sesuai skema ([data-model.md](data-model.md)) | M | MVP |
| FR-031 | Visualisasi dependency graph interaktif (klik node → sumber, status, feedback) | M | MVP |
| FR-032 | Mahasiswa dapat menerima / menolak / mengedit hasil ekstraksi | M | MVP |

### 4.5 Alignment Checker & Constraint Engine (§6.2, §9.2D)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-040 | Jalankan 5–10 aturan alignment ([alignment-rules.md](alignment-rules.md)) | M | MVP |
| FR-041 | Tiap temuan: judul, prioritas, alasan, evidence (halaman), saran klarifikasi, confidence | M | MVP |
| FR-042 | Aturan configurable (data, bukan hard-coded) | S | MVP |
| FR-043 | Bahasa temuan berupa pertanyaan/peringatan, bukan vonis | M | MVP |

### 4.6 Retrieval (§9.2E)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-050 | Retrieval dibatasi: panduan kampus, rubrik prodi, feedback/catatan, literatur yang diunggah pengguna | M | MVP |
| FR-051 | Jika evidence tidak ada → tandai "memerlukan konfirmasi" | M | MVP |

### 4.7 Feedback-to-Action (§6.3)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-060 | Input feedback manual atau tempel teks (mis. dari WhatsApp) | M | MVP |
| FR-061 | Hasilkan: original, possible interpretation, affected components, proposed actions, status | M | MVP |
| FR-062 | Tampilkan interpretasi & minta konfirmasi mahasiswa | M | MVP |
| FR-063 | Upload feedback dari komentar DOCX | C | P1 |

### 4.8 Version Comparison & Change Impact (§6.4, §10.3)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-070 | Bandingkan versi proposal; tandai node berubah / isu terselesaikan / dampak baru | M | MVP |
| FR-071 | Change impact analysis sederhana saat node diubah (daftar bagian yang perlu dicek) | M | MVP |
| FR-072 | Tandai *unresolved dependency* (mis. abstrak masih "impact") | S | MVP |

### 4.9 Decision Memory (§6.5)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-080 | Catat keputusan: decision, reason, confirmed by, date, evidence, affected sections | S | MVP |
| FR-081 | Deteksi pengulangan isu antar-sesi | C | P1 |

### 4.10 Route Map (§6.1)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-090 | Dashboard: milestone, dependency selesai, current bottleneck, blocked tasks, next best action | M | MVP |

### 4.11 Bimbingan Brief (§6.6)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-100 | Generate ringkasan 1 halaman: perubahan, feedback selesai, keputusan butuh persetujuan, isu terbuka, pertanyaan, fokus pertemuan | M | MVP |
| FR-101 | Ekspor brief (PDF/Markdown) | S | MVP |

### 4.12 Human Confirmation & Supervisor Workspace (§9.2F, §7.2)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-110 | Status temuan: AI-suggested → Student-confirmed → Supervisor-confirmed / Rejected / Resolved | M | MVP |
| FR-111 | Dosen: lihat ringkasan, tandai temuan valid/tidak relevan, konfirmasi keputusan & action | M | MVP |
| FR-112 | Dashboard multi-mahasiswa bimbingan | S | P1 |
| FR-113 | Multi-supervisor conflict flag + pertanyaan klarifikasi | C | P1 |

### 4.13 Audit, Privasi, Keamanan (§12)
| ID | Requirement | Pri | Rilis |
|---|---|---|---|
| FR-120 | Semua saran AI berlabel "AI-generated" | M | MVP |
| FR-121 | Audit trail penggunaan & perubahan | M | MVP |
| FR-122 | Hapus permanen project/dokumen atas permintaan | S | MVP |
| FR-123 | Tidak ada pelatihan model pada dokumen tanpa persetujuan terpisah | M | MVP |

## 5. Non-Functional Requirements

| ID | Kategori | Requirement |
|---|---|---|
| NFR-01 | Keamanan | Enkripsi saat transit & tersimpan; RBAC; audit log (§9.3, §12.2) |
| NFR-02 | Privasi | Pisahkan data identitas dan isi penelitian; consent; retention policy |
| NFR-03 | Provenance | ≥90% temuan memiliki sumber valid (BO-4) |
| NFR-04 | Akurasi | Precision alignment ≥75% setelah konfirmasi (BO-3) — hipotesis |
| NFR-05 | Performa | Ekstraksi + graph proposal Bab 1–3 selesai dalam batas wajar untuk demo (target internal: < 3 menit; **perlu divalidasi**) |
| NFR-06 | Usability | SUS ≥70; task completion ≥80% |
| NFR-07 | Keterjelasan | Setiap peringatan menjelaskan *mengapa* muncul |
| NFR-08 | Portabilitas | Web/PWA, responsif untuk laptop & mobile |
| NFR-09 | Observabilitas | Log kualitas ekstraksi, latensi, error LLM |
| NFR-10 | Bahasa | UI Bahasa Indonesia (opsi Inggris menyusul) |

## 6. Guardrails Produk (§7.3, §12.1)

- Tidak menulis bab, tidak mengarang referensi, tidak menyatakan metodologi "pasti benar", tidak menggantikan persetujuan dosen, tidak mengirim apa pun tanpa aksi pengguna.
- Mekanisme: tidak ada fitur "generate paragraph"; prompt sistem melarang penulisan konten penelitian; Socratic prompt saat mahasiswa meminta jawaban langsung.

## 7. Arsitektur & Stack (ringkas)

Lihat [technical-design.md](technical-design.md). Stack MVP: Next.js PWA / Flutter Web · FastAPI / Node.js · PostgreSQL (+pgvector) · S3-compatible storage · LLM structured JSON (§9.3).

## 8. Metrik Produk

Lihat BRD §4 dan [research-validation-plan.md](research-validation-plan.md). Event analitik minimal: `proposal_uploaded`, `extraction_confirmed`, `finding_shown`, `finding_confirmed/rejected`, `feedback_converted`, `brief_generated`, waktu-ke-action-plan.

## 9. Open Questions

| # | Pertanyaan | Owner | Dampak |
|---|---|---|---|
| Q1 | Kampus/prodi sasaran & format panduan MVP mana? | Tim | Policy pack |
| Q2 | Frontend: Next.js vs Flutter Web? Backend: FastAPI vs Node? | Tim | Step-plan M0 |
| Q3 | LLM provider & anggaran token? | Tim | NFR-05, biaya |
| Q4 | Sumber dataset evaluasi: nyata (consent) atau sintetis? | Tim | Validasi |
| Q5 | Aturan alignment final disetujui dosen metodologi siapa? | Tim + dosen | Akurasi |
| Q6 | Neo4j perlu atau cukup relational graph? | Tim | Kompleksitas |

## 10. Traceability

Pemetaan FR ↔ BR ↔ UAT ada di [traceability-matrix.md](traceability-matrix.md).
