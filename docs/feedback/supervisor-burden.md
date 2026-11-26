# Audit Beban Dosen

Asal: notulensi rapat 2026-11-24, "cek kebutuhan dosen dan apakah memberatkan atau tidak dari app-nya".

Dokumen ini memisahkan **apa yang diminta aplikasi dari dosen saat ini** (fakta dari kode) dari **apa yang perlu ditanyakan ke dosen** (belum ada datanya). Belum ada angka waktu atau kepuasan dosen yang terukur; jangan dikutip sebagai hasil.

## 1. Yang diminta dari dosen saat ini (per kode, 2026-11-24)

| Langkah | Wajib? | Sumber |
|---|---|---|
| Membuka tautan dari mahasiswa, tanpa akun dan tanpa login | Ya, satu-satunya langkah wajib | `/dosen/[token]`; tautan berlaku 14 hari (`DEFAULT_DAYS` di [share.py](../../apps/api/app/services/share.py)) |
| Membaca ringkasan: perubahan, dampak, status komentar, temuan terbuka | Tidak (bisa juga dicetak) | [SupervisorBrief.tsx](../../apps/web/src/components/features/supervisor/SupervisorBrief.tsx) |
| Setuju/tidak setuju pada temuan yang menunggu dosen | Tidak; tanpa keputusan, status tetap "menunggu" | `POST /share/{token}/findings/{id}` |
| Memberi nilai 1–5 pada pertanyaan stress-test | Tidak | `POST /share/{token}/stress-questions/{id}/rating` |

Tidak ada notifikasi, email, tenggat, atau kewajiban mengisi apa pun dari sisi aplikasi. Guardrail 9 (dosen tanpa akun) terpenuhi.

## 2. Titik yang berpotensi memberatkan (hipotesis tim, belum diuji)

1. ~~**Keputusan temuan tanpa konteks.**~~ **Ditangani 2026-11-26:** kartu "menunggu dosen" kini memuat alasan, bukti (elemen + halaman/bagian), landasan beserta asal sumbernya; teks brief untuk chat ikut mencantumkan halaman. Apakah ini *cukup* untuk memutuskan tanpa membuka dokumen masih perlu dicek ke dosen (pertanyaan no. 9).
2. **Panjang ringkasan tidak dibatasi.** Proposal dengan banyak temuan menghasilkan daftar panjang. Belum ada batas atau urutan "3 hal terpenting".
3. **Tautan kedaluwarsa 14 hari.** Bila dosen membuka setelah itu, mahasiswa harus membuat tautan baru. Belum diketahui apakah ini mengganggu.
4. **Istilah aturan** (mis. `R-CAUSAL-01`) mungkin tidak bermakna bagi dosen.

## 3. Pertanyaan untuk dosen

Sudah ditambahkan ke [interview-guide.md](evidence/interview-guide.md) bagian Dosen pembimbing (no. 6–10). Hasilnya dicatat di [interview-log.md](evidence/interview-log.md), lalu tabel §2 diperbarui: hipotesis yang terbukti diberi rujukan ID responden, yang tidak terbukti dicoret.

## 4. Yang diukur saat UAT

- UAT-063: waktu dosen memahami konteks dari brief vs membaca dokumen penuh.
- Tambahan: berapa temuan yang diputuskan dosen tanpa membuka dokumen, dan berapa yang dilewati.
