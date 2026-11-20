# Risk Register, Privasi & Integritas Akademik

**Versi:** 1.0 (draft) · Sumber: proposal §12 (baris 1–6 dari proposal; sisanya usulan penyusun, ditandai ★)
Skala: Probabilitas (L/M/H) × Dampak (L/M/H).

## 1. Risiko

| ID | Risiko | P | D | Dampak | Mitigasi | Owner |
|---|---|---|---|---|---|---|
| R1 | AI salah menilai metode | M | H | Mahasiswa mengikuti saran keliru | Evidence, confidence, constraint, supervisor confirmation | Tim AI |
| R2 | Mahasiswa terlalu bergantung | M | M | Penurunan berpikir mandiri | Socratic prompts, larangan auto-writing | Produk |
| R3 | Feedback ambigu salah dipahami | H | M | Action item tidak sesuai | Tampilkan interpretasi, minta konfirmasi | Tim AI |
| R4 | Dokumen bocor | L | H | Kerugian akademik & privasi | Encryption, RBAC, retention policy | Tim Backend |
| R5 | Dosen merasa digantikan | M | H | Adopsi rendah | Positioning "preparation & memory layer"; dosen pegang approval | Produk |
| R6 | Aturan berbeda antarkampus | H | M | Temuan tidak relevan | Campus-specific policy pack | Produk |
| R7★ | Parser salah halaman/struktur | M | H | Evidence keliru, kepercayaan turun | Uji format beragam; koreksi manual | Tim Backend |
| R8★ | Biaya/latensi LLM tinggi | M | M | Demo lambat/mahal | Cache, model kecil untuk ekstraksi | Tim AI |
| R9★ | API LLM gagal saat demo | M | H | Demo gagal | Data cache + rekaman (Plan B) | Tim |
| R10★ | Dataset nyata tak tersedia | H | M | Validasi lemah | Dataset sintetis berlabel simulasi | Riset |
| R11★ | Klaim angka berlebihan | M | H | Pelanggaran aturan STACK/kredibilitas | Audit klaim (T10.5); label hasil/hipotesis/simulasi | Semua |
| R12★ | False positive tinggi | M | M | Kelelahan peringatan | Prioritas, ambang confidence, tuning dengan dosen | Tim AI |
| R13★ | Provider LLM menyimpan/melatih data | L | H | Pelanggaran privasi | Verifikasi kontrak; redaction; opsi self-host | Tim Backend |
| R14★ | Scope creep | H | M | MVP tak selesai | Pegang §10.2 out-of-scope; critical path | PM |

## 2. Prinsip Integritas Akademik (§12.1)
- Membantu navigasi, bukan menghasilkan karya untuk diserahkan.
- Semua saran berlabel AI-generated.
- Tidak ada referensi tanpa sumber.
- Mahasiswa tetap menjelaskan keputusan penelitian.
- Persetujuan metodologi hanya oleh dosen.
- Audit trail penggunaan & perubahan.

## 3. Kontrol Privasi Minimum (§12.2)
Consent eksplisit · enkripsi transit & at-rest · kontrol akses dokumen · pemisahan identitas vs isi · hapus permanen · tidak untuk training tanpa persetujuan terpisah · redaction NIM/telepon/email/data peserta.

## 4. Pemantauan
Tinjau register tiap akhir milestone (step-plan). Risiko dengan P×D = H×H atau M×H wajib punya tindakan aktif.
