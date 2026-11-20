# BRD — Business Requirements Document

**Produk:** ThesisTwin · **Versi:** 1.0 (draft) · **Tanggal:** 2026-11-20
**Sumber:** [source/01-proposal-full.md](source/01-proposal-full.md) (bagian dirujuk sebagai `§`)

---

## 1. Tujuan Bisnis

Mengurangi hambatan koordinasi, dokumentasi, dan konsistensi pada perjalanan skripsi mahasiswa S1 melalui "digital twin" perjalanan skripsi, tanpa menulis skripsi menggantikan mahasiswa (§1, §5).

Konteks kompetisi: **STACK 2026 — Case 1 "Smarter Campus and Learning"**. Tim harus menunjukkan user journey jelas, interaksi inti yang berjalan, dan manfaat terukur (§2).

## 2. Latar Masalah (ringkas)

| Masalah | Bukti di proposal |
|---|---|
| Struktur penelitian tidak terlihat, inkonsistensi ditemukan terlambat | §4.2 |
| Feedback pembimbing abstrak & tidak terstruktur | §4.2, §6.3 |
| Keputusan tidak tercatat → diskusi berulang | §4.2, §6.5 |
| Dampak perubahan tidak dianalisis → revisi berantai | §4.2, §6.4 |
| Konteks tersebar (file, WhatsApp, email, catatan) → *context reconstruction cost* | §3.2 |

**Catatan integritas data:** angka nasional (289.670 putus kuliah, +2,62%) **tidak boleh** dipakai sebagai klaim kausal bahwa skripsi penyebab putus kuliah (§3.3). Urgensi spesifik skripsi harus dibuktikan lewat riset pengguna.

## 3. Stakeholder

| Stakeholder | Peran | Kepentingan |
|---|---|---|
| Mahasiswa S1 tingkat akhir | Pengguna utama | Tahu posisi, langkah berikut, dampak revisi |
| Dosen pembimbing | Pengguna utama | Ringkasan perubahan & isu terbuka, tanpa baca ulang semua |
| Peer mentor / asisten akademik | Pendukung | Membantu mahasiswa menindaklanjuti feedback |
| Koordinator TA / Prodi | Pendukung (Fase 3) | Bottleneck agregat, SOP & template resmi |
| Layanan akademik kampus | Pendukung | Kepatuhan milestone/administrasi |
| Tim ThesisTwin | Pemilik produk | Menang/lolos tiap fase STACK, lalu pilot |
| Juri STACK 2026 | Evaluator | Demo jelas, klaim jujur, manfaat terukur |

## 4. Business Objectives & KPI

| ID | Objective | KPI | Target awal (hipotesis, bukan hasil) |
|---|---|---|---|
| BO-1 | Hemat waktu mahasiswa | Waktu membuat action plan | Turun ≥30% |
| BO-2 | Tindak lanjut feedback meningkat | % feedback → action item | ≥80% |
| BO-3 | Temuan akurat | Precision temuan alignment setelah konfirmasi | ≥75% |
| BO-4 | Temuan tertelusur | % temuan dengan sumber valid | ≥90% |
| BO-5 | Proses jelas | Task completion pada user test | ≥80% |
| BO-6 | Usability | System Usability Scale | ≥70 |
| BO-7 | Bimbingan lebih efektif | Proporsi isu yang diputuskan dalam satu sesi (H3) | Naik vs baseline |

Sumber: §11.4. Target **tidak boleh dipresentasikan sebagai hasil** sebelum diuji.

## 5. Scope Bisnis

**In scope (MVP STACK 2026):** proposal Bab 1–3, satu format panduan kampus, ekstraksi elemen riset, dependency graph, 5–10 aturan alignment, feedback-to-action, change impact sederhana, bimbingan brief (§10.1).

**Out of scope:** auto-writing bab, statistik lanjutan, integrasi penuh LMS/SIAKAD, keputusan kelayakan sidang otomatis, plagiarism detection sebagai fitur utama, fine-tuning model besar (§10.2).

## 6. Business Requirements

| ID | Requirement | Prioritas | Ref |
|---|---|---|---|
| BR-01 | Sistem membantu mahasiswa mengetahui posisi penelitian dan langkah berikutnya | Must | §5.1 |
| BR-02 | Sistem menemukan inkonsistensi antarbagian proposal dengan bukti sumber | Must | §6.2 |
| BR-03 | Feedback pembimbing diubah menjadi action items terstruktur | Must | §6.3 |
| BR-04 | Dampak perubahan terlihat sebelum menimbulkan kontradiksi | Must | §6.4 |
| BR-05 | Keputusan & alasannya tersimpan (decision memory) | Should | §6.5 |
| BR-06 | Dosen mendapat ringkasan pra-bimbingan | Must | §6.6 |
| BR-07 | Konflik antar-pembimbing ditandai tanpa memilih salah satu | Could | §6.7 |
| BR-08 | Seluruh output AI wajib bersumber dan berstatus konfirmasi manusia | Must | §9.2F, §12.1 |
| BR-09 | Sistem tidak menulis skripsi / mengarang referensi | Must | §7.3 |
| BR-10 | Privasi dokumen mahasiswa terlindungi (consent, enkripsi, RBAC, hapus permanen) | Must | §12.2 |
| BR-11 | Dapat didemokan end-to-end dalam waktu singkat | Must | §10.3 |
| BR-12 | Klaim angka dilaporkan jujur; data simulasi berlabel | Must | §3.3, §11.2 |

## 7. Asumsi, Batasan, Dependensi

**Asumsi**
- Mahasiswa bersedia mengunggah proposal DOCX/PDF.
- Dosen metodologi dapat membantu merumuskan aturan constraint.
- Tersedia akses LLM dengan structured JSON output.

**Batasan**
- MVP hanya Bab 1–3 dan satu format panduan kampus.
- Output = *decision support*, bukan penilaian final (§8.3).
- Timeline mengikuti fase STACK 2026 (§14).

**Dependensi**
- Handbook STACK 2026; panduan skripsi kampus sasaran; akses 15–30 mahasiswa, 3–5 dosen untuk riset (§11.1).

## 8. Model Bisnis & Keberlanjutan (§13.4)

- Lisensi institusi (prodi/fakultas).
- Versi mahasiswa gratis dengan batas jumlah proyek.
- Campus-hosted deployment untuk kebutuhan privasi tinggi.
- **Tidak** memonetisasi atau menjual isi skripsi.

## 9. Strategi Rollout (§13)

1. **Fase 1** Student-side pilot (tanpa integrasi kampus).
2. **Fase 2** Supervisor workspace (brief, konfirmasi keputusan, dashboard).
3. **Fase 3** Program-study integration (SOP, rubrik, agregat bottleneck tanpa ekspos isi).

## 10. Risiko Bisnis Utama

Lihat [risk-register.md](risk-register.md) untuk daftar lengkap. Ringkas: adopsi dosen rendah, salah nilai oleh AI, ketergantungan mahasiswa, kebocoran dokumen, variasi aturan antarkampus.

## 11. Kriteria Keberhasilan Proyek

- Demo end-to-end 8 langkah berjalan di Final Day (§10.3).
- Seluruh klaim di presentasi dapat ditelusuri ke bukti atau berlabel hipotesis/simulasi.
- Minimal 1 siklus user test dengan metrik BO-1..BO-6 tercatat jujur.
