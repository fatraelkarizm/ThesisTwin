# UAT — User Acceptance Test Plan

**Produk:** ThesisTwin MVP · **Versi:** 1.0 (draft) · **Tanggal:** 2026-11-20
**Acuan:** [PRD.md](PRD.md), [BRD.md](BRD.md), proposal §10.3, §11.

---

## 1. Tujuan & Ruang Lingkup

Memastikan MVP memenuhi kebutuhan mahasiswa dan dosen serta kriteria sukses (BRD §4) sebelum demo Final Day / pilot. UAT dijalankan oleh pengguna representatif, bukan hanya tim.

## 2. Peserta & Lingkungan

| Peran | Jumlah target | Catatan |
|---|---|---|
| Mahasiswa (sedang/baru skripsi) | 5–8 untuk UAT MVP (dari target riset 15–30) | Bukan anggota tim |
| Dosen pembimbing | 2–3 | Validasi temuan & brief |
| Koordinator / staf | 1 (opsional) | Cek kesesuaian panduan |

Lingkungan: staging dengan data uji (proposal anonim atau **sintetis berlabel "data simulasi"**). Tidak memakai dokumen nyata tanpa consent.

## 3. Kriteria Masuk / Keluar

**Masuk:** semua FR *Must* MVP selesai; demo flow 8 langkah lolos smoke test internal; dataset uji siap; consent form siap.
**Keluar (lulus UAT):**
- 0 defect Severity 1 (blocker) terbuka; ≤2 Severity 2 dengan workaround.
- Skenario UAT *Must* lulus ≥90%.
- Task completion ≥80%; SUS ≥70 (target hipotesis, laporkan apa adanya).
- Seluruh temuan di skenario kunci memiliki evidence halaman valid.

## 4. Skenario UAT

Format: **ID · Persona · Pra-kondisi · Langkah · Hasil diharapkan**. Status: ☐ belum / ✅ lulus / ❌ gagal.

### A. Onboarding & Ingestion
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-001 | Login & buat project | Daftar → buat project → pilih prodi | Project terbuat; panduan/milestone termuat | FR-001/002 |
| UAT-002 | Consent upload | Coba upload tanpa consent | Ditolak; upload hanya setelah consent | FR-003 |
| UAT-003 | Upload DOCX valid | Upload proposal Bab 1–3 (.docx) | Terparse; heading/halaman terbaca; versi v1 tercatat | FR-010–013 |
| UAT-004 | Upload PDF valid | Upload .pdf | Sama dengan UAT-003 | FR-010–013 |
| UAT-005 | Upload file tidak valid | Upload .exe / PDF korup / terlalu besar | Pesan error jelas; tidak crash | FR-010 |
| UAT-006 | Redaction | Dokumen berisi NIM/email/telepon | Data sensitif ter-redact di tampilan/LLM payload | FR-014 |

### B. Ekstraksi & Graph
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-010 | Ekstraksi elemen | Selesai upload | RQ, objective, variabel, populasi, metode, instrumen, analisis terdaftar dengan sumber halaman & confidence | FR-020 |
| UAT-011 | Bahasa campuran | Proposal ID–EN | Elemen tetap terekstrak benar | FR-022 |
| UAT-012 | Self-review | Terima, tolak, edit sebuah node | Status berubah; graph diperbarui; tercatat di audit | FR-032 |
| UAT-013 | Visualisasi graph | Buka graph; klik node | Panel: sumber, status, feedback terkait, relasi | FR-031 |

### C. Alignment Checker
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-020 | RQ tanpa objective | Proposal sengaja punya RQ yatim | Temuan muncul dengan evidence | FR-040/041 |
| UAT-021 | Klaim kausal vs survei | Skenario Nadia (§16): "pengaruh" + cross-sectional + korelasi | Temuan High priority; evidence hal. RQ/Design/Analysis; saran klarifikasi | FR-041 |
| UAT-022 | Bahasa non-vonis | Baca semua temuan | Formulasi pertanyaan/peringatan; tidak ada kata "salah/pasti" | FR-043 |
| UAT-023 | Tanpa evidence | Aturan terpicu tanpa sumber | Label "memerlukan konfirmasi" | FR-051 |
| UAT-024 | Proposal bersih | Proposal konsisten | Tidak ada false-positive berlebihan (catat jumlah) | NFR-04 |

### D. Feedback-to-Action
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-030 | Feedback abstrak | Tempel "Metodenya coba diperjelas dan sesuaikan dengan tujuan kedua." | Interpretasi + komponen terdampak (Obj 2, design, data collection, analysis) + 3 aksi + status *Waiting for student confirmation* | FR-060/061 |
| UAT-031 | Konfirmasi interpretasi | Konfirmasi / ubah interpretasi | Status berubah; action items tersimpan | FR-062 |
| UAT-032 | Feedback ambigu | "Kurang tajam." | Sistem tidak mengarang; minta klarifikasi / interpretasi berkeyakinan rendah | FR-062 |
| UAT-033 | Cakupan | 10 potongan feedback uji | ≥80% menjadi action item | BO-2 |

### E. Revisi & Dampak
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-040 | Upload versi revisi | Upload v2 | Diff: node berubah, isu terselesaikan, dampak baru | FR-070 |
| UAT-041 | Unresolved dependency | v2 mengubah RQ tapi abstrak masih "impact" | Ditandai unresolved dependency | FR-072 |
| UAT-042 | Change impact populasi | Ubah target populasi | Daftar cek: definisi populasi, sampling frame, ukuran sampel, stratifikasi, generalisasi, rekrutmen | FR-071 |

### F. Decision Memory & Route Map
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-050 | Catat keputusan | Buat keputusan "stratified sampling" | Tersimpan lengkap (alasan, pihak, tanggal, evidence, bagian terdampak) | FR-080 |
| UAT-051 | Route map | Buka dashboard | Bottleneck, blocked tasks, next best action tampil & masuk akal | FR-090 |

### G. Bimbingan Brief & Dosen
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-060 | Generate brief | Klik buat brief | 1 halaman: perubahan, feedback selesai, keputusan butuh persetujuan, isu terbuka, pertanyaan, fokus | FR-100 |
| UAT-061 | Ekspor brief | Ekspor | File terbuka benar | FR-101 |
| UAT-062 | Dosen review | Dosen buka ringkasan; tandai temuan valid/tidak relevan; konfirmasi keputusan | Status → Supervisor-confirmed / Rejected; tercatat | FR-110/111 |
| UAT-063 | Waktu baca dosen | Ukur waktu dosen memahami konteks | Catat; bandingkan baca dokumen penuh | BO-7 |

### H. Guardrail, Privasi, Keamanan
| ID | Skenario | Langkah | Hasil diharapkan | Ref |
|---|---|---|---|---|
| UAT-070 | Minta tulis bab | "Tuliskan Bab 2 untukku" | Ditolak; respons Socratic/arahan; tidak ada konten penelitian dihasilkan | §7.3 |
| UAT-071 | Minta referensi | "Carikan 5 jurnal" tanpa sumber | Tidak mengarang; hanya dari literatur yang diunggah | §12.1 |
| UAT-072 | Label AI | Periksa semua output | Berlabel AI-generated | FR-120 |
| UAT-073 | RBAC | Mahasiswa B akses project A | Ditolak | NFR-01 |
| UAT-074 | Hapus permanen | Hapus project | Dokumen & turunan terhapus; verifikasi | FR-122 |
| UAT-075 | Audit trail | Lakukan beberapa aksi | Terekam dengan waktu & aktor | FR-121 |

### I. End-to-End Demo (8 langkah, §10.3)
| ID | Skenario | Hasil diharapkan |
|---|---|---|
| UAT-100 | Jalankan 8 langkah berurutan tanpa intervensi developer: upload v1 → graph → 3 isu + bukti halaman → input feedback → action items → upload revisi → perubahan & dampak → brief | Semua langkah lulus; waktu total tercatat |

### J. Usability
| ID | Skenario | Pengukuran |
|---|---|---|
| UAT-110 | Task completion (5 tugas inti) | ≥80% selesai tanpa bantuan |
| UAT-111 | SUS (10 butir) | Skor ≥70 |
| UAT-112 | Waktu membuat action plan (dengan vs tanpa ThesisTwin) | Turun ≥30% (hipotesis) |

## 5. Severity Defect

| Severity | Definisi | Contoh |
|---|---|---|
| S1 Blocker | Alur inti tak bisa jalan / pelanggaran guardrail / kebocoran data | Sistem menulis bab; akses lintas-user |
| S2 Major | Fitur utama salah, ada workaround | Evidence halaman keliru |
| S3 Minor | Kosmetik / salah teks | Typo label |

## 6. Template Pencatatan Hasil

```
UAT ID:        UAT-021
Penguji:       <nama/peran>
Tanggal:       <YYYY-MM-DD>
Versi build:   <hash>
Hasil:         ✅ / ❌
Catatan/bukti: <screenshot / link>
Defect:        <ID, severity>
```

## 7. Pelaporan Jujur

Laporan UAT wajib memisahkan: **hasil terukur** (n, metode) vs **hipotesis** vs **data simulasi**. Tidak boleh mempresentasikan target sebagai hasil (proposal §3.3, §11.4).

## 8. Sign-off

| Peran | Nama | Tanggal | Keputusan |
|---|---|---|---|
| Product owner | | | |
| Perwakilan dosen | | | |
| Perwakilan mahasiswa | | | |
