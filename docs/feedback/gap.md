# Gap — Kritik Juri vs Isi Repo

Dibuat dari analisis di [critique-vs-repo-1.png](images/critique-vs-repo-1.png) dan [critique-vs-repo-2.png](images/critique-vs-repo-2.png), dicek ulang terhadap isi repo per 2026-11-24. Skor juri: [features.md](features.md).

Legenda status: ❌ belum sama sekali · 🟡 sebagian · ✅ terjawab.

## 0. Status penutupan (diperbarui 2026-11-24)

| Gap | Status | Yang sudah dikerjakan | Yang masih butuh tim |
|---|---|---|---|
| G1 Bukti kecil (−6) | 🟡 alat siap, **data belum** | [evidence/](evidence/README.md): panduan wawancara, consent, log anonim, catatan literatur | **Isi log dari wawancara nyata**; tambah responden (target 15–30 mahasiswa, 3–5 dosen); baca ref [5]. Tidak bisa dikerjakan dengan kode |
| G2 Pembanding (−5) | 🟡 desain siap, **uji belum jalan** | [comparison.md](comparison.md): pembanding praktik nyata + rancangan uji 3 lengan | Jalankan uji T1–T3; validasi kolom "batasan" lewat wawancara |
| G3 Mitigasi ekstraksi (−3) | ✅ **dibangun & dites** (30 tes) | Verifikasi halaman + kutipan, redaction, retry skema, parser PDF, metrik | Belum diuji pada proposal nyata; persamaan/DOCX belum ditangani |
| R1 Tanggal milestone | 🟡 | Tabel bertanggal di README; 30 Nov terisi | Isi tanggal resmi STACK (`TODO`) |
| R2 Scope melebar | ✅ | README memusatkan version record + brief | — |
| R3 Judul lama | ❌ | — | **Teks abstrak/judul baru dibutuhkan** |
| R4 Metrik berbeda | ✅ | README memuat 50% waktu review (abstrak) dan 30% action plan | Tim putuskan satu metrik utama |
| R5 Stress-Test, Matematika | 🟡 | Matematika dan Stress-Test disebut di README | **Spesifikasi Defense Stress-Test** dari tim |
| R6 Identitas tim | ❌ | — | Nama tim, anggota, kontribusi, deklarasi (ditandatangani) |

## 1. Kritik juri

| # | Kritik juri | Kriteria | Status | Isi di repo | Yang masih kurang | Jenis kerja |
|---|---|---|---|---|---|---|
| G1 | Bukti masih kecil | P1 (−6) | 🟡 | Bagian "Supporting evidence" di README hanya memuat angka 289.670 mahasiswa putus kuliah, yang README sendiri akui **tidak** membuktikan skripsi sebagai penyebab. Data skripsi disebut "to be collected". | Wawancara 7+1 dan literatur [2]–[5] dari abstrak tidak muncul. Tidak ada survei, catatan wawancara, atau dosen tambahan. | **Kerja lapangan**, bukan kode |
| G2 | Pembanding hanya chatbot umum | P3 (−5) | 🟡 bentuk saja | Tabel alternatif naik dari 1 jadi 5 kategori: chatbot, grammar checker, reference manager, task manager, LMS. | Isinya salinan proposal lama. Praktik sehari-hari (komentar dan riwayat versi Word/Google Docs, WhatsApp, kartu bimbingan) dan chatbot dengan memori proyek belum ada. Tidak ada pengujian pembanding. | Riset + uji pembanding |
| G3 | Mitigasi kesalahan ekstraksi belum detail | P4 (−3) | 🟡 prinsip saja | LLM tidak memutuskan alignment; output divalidasi lalu diulang terbatas; redaction sebelum LLM; evidence invariant ([evidence.py](../../apps/api/app/domain/evidence.py)). | Evidence invariant hanya memeriksa bahwa ada dokumen dan halaman. **Kutipan dan keberadaan halaman tidak diverifikasi.** Cara mengukur akurasi ekstraksi, penanganan persamaan, dan pemetaan halaman PDF belum ada. Kode ekstraksinya sendiri belum ada. | Desain + kode + pengukuran |

## 2. Yang justru mundur (regresi README)

| # | Masalah | Detail | Perbaikan |
|---|---|---|---|
| R1 | **Tonggak bertanggal hilang** | Juri memuji tonggak bertanggal, tetapi tabel milestone README hanya berisi fase tanpa tanggal. | Tambahkan tanggal ke tabel Development Plan (acuan: [step-plan.md](../step-plan.md), tanggal STACK resmi) |
| R2 | **Scope melebar** | Juri memuji pembeda "rekam versi dan brief", tetapi README memperkenalkan enam fitur sekaligus, termasuk Route Map dan Decision Memory. | Pakai fokus fitur di [features.md](features.md) |
| R3 | **Judul versi lama** | README masih "Navigation and Consistency Engine…". | Samakan dengan judul di abstrak (salin teks abstrak ke repo dulu) |
| R4 | **Target metrik berbeda** | README: 30% waktu action plan. Abstrak: 50% waktu review. | Samakan satu angka; label sebagai hipotesis |
| R5 | **Defense Stress-Test dan prodi Matematika tidak disebut** | Ada di abstrak, tidak ada di repo. | Definisikan fitur dan prodi target |
| R6 | **Identitas tim kosong** | Nama tim, anggota, kontribusi, deklarasi masih `TODO`. | Isi oleh tim; deklarasi harus ditandatangani |

## 3. Janji abstrak yang belum terpenuhi

README sendiri mencatat ingestion, ekstraksi LLM, graph, constraint engine, dan feedback mapping **belum dibangun**. Janji ekstraksi 10 proposal per **30 Nov** (6 hari dari 24 Nov) belum tercapai.

Yang ada di kode sekarang: state machine status, evidence invariant (hanya cek keberadaan), tabel SQLite untuk finding/evidence/audit log, dan komponen UI dengan data simulasi.

## 4. Rencana penutupan gap (usulan ★)

Urutan berdasarkan poin yang bisa direbut per usaha.

| Prioritas | Aksi | Menutup | Catatan |
|---|---|---|---|
| 1 | Rapikan README: tanggal milestone, fokus fitur, judul dan metrik sesuai abstrak, prodi target | R1–R5 | Murah, hanya dokumen. Salin teks abstrak ke repo lebih dulu |
| 2 | Kumpulkan bukti lapangan: catatan wawancara 7+1, tambah responden dan dosen, tautkan literatur [2]–[5] | G1 (−6) | Gap terbesar; tidak bisa diselesaikan dengan kode. Data anonim + consent |
| 3 | Tulis perbandingan praktik nyata: riwayat versi Docs/Word, komentar, WhatsApp, kartu bimbingan, chatbot ber-memori. Rancang uji pembanding kecil | G2 (−5) | Pembanding harus yang benar-benar dipakai mahasiswa |
| 4 | Tulis spesifikasi mitigasi ekstraksi (lihat §5) lalu bangun ingestion + ekstraksi | G3 (−3), §3 | Mulai dari verifikasi kutipan dan halaman |
| 5 | Isi identitas tim dan deklarasi orisinalitas | R6 | Dikerjakan tim |

## 5. Rancangan mitigasi kesalahan ekstraksi (draf ★)

Untuk menjawab G3. Semua poin di bawah adalah **usulan**; belum diimplementasikan.

| Risiko ekstraksi | Mitigasi yang dirancang | Cara mengukur |
|---|---|---|
| Halaman sumber salah / PDF bergeser | Simpan nomor halaman dari parser, bukan dari LLM; verifikasi halaman ada di dokumen | % elemen dengan halaman benar pada sampel berlabel |
| Kutipan tidak ada di dokumen (halusinasi) | Wajibkan `quote`; cek `quote` muncul pada teks halaman (fuzzy match) sebelum diterima; gagal → `needs_user_confirmation` | % kutipan yang lolos pencocokan |
| Persamaan / simbol rusak | Tandai blok non-teks; jangan diekstrak oleh LLM; minta konfirmasi pengguna | Jumlah blok ditandai vs ditangani manual |
| Output JSON tidak valid | Validasi Pydantic, retry terbatas, lalu fallback konfirmasi pengguna | Tingkat retry dan kegagalan |
| Bahasa campuran ID–EN | Uji pada set berlabel campuran | Akurasi per bahasa |
| Akurasi keseluruhan tidak diketahui | Set emas berlabel ≥2 evaluator; ukur precision/recall per tipe elemen ([research-validation-plan.md](../research-validation-plan.md) §11.3) | Precision/recall per `element_type` |

Gap pada kode saat ini: [evidence.py](../../apps/api/app/domain/evidence.py) baru memeriksa bahwa daftar evidence tidak kosong. Verifikasi `quote` dan keberadaan halaman belum ada.
