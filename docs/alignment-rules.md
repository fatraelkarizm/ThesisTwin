# Katalog Aturan Alignment (MVP)

**Versi:** 1.0 (draft) · Sumber: proposal §6.2, §9.2D · MVP: 5–10 aturan · **Harus direview dosen metodologi** sebelum dipakai.

Prinsip: aturan bersifat deterministik & configurable; keluaran berupa **pertanyaan/peringatan yang dapat diverifikasi**, bukan vonis. LLM hanya membantu ekstraksi dan penjelasan.

## Aturan Inti (dari proposal)

| ID | Aturan | Pemicu | Pesan temuan (pola) | Prioritas |
|---|---|---|---|---|
| R-RQ-OBJ | Tiap RQ terhubung ke ≥1 objective | RQ tanpa edge `addresses`→Objective | "RQ{n} belum terhubung ke tujuan penelitian. Periksa apakah ada objective yang sesuai." | High |
| R-OBJ-DATA | Tiap objective punya data source & analysis plan | Objective tanpa `requires` Data Source atau `analyzed_with` Analysis | "Objective {n} belum memiliki sumber data / rencana analisis." | High |
| R-VAR-INSTR | Variabel yang dianalisis terhubung ke indikator/instrumen | Variable tanpa `measured_by` | "Variabel {x} dianalisis tetapi tidak ditemukan pada instrumen." | Medium |
| R-CAUSAL-01 | Klaim/kata kausal butuh desain pendukung | RQ/Claim memakai pola kausal (mis. "pengaruh", "impact", "menyebabkan") + desain survei/cross-sectional/korelasi | "Desain saat ini mungkin hanya menunjukkan asosiasi, bukan dampak kausal. Diskusikan reframing atau desain lain." | High |
| R-POP-CHANGE | Perubahan populasi memicu cek sampling & generalisasi | Node Population berubah antarversi | "Populasi berubah. Periksa sampling frame, ukuran sampel, stratifikasi, generalisasi, kelayakan rekrutmen." | High |

## Aturan Tambahan Usulan (untuk melengkapi 5–10; **perlu validasi dosen**)

| ID | Aturan | Pemicu | Prioritas |
|---|---|---|---|
| R-METHOD-RQ | Metode mampu menjawab bentuk RQ | Bentuk RQ (deskriptif/komparatif/kausal) tidak cocok dengan metode | Medium |
| R-SAMPLE-UNIT | Populasi/sampling sesuai unit analisis | Unit analisis ≠ unit sampling | Medium |
| R-ANALYSIS-TYPE | Teknik analisis sesuai tipe data | Skala variabel tak cocok dengan analisis | Medium |
| R-CONCL-SCOPE | Kesimpulan terencana dalam batas desain | Claim melampaui desain/populasi | Medium |
| R-TERM-CONSIST | Terminologi konsisten antar bagian (mis. abstrak vs RQ) | Istilah kunci berbeda ("impact" vs "hubungan") | Low–Medium |

## Aturan Konvensi Penulisan (konsistensi gaya, bukan isi)

Landasan berasal dari konvensi penulisan matematika dan gaya publikasi, bukan metodologi. Keduanya **tidak memilih gaya**; yang diperiksa hanya konsistensi. Gaya yang berlaku ditentukan panduan prodi atau jurnal target.

| ID | Aturan | Pemicu (`mixed_patterns`) | `source_types` | Prioritas |
|---|---|---|---|---|
| R-CITE-STYLE-MIX | Satu sistem sitasi per dokumen | ≥2 sitasi bernomor `[n]` **dan** ≥2 sitasi penulis–tahun | `publication_style` | Low |
| R-DECIMAL-MIX | Satu penanda desimal per dokumen | ≥2 `0,dd` **dan** ≥2 `0.dd` | `math_writing` | Low |

Setiap temuan menawarkan **arah** (`directions`) beserta konsekuensinya, termasuk arah "temuan ini bisa ditolak" bila polanya bukan yang dimaksud (interval `[0, 1]`, abstrak berbahasa Inggris).

## Format Konfigurasi (usulan)

```yaml
- id: R-CAUSAL-01
  enabled: true
  priority: high
  patterns: ["pengaruh", "mempengaruhi", "dampak", "impact", "menyebabkan", "effect"]
  design_flags_non_causal: ["cross_sectional", "survey_single", "correlation"]
  message_id: "Desain saat ini mungkin hanya menunjukkan asosiasi ..."
  require_evidence: [research_question, research_design, analysis_plan]
```

## Uji Aturan

Tiap aturan wajib punya: 1 kasus positif (harus terpicu), 1 kasus negatif (tidak boleh terpicu), dan rujukan evidence. Skenario acuan: kasus Nadia (proposal §16) untuk `R-CAUSAL-01`.
