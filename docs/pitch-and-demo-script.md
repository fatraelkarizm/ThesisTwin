# Pitch & Demo Script

**Versi:** 1.0 (draft) · Sumber: proposal §10.3, §15, §16, §17

## 1. Narasi Pitch (§17)

- **Problem hook:** "Mahasiswa tidak selalu terlambat skripsi karena tidak mampu menulis. Sering kali mereka tersesat di antara feedback, versi dokumen, dan keputusan yang saling bergantung."
- **Solution hook:** "ThesisTwin turns a thesis from a static document into a navigable research journey."
- **Differentiator:** "Unlike an AI writer, ThesisTwin maps the logic of a research project, remembers why decisions were made, and shows what must change when one decision changes."
- **Closing:** "We are not replacing supervisors or student thinking. We are removing the coordination and consistency barriers that prevent both from working effectively."

## 2. Struktur Deck (usulan, ±10 slide)

1. Hook masalah (tersesat, bukan tak mampu menulis)
2. Masalah & akar masalah (§4.2) — hanya fakta yang bisa dibuktikan; **jangan** klaim skripsi → putus kuliah
3. Bukti riset pengguna (hasil wawancara kita sendiri; berlabel n)
4. Solusi: digital twin perjalanan skripsi — 4 pertanyaan
5. Dependency graph
6. Demo (live)
7. Mengapa bukan AI writer: guardrail & human-in-the-loop
8. Hasil validasi (terukur vs hipotesis vs simulasi)
9. Positioning & moat (§15)
10. Rencana implementasi & keberlanjutan (§13–14) + penutup

## 3. Skrip Demo 8 Langkah (§10.3) — skenario Nadia (§16)

| # | Aksi | Yang ditunjukkan | Waktu |
|---|---|---|---|
| 1 | Upload proposal v1 | Parser + versi | 0:20 |
| 2 | Buka graph | Dependency graph terbentuk, klik node → sumber | 0:30 |
| 3 | Lihat 3 temuan | RQ "pengaruh" vs survei+korelasi (High); evidence hal. 5/21/29 | 0:40 |
| 4 | Tempel feedback: "Jangan terlalu berani menyimpulkan pengaruh…" | Input feedback | 0:20 |
| 5 | Action items | 5 aksi + interpretasi + minta konfirmasi | 0:30 |
| 6 | Upload v2 | Versi revisi | 0:15 |
| 7 | Perubahan & dampak | RQ/objective berubah; **abstrak masih "impact" → unresolved dependency** | 0:40 |
| 8 | Bimbingan brief | Ringkasan 1 halaman untuk dosen | 0:25 |

Total ≈ 3:20 (sesuaikan dengan batas waktu pitch).

## 4. Checklist Persiapan
- [ ] Data demo + skrip reset
- [ ] 3× run bersih berturut-turut
- [ ] Plan B: rekaman + data cache jika API gagal
- [ ] Semua angka berlabel (terukur / hipotesis / simulasi)
- [ ] Jawaban untuk "kenapa tidak ChatGPT?", "bagaimana jika AI salah?", "bagaimana privasi?", "apakah ini membantu mencontek?"

## 5. Q&A Siap Pakai

| Pertanyaan | Jawaban inti |
|---|---|
| Bedanya dengan ChatGPT? | Journey-aware: state longitudinal, graph, evidence, decision memory; bukan jawaban sekali pakai |
| Bagaimana jika AI salah? | Evidence+confidence, aturan deterministik, status konfirmasi; persetujuan hanya dosen |
| Apakah membantu mencontek? | Tidak menulis bab/referensi; mahasiswa harus menjelaskan keputusan; audit trail |
| Privasi? | Consent, enkripsi, RBAC, redaction, hapus permanen, tidak untuk training |
| Datamu dari mana? | Sebutkan jujur: wawancara nyata (n=?) atau data simulasi berlabel |
| Skalabilitas? | Policy pack per kampus; Fase 1→3 (§13) |
