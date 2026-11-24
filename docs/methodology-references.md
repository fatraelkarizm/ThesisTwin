# Rujukan Metodologi untuk Aturan Cek Konsistensi

Setiap aturan di [apps/api/rules/](../apps/api/rules/README.md) membawa `basis` (prinsip), `references` (rujukan), `source_types` (asal landasan), dan `directions` (arah yang bisa dieksplorasi beserta konsekuensinya, bukan vonis atau perintah). Halaman ini mendaftar semua rujukan yang dipakai.

> **Status verifikasi:** rujukan di bawah adalah karya metodologi yang dikenal luas. Rujukan dicantumkan di tingkat buku/artikel, **tanpa nomor halaman**, karena halaman belum diverifikasi oleh tim. Sebelum dikutip di proposal STACK atau di aplikasi untuk dosen: (1) cek edisi yang tersedia di perpustakaan, (2) catat bab/halaman yang mendukung tiap aturan, (3) minta dosen metodologi meninjau aturan dan ubah `reviewed_by_supervisor: true`.

| Rujukan | Dipakai di aturan | Yang didukung |
|---|---|---|
| Campbell, D. T., & Stanley, J. C. (1963). *Experimental and quasi-experimental designs for research.* Rand McNally. | R-CAUSAL-01 | Klasifikasi desain; one-group pretest–posttest termasuk desain **pra-eksperimental** yang lemah untuk inferensi kausal |
| Shadish, W. R., Cook, T. D., & Campbell, D. T. (2002). *Experimental and quasi-experimental designs for generalized causal inference.* Houghton Mifflin. | R-CAUSAL-01, R-CONCL-SCOPE, R-VALIDITY-THREATS | Ancaman validitas internal, eksternal, konstruk, dan kesimpulan statistik |
| Creswell, J. W., & Creswell, J. D. (2018). *Research design: Qualitative, quantitative, and mixed methods approaches* (5th ed.). SAGE. | R-RQ-OBJ, R-RQ-OBJ-COUNT, R-OBJ-ANALYSIS, R-VAR-INSTR, R-CONCL-SCOPE, R-PROPOSAL-RESULTS | Keselarasan tujuan dan pertanyaan penelitian; proposal sebagai rencana; rencana analisis per pertanyaan |
| Sugiyono. (2019). *Metode penelitian kuantitatif, kualitatif, dan R&D.* Alfabeta. | R-RQ-OBJ, R-RQ-OBJ-COUNT, R-VAR-INSTR | Rumusan masalah dan tujuan; definisi operasional variabel; instrumen serta validitas/reliabilitas (rujukan umum di kampus Indonesia) |
| Wohlin, C., Runeson, P., Höst, M., Ohlsson, M. C., Regnell, B., & Wesslén, A. (2012). *Experimentation in software engineering.* Springer. | R-VALIDITY-THREATS, R-STAT-TEST | Eksperimen di rekayasa perangkat lunak; analisis ancaman validitas; uji hipotesis |
| Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *Journal of Machine Learning Research, 7*, 1–30. | R-STAT-TEST | Perbandingan model/klasifier perlu uji statistik yang tepat, bukan hanya selisih rata-rata |

## Yang belum dicakup (jujur)

- **Panduan resmi prodi** (bagian wajib proposal): R-SECTIONS-UMUM masih contoh umum tanpa rujukan.
- **Rujukan khusus pendidikan Matematika** belum ada; aturan saat ini bersifat lintas bidang.
- Aturan bekerja dengan kata kunci; ia **tidak memahami** isi argumen. Rujukan menjelaskan *mengapa* sebuah pola layak ditanyakan, bukan membuktikan bahwa proposal itu salah.
