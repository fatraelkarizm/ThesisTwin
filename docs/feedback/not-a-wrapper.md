# Apakah ThesisTwin Hanya LLM Wrapper?

Jawaban tim (diskusi grup, 2026-11-24): **bukan, tetapi hanya untuk bagian yang benar-benar dibangun dengan kode.** Tabel di bawah memisahkan kerja kode kita dari kerja LLM, dan kolom **Status di repo** menunjukkan apa yang sudah ada per hari ini. Perbarui kolom itu setiap kali satu baris selesai.

## Yang kita bangun dan yang diserahkan ke LLM

| Komponen | Pelaku | Bisa ditiru dengan satu prompt? | Status di repo (2026-11-24) |
|---|---|---|---|
| Penyimpanan versi | Kode kita | Tidak, chat tidak persisten antarsesi | ✅ versi append-only + SHA-256 ([documents.py](../../apps/api/app/services/documents.py)) |
| Diff antarversi | Kode kita | Tidak persisten | ✅ diff per elemen ([diff.py](../../apps/api/app/domain/diff.py)); RQ yang ditulis ulang tercatat "diubah" |
| Pelacakan "komentar dosen sudah ditindaklanjuti atau belum" | Kode kita (status) | Tidak, perlu keadaan jangka panjang | ✅ komentar DOCX → "kemungkinan ditangani" bila teks yang dikomentari berubah, lalu dikonfirmasi mahasiswa ([comments.py](../../apps/api/app/domain/comments.py)) |
| Aturan sebagai data, dengan tes positif dan negatif | Kode kita | Tidak, hasil LLM tidak terulang persis | ✅ 6 aturan YAML, contoh `fires`/`quiet` dites otomatis ([rules/](../../apps/api/rules/README.md)); belum ditinjau dosen |
| Verifikasi kutipan dan halaman sumber | Kode kita | Tidak, LLM sering mengarang rujukan | ✅ ([verification.py](../../apps/api/app/domain/verification.py)); baru diuji dengan LLM palsu, belum pada proposal nyata |
| Status konfirmasi mahasiswa → dosen, audit log | Kode kita | Tidak, itu catatan bersama | ✅ state machine + audit log ([status.py](../../apps/api/app/domain/status.py), [findings.py](../../apps/api/app/services/findings.py)) |
| Konfirmasi dosen **lewat tautan** (tanpa akun) | Kode kita | Tidak | ✅ tautan bertoken (hanya hash disimpan, kedaluwarsa 14 hari, terbatas satu proyek, keputusan masuk audit log) ([share.py](../../apps/api/app/services/share.py)); halaman `/dosen/[token]`. Keputusan 0.1 tetap perlu ADR-005 |
| Parser `.tex` (teorema, `\label`, `\ref`, notasi) | Kode kita, tanpa LLM | Tidak perlu LLM | ✅ bagian, lingkungan teorema, `\label`/`\ref` (termasuk rujukan rusak), makro ([tex.py](../../apps/api/app/parsing/tex.py)) |
| Pemilihan tautan terlemah + pertanyaan Defense Stress-Test | Kode kita (templat) | Tidak, perlu graph + status temuan | ✅ ([stress.py](../../apps/api/app/domain/stress.py)); rating dosen 1–5 lewat tautan |
| Ekstraksi dari PDF/Word, penjelasan temuan, memperhalus bahasa pertanyaan stress-test | **LLM** | Ya, di sinilah LLM berguna | ❌ menunggu provider (keputusan 0.3); pipeline dan validasinya sudah ada ([extraction.py](../../apps/api/app/services/extraction.py)). Sementara itu mahasiswa memasukkan elemen sendiri dan **tetap diverifikasi** terhadap dokumen |

Ringkas (diperbarui 2026-11-24): dari 9 baris, **8 sudah ada di kode dan dites** (86 tes API, termasuk satu tes alur penuh), 1 menunggu provider LLM. Alur end-to-end berjalan **tanpa LLM**: unggah → elemen (dimasukkan mahasiswa, diverifikasi) → cek aturan → konfirmasi → versi baru → diff + komentar → brief → tautan dosen → keputusan dosen.

**Yang belum diuji:** semua ini baru dicoba dengan data sintetis berlabel, bukan proposal mahasiswa nyata.

## Hal yang harus diakui jujur

- **Satu proposal dengan prompt yang bagus bisa menemukan banyak masalah** yang juga ditemukan pipeline kita, mungkin dengan recall setara. **Jangan klaim keunggulan deteksi.** Uji pembanding ([comparison.md](comparison.md)) yang akan menjawabnya.
- **Keunggulan yang dipertahankan:** hasil konsisten (aturan bernama, bukan jawaban berubah-ubah), persisten antarversi, bukti yang dapat diperiksa, dan alur konfirmasi dosen.
- **Ini hanya benar jika dibangun.** Tuduhan wrapper valid untuk setiap baris yang statusnya masih ❌.

## Cara memakai di pitch

Tunjukkan baris yang ✅ beserta buktinya (tes, demo). Untuk baris ❌, katakan "direncanakan", jangan "sudah". Rujukan juri: P3 Value and Originality (−5) menyoroti pembanding yang lemah ([gap.md](gap.md) G2).
