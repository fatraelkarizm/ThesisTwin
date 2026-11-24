# Comparison — Pembanding Praktik Nyata (menjawab G2)

Juri: *"cuma dibandingkan dengan chatbot umum"*. Dokumen ini memperluas pembanding ke **apa yang benar-benar dipakai mahasiswa dan dosen**, dan merancang uji pembandingnya.

> **Status klaim.** Kolom "kelebihan" memuat kemampuan umum yang diketahui dari produk tersebut. Kolom "batasan" dan semua klaim keunggulan ThesisTwin adalah **hipotesis desain**, bukan hasil. Keduanya harus diuji lewat §3 dan wawancara ([evidence/](evidence/README.md)). Jangan dipresentasikan sebagai hasil sebelum diuji.

## 1. Praktik sehari-hari yang menggantikan ThesisTwin hari ini

| Praktik | Dipakai untuk | Kelebihan | Batasan yang diduga (hipotesis) | Diuji di |
|---|---|---|---|---|
| **Word: track changes, komentar, *Compare documents*** | Revisi, feedback tertulis dosen | Sudah dikenal semua orang; diff tingkat teks; komentar menempel di lokasi | Diff berbasis teks, bukan berbasis elemen penelitian: tidak tahu bahwa perubahan populasi berdampak ke sampling | T2 |
| **Google Docs: riwayat versi + komentar** | Revisi kolaboratif | Riwayat otomatis, berbagi mudah | Sama; riwayat tidak menyimpan *alasan* keputusan | T2 |
| **WhatsApp / email dosen** | Feedback lisan/singkat | Cepat, selalu ada | Tidak terstruktur, tidak terhubung ke bagian dokumen, mudah hilang | T3 |
| **Kartu / form bimbingan kampus** | Catatan resmi sesi | Diwajibkan, ada tanda tangan | Ringkas dan administratif; tidak menautkan isu ke bagian proposal | T3 |
| **Catatan pribadi mahasiswa** | Mengingat arahan | Fleksibel | Tidak terbagi dengan dosen, tidak ada pelacakan status | T3 |
| **Chatbot umum** (tanpa memori proyek) | Tanya jawab, review cepat | Fleksibel, cepat | Konteks harus ditempel ulang tiap sesi | T1 |
| **Chatbot dengan memori/proyek** (fitur "Projects" pada chatbot populer) | Review berkelanjutan dalam satu proyek | Menyimpan dokumen dan percakapan dalam satu ruang | Penilaian oleh LLM tanpa aturan deterministik; tanpa verifikasi kutipan/halaman; tanpa status konfirmasi mahasiswa/dosen | T1, T2 |
| **Grammar checker, reference manager, task manager, LMS/SIAKAD** | Bahasa, sitasi, tugas, milestone | Matang di bidangnya | Tidak memahami keterkaitan metodologis (kategori dari proposal §15) | — (di luar uji) |

**Pembanding terkuat** yang harus dikalahkan: *Word/Docs Compare + chatbot dengan memori proyek*, karena itulah gabungan yang paling mungkin dipakai mahasiswa yang cerdas. Chatbot tanpa memori adalah pembanding yang terlalu mudah.

## 2. Pembeda yang diklaim (yang dipuji juri)

| Pembeda | Pembanding terdekat | Yang membuatnya berbeda *secara desain* |
|---|---|---|
| **Rekam versi di level elemen penelitian** | Word Compare / riwayat Docs | Diff per node (RQ, objective, variabel…), bukan per teks; propagasi dampak antar node |
| **Brief supervisor** | Kartu bimbingan, ringkasan chatbot | Dibuat dari state terstruktur (perubahan, isu terbuka, keputusan butuh persetujuan), bukan dari teks bebas |
| **Evidence terverifikasi** | Chatbot dengan memori | Tiap temuan menunjuk halaman, dan kutipannya dicek terhadap teks halaman ([verification.py](../../apps/api/app/domain/verification.py)) |
| **Konfirmasi manusia berjenjang** | Semua | State machine mahasiswa → dosen; hanya dosen yang dapat `supervisor_confirmed` |

## 3. Rancangan uji pembanding (belum dijalankan)

Tiga lengan, data sama, penilai tidak tahu lengan mana (blind) bila memungkinkan.

| Lengan | Perlakuan |
|---|---|
| **A: Praktik manual** | Word/Docs Compare + komentar; pengguna bekerja tanpa AI |
| **B: Chatbot ber-memori** | Proposal diunggah ke proyek chatbot; prompt standar yang sama untuk semua partisipan |
| **C: ThesisTwin** | Pipeline lengkap (ekstraksi → graph → constraint → verifikasi) |

| Tugas | Isi | Metrik |
|---|---|---|
| **T1 Temukan inkonsistensi** | Proposal v1 dengan inkonsistensi yang sudah **ditanam** dan dilabeli ≥2 evaluator | Precision, recall, *evidence correctness* (halaman + kutipan benar), waktu |
| **T2 Dampak revisi** | Pasangan v1→v2: daftar perubahan, isu yang selesai, dampak baru | Recall perubahan, ketepatan dampak, waktu |
| **T3 Brief bimbingan** | Buat ringkasan satu halaman untuk sesi berikutnya | Kelengkapan (daftar periksa), skor dosen 1–5, waktu |

**Data.** Proposal asli anonim bila ada izin; bila tidak, set sintetis. **Set sintetis wajib berlabel "data simulasi"** (aturan STACK dan [AGENTS.md](../../AGENTS.md) §3.9).

**Cara membaca hasil.** Laporkan apa adanya, termasuk bila lengan A atau B menang pada tugas tertentu. Perbandingan yang hanya memilih tugas yang menguntungkan tidak akan dipercaya juri.

**Alat ukur di kode.** [metrics.py](../../apps/api/app/domain/metrics.py) menghitung precision/recall per tipe elemen dan *evidence correctness*.
