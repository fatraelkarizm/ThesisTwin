# Apakah ThesisTwin Hanya LLM Wrapper?

Jawaban tim (diskusi grup, 2026-11-24): **bukan, tetapi hanya untuk bagian yang benar-benar dibangun dengan kode.** Tabel di bawah memisahkan kerja kode kita dari kerja LLM, dan kolom **Status di repo** menunjukkan apa yang sudah ada per hari ini. Perbarui kolom itu setiap kali satu baris selesai.

## Yang kita bangun dan yang diserahkan ke LLM

| Komponen | Pelaku | Bisa ditiru dengan satu prompt? | Status di repo (2026-11-24) |
|---|---|---|---|
| Penyimpanan versi | Kode kita | Tidak, chat tidak persisten antarsesi | ✅ versi append-only + SHA-256 ([documents.py](../../apps/api/app/services/documents.py)) |
| Diff antarversi | Kode kita | Tidak persisten | ❌ Langkah 18 |
| Pelacakan "komentar dosen sudah ditindaklanjuti atau belum" | Kode kita (status) | Tidak, perlu keadaan jangka panjang | 🟡 komentar DOCX sudah terbaca ([docx.py](../../apps/api/app/parsing/docx.py)); status tindak lanjut belum (Langkah 19) |
| Aturan sebagai data, dengan tes positif dan negatif | Kode kita | Tidak, hasil LLM tidak terulang persis | ✅ 6 aturan YAML, contoh `fires`/`quiet` dites otomatis ([rules/](../../apps/api/rules/README.md)); belum ditinjau dosen |
| Verifikasi kutipan dan halaman sumber | Kode kita | Tidak, LLM sering mengarang rujukan | ✅ ([verification.py](../../apps/api/app/domain/verification.py)); baru diuji dengan LLM palsu, belum pada proposal nyata |
| Status konfirmasi mahasiswa → dosen, audit log | Kode kita | Tidak, itu catatan bersama | ✅ state machine + audit log ([status.py](../../apps/api/app/domain/status.py), [findings.py](../../apps/api/app/services/findings.py)) |
| Konfirmasi dosen **lewat tautan** (tanpa akun) | Kode kita | Tidak | ❌ Langkah 21; arah ini perlu dicatat sebagai keputusan 0.1 (ADR-005) |
| Parser `.tex` (teorema, `\label`, `\ref`, notasi) | Kode kita, tanpa LLM | Tidak perlu LLM | ❌ **baru**, Langkah 7b |
| Ekstraksi dari PDF/Word, penjelasan temuan, pertanyaan stress-test | **LLM** | Ya, di sinilah LLM berguna | ❌ menunggu provider (keputusan 0.3); pipeline dan validasinya sudah ada ([extraction.py](../../apps/api/app/services/extraction.py)) |

Ringkas: dari 9 baris, **4 sudah ada**, 1 sebagian, 4 belum. Dua baris yang paling sering dipakai untuk membantah tuduhan "wrapper", yaitu diff antarversi dan pelacakan komentar, **belum dibangun**.

## Hal yang harus diakui jujur

- **Satu proposal dengan prompt yang bagus bisa menemukan banyak masalah** yang juga ditemukan pipeline kita, mungkin dengan recall setara. **Jangan klaim keunggulan deteksi.** Uji pembanding ([comparison.md](comparison.md)) yang akan menjawabnya.
- **Keunggulan yang dipertahankan:** hasil konsisten (aturan bernama, bukan jawaban berubah-ubah), persisten antarversi, bukti yang dapat diperiksa, dan alur konfirmasi dosen.
- **Ini hanya benar jika dibangun.** Tuduhan wrapper valid untuk setiap baris yang statusnya masih ❌.

## Cara memakai di pitch

Tunjukkan baris yang ✅ beserta buktinya (tes, demo). Untuk baris ❌, katakan "direncanakan", jangan "sudah". Rujukan juri: P3 Value and Originality (−5) menyoroti pembanding yang lemah ([gap.md](gap.md) G2).
