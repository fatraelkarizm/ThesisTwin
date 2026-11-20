# ThesisTwin — Detailed Concept Proposal (STACK 2026, Case 1)

> Konversi penuh dari `ThesisTwin_Detailed_Proposal_STACK_2026.pdf` (27 halaman, Versi 1.0, 8 November 2026).
> Ini adalah **source of truth** untuk seluruh dokumen lain di folder `docs/`. Jika ada konflik, dokumen ini yang menang.

**Selected Case:** Smarter Campus and Learning
**Tagline:** *"ThesisTwin tidak menulis skripsi mahasiswa. ThesisTwin mencegah mahasiswa tersesat ketika menyelesaikannya."*
**Subjudul:** AI-Powered Navigation and Consistency Engine for the Undergraduate Thesis Journey

---

## 1. Ringkasan Eksekutif

Skripsi merupakan salah satu perjalanan akademik yang paling panjang, tidak pasti, dan bergantung pada banyak keputusan. Mahasiswa harus mengubah ide awal menjadi rumusan masalah, tujuan penelitian, metode, instrumen, data, analisis, dan kesimpulan yang saling konsisten. Dalam praktiknya, perjalanan tersebut juga melibatkan panduan kampus, jadwal administratif, beberapa versi dokumen, komentar pembimbing, percakapan WhatsApp, serta keputusan yang sering tidak tercatat secara sistematis.

Hambatan utama bukan hanya kemampuan menulis. Mahasiswa kerap tidak mengetahui posisi penelitiannya, langkah berikutnya, alasan sebuah revisi diminta, atau bagian lain yang terdampak ketika satu keputusan berubah. Dosen pembimbing juga harus berulang kali merekonstruksi konteks sebelum memberikan feedback. Akibatnya, bimbingan dapat berubah menjadi siklus revisi yang panjang dan reaktif.

ThesisTwin diusulkan sebagai **AI-powered navigation and consistency engine** yang membangun representasi digital dari perjalanan skripsi mahasiswa. Sistem mengekstrak elemen inti penelitian, menyusunnya sebagai research dependency graph, menghubungkan feedback dengan bagian yang terdampak, menyimpan riwayat keputusan, mendeteksi inkonsistensi, dan menghasilkan langkah berikutnya yang dapat diverifikasi.

ThesisTwin secara sengaja **tidak dirancang untuk menulis skripsi secara otomatis**. Sistem mendukung proses berpikir dan koordinasi, sementara keputusan ilmiah tetap menjadi tanggung jawab mahasiswa dan dosen. Pendekatan ini membedakan ThesisTwin dari chatbot akademik, summarizer, maupun generator tulisan.

Untuk MVP STACK 2026, ruang lingkup dibatasi pada perjalanan proposal skripsi — Bab 1 sampai Bab 3 — dengan satu interaksi inti: mahasiswa mengunggah proposal dan feedback pembimbing, lalu memperoleh peta keterkaitan penelitian, temuan inkonsistensi, dampak revisi, serta next-action plan untuk sesi bimbingan berikutnya.

---

## 2. Kesesuaian dengan Case 1: Smarter Campus and Learning

Handbook STACK 2026 mendefinisikan Case 1 melalui pertanyaan:

> "How might we help students learn, collaborate, and access campus opportunities more effectively?"

Case ini berfokus pada solusi digital yang mengurangi hambatan dalam student journey. Pengguna yang disebutkan mencakup mahasiswa, organisasi mahasiswa, peer mentor, dan pengguna layanan kampus. Tim juga diminta mendemonstrasikan perjalanan pengguna yang jelas, interaksi inti yang bekerja, serta manfaat yang dapat diukur seperti penghematan waktu, peningkatan keberhasilan tugas, atau aksesibilitas yang lebih baik.

ThesisTwin memenuhi kriteria tersebut karena:

- Berfokus pada fase kritis dalam perjalanan mahasiswa, yaitu penyelesaian tugas akhir.
- Mengurangi hambatan informasi, koordinasi, dokumentasi, dan konsistensi penelitian.
- Melibatkan mahasiswa, dosen pembimbing, peer mentor, dan layanan akademik.
- Memiliki interaksi inti yang dapat didemonstrasikan dalam waktu singkat.
- Menghasilkan manfaat yang dapat diuji melalui waktu persiapan bimbingan, jumlah inkonsistensi, dan tingkat tindak lanjut feedback.

---

## 3. Latar Belakang dan Urgensi

### 3.1 Skripsi sebagai perjalanan, bukan satu dokumen

Skripsi sering diperlakukan sebagai satu file akhir. Padahal, skripsi sebenarnya adalah perjalanan keputusan yang saling bergantung. Sebuah perubahan pada rumusan masalah dapat memengaruhi tujuan penelitian, definisi variabel, kebutuhan data, metode sampling, instrumen, teknik analisis, dan ruang lingkup kesimpulan.

Dokumen pengolah kata dapat menyimpan teks, tetapi tidak memahami hubungan logis tersebut. Task manager dapat menyimpan daftar pekerjaan, tetapi tidak mengetahui bahwa perubahan target populasi membuat kriteria inklusi dan perhitungan sampel harus diperiksa kembali. Chatbot dapat menjawab pertanyaan, tetapi biasanya tidak mempertahankan status longitudinal penelitian secara andal selama berbulan-bulan.

### 3.2 Fragmentasi konteks bimbingan

Konteks skripsi dapat tersebar pada:

- Berbagai versi file proposal.
- Komentar dan track changes pada dokumen.
- Pesan WhatsApp atau email pembimbing.
- Catatan pribadi mahasiswa.
- Form bimbingan dan portal akademik.
- Panduan penulisan serta SOP fakultas.
- Keputusan verbal yang tidak pernah dicatat.

Fragmentasi ini menimbulkan **context reconstruction cost**: mahasiswa dan dosen harus mengingat kembali apa yang berubah, mengapa berubah, dan keputusan mana yang sudah disetujui.

### 3.3 Indikator nasional dan batas interpretasinya

Statistik Pendidikan Tinggi 2025 mencatat 289.670 mahasiswa mengalami putus kuliah, meningkat 2,62% dibanding 2024. Kelompok usia 21–30 tahun menjadi kelompok dengan jumlah putus kuliah tertinggi. Data tersebut menunjukkan bahwa keberlanjutan studi merupakan persoalan penting pada pendidikan tinggi Indonesia.

Namun, data tersebut **tidak menjelaskan bahwa skripsi adalah penyebab putus kuliah**. Karena itu, ThesisTwin tidak menggunakan angka nasional untuk membuat klaim kausal. Urgensi spesifik terkait skripsi harus dibuktikan melalui riset pengguna di kampus sasaran, misalnya jumlah putaran revisi, waktu tunggu feedback, frekuensi kehilangan konteks, dan jenis inkonsistensi proposal yang paling sering terjadi.

Prinsip ini penting agar presentasi tim tetap akurat sesuai aturan STACK 2026: angka pengguna dan temuan riset harus dilaporkan secara jujur, sedangkan data simulasi harus diberi label dengan jelas.

---

## 4. Definisi Permasalahan

### 4.1 Problem statement

> Mahasiswa tingkat akhir membutuhkan cara untuk mengetahui posisi penelitian, menjaga keterkaitan antarbagian, menerjemahkan feedback menjadi tindakan, dan mempertahankan riwayat keputusan selama proses skripsi tanpa menyerahkan proses berpikir atau penulisan kepada AI.

### 4.2 Akar masalah

| Akar masalah | Manifestasi | Dampak |
|---|---|---|
| Struktur penelitian tidak terlihat | Bab dibaca sebagai bagian terpisah | Inkonsistensi baru ditemukan terlambat |
| Feedback tidak terstruktur | Komentar abstrak seperti "metodenya diperjelas" | Mahasiswa bingung menentukan tindakan |
| Tidak ada decision memory | Alasan pemilihan metode tidak terdokumentasi | Diskusi yang sama berulang |
| Perubahan tidak dianalisis dampaknya | Satu bagian diperbarui tanpa memperbarui bagian lain | Revisi berantai dan kontradiksi |
| Persiapan bimbingan lemah | Mahasiswa datang tanpa daftar isu dan keputusan | Waktu bimbingan tidak optimal |
| Panduan kampus terpisah | Aturan format dan milestone dicari manual | Kesalahan administratif dan keterlambatan |

### 4.3 Sasaran pengguna

**Pengguna utama:**
- Mahasiswa S1 yang sedang menyiapkan proposal atau skripsi.
- Dosen pembimbing yang menangani beberapa mahasiswa secara paralel.

**Pengguna pendukung:**
- Peer mentor atau asisten akademik.
- Koordinator tugas akhir dan program studi.
- Layanan akademik kampus.

---

## 5. Solusi: ThesisTwin

### 5.1 Konsep inti

ThesisTwin membuat **digital twin dari perjalanan skripsi**: model yang selalu diperbarui mengenai struktur penelitian, status keputusan, feedback, milestone, dan dependency. Sistem menjawab empat pertanyaan utama:

1. **Where am I?** — Posisi mahasiswa dalam perjalanan skripsi.
2. **What is inconsistent?** — Bagian yang tidak selaras atau belum didukung.
3. **What changes if I revise this?** — Dampak sebuah revisi terhadap bagian lain.
4. **What should I do next?** — Tindakan konkret sebelum bimbingan berikutnya.

### 5.2 Research dependency graph

```
Research Problem
      ↓
Research Questions
      ↓
Research Objectives
      ↓
Concepts / Variables
      ↓
Required Evidence and Data
      ↓
Population and Sampling
      ↓
Instrument / Data Collection
      ↓
Analysis Method
      ↓
Claims and Expected Conclusions
```

Setiap node menyimpan lokasi sumber, status verifikasi, versi terakhir, feedback terkait, dan hubungan dengan node lain. Graph ini memungkinkan pemeriksaan berbasis dependency, bukan sekadar pemeriksaan tata bahasa.

### 5.3 Nilai yang diberikan

- Mahasiswa memperoleh kejelasan posisi dan langkah berikutnya.
- Feedback pembimbing berubah menjadi tindakan terstruktur.
- Dampak revisi dapat terlihat sebelum menimbulkan kontradiksi baru.
- Dosen memperoleh ringkasan perubahan dan isu terbuka sebelum bimbingan.
- Riwayat keputusan tidak hilang ketika dokumen terus berubah.

---

## 6. Fitur Utama

### 6.1 Thesis Route Map

Dashboard menunjukkan milestone, dependency yang selesai, bagian terhambat, dan tindakan paling penting.

```
CURRENT BOTTLENECK
Sampling criteria belum mendapat validasi.

BLOCKED TASKS
- Participant recruitment
- Instrument distribution
- Statistical analysis plan

NEXT BEST ACTION
Konfirmasi inclusion dan exclusion criteria kepada pembimbing.
```

### 6.2 Alignment Checker

Sistem memeriksa hubungan seperti:

- Apakah setiap research question memiliki objective yang sesuai?
- Apakah metode mampu menjawab bentuk pertanyaan yang diajukan?
- Apakah variabel atau konsep muncul dalam instrumen?
- Apakah populasi dan sampling sesuai dengan unit analisis?
- Apakah teknik analisis sesuai dengan tipe data?
- Apakah kesimpulan yang direncanakan berada dalam batas desain penelitian?

Hasil pemeriksaan harus berupa **pertanyaan atau peringatan yang dapat diverifikasi, bukan keputusan mutlak**. Contoh:

> "Research Question 2 menggunakan kata 'impact', tetapi desain yang tercantum adalah survei deskriptif. Periksa apakah tujuan penelitian bersifat kausal atau hanya mendeskripsikan hubungan."

### 6.3 Feedback-to-Action

Feedback pembimbing diubah menjadi struktur berikut:

```
Original feedback:
"Metodenya coba diperjelas dan sesuaikan dengan tujuan kedua."

Possible interpretation:
Objective 2 dan research design mungkin belum selaras.

Affected components:
- Objective 2
- Research design
- Data collection
- Analysis method

Proposed actions:
1. Tentukan apakah Objective 2 bersifat deskriptif, komparatif, atau kausal.
2. Tuliskan justifikasi desain yang dipilih.
3. Petakan Objective 2 ke data dan metode analisis.

Status:
Waiting for student confirmation.
```

### 6.4 Change Impact Analysis

Ketika mahasiswa mengubah suatu node, sistem menunjukkan kemungkinan dampaknya.

Contoh perubahan: *Target population berubah dari mahasiswa tahun pertama menjadi seluruh mahasiswa aktif.*

Bagian yang perlu diperiksa:
- Definisi populasi.
- Sampling frame.
- Perhitungan ukuran sampel.
- Stratifikasi fakultas atau angkatan.
- Batas generalisasi hasil.
- Kelayakan rekrutmen peserta.

### 6.5 Decision Memory

Setiap keputusan penting disimpan bersama alasan dan sumber persetujuan.

```
Decision: Use stratified random sampling
Reason: Population distribution differs across faculties
Confirmed by: Supervisor 1
Date: 12 October 2026
Evidence: Meeting note #04
Affected sections: 3.2, 3.3, 3.5
```

### 6.6 Bimbingan Brief

Sebelum sesi bimbingan, sistem membuat ringkasan satu halaman:

- Perubahan sejak pertemuan sebelumnya.
- Feedback yang telah diselesaikan.
- Keputusan yang membutuhkan persetujuan.
- Konflik atau inkonsistensi yang masih terbuka.
- Pertanyaan yang disiapkan mahasiswa.
- Rekomendasi fokus pertemuan.

### 6.7 Multi-Supervisor Conflict Flag

Jika dua feedback tampak berbeda, sistem tidak memilih salah satunya. Sistem menampilkan konteks dan menyarankan pertanyaan klarifikasi.

> "Feedback A meminta perluasan populasi, sedangkan Feedback B menekankan pembatasan ruang lingkup. Konfirmasi apakah perluasan hanya berlaku pada lokasi penelitian atau juga target population."

---

## 7. User Journey

### 7.1 Journey mahasiswa

| Tahap | Aktivitas | Respons ThesisTwin | Outcome |
|---|---|---|---|
| Onboarding | Memilih prodi dan mengunggah panduan | Sistem memuat aturan dan milestone | Rute skripsi sesuai kampus |
| Proposal intake | Mengunggah Bab 1–3 | AI mengekstrak elemen penelitian | Dependency graph awal |
| Self-review | Memeriksa temuan sistem | Mahasiswa menerima/menolak ekstraksi | Graph terverifikasi pengguna |
| Bimbingan | Mengunggah atau mencatat feedback | AI memetakan feedback ke bagian terkait | Action items terstruktur |
| Revision | Mengunggah versi baru | Sistem membandingkan perubahan | Dampak revisi terlihat |
| Pre-meeting | Membuka bimbingan brief | Sistem merangkum status dan isu | Pertemuan lebih terarah |
| Progress review | Melihat route map | Sistem menunjukkan bottleneck | Mahasiswa tahu langkah berikutnya |

### 7.2 Journey dosen

1. Membuka ringkasan mahasiswa sebelum pertemuan.
2. Melihat perubahan penting, bukan membaca ulang seluruh dokumen.
3. Memeriksa temuan AI dan menandainya sebagai valid atau tidak relevan.
4. Mengonfirmasi keputusan serta action items.
5. Melihat isu yang terus berulang lintas pertemuan.

### 7.3 Boundary yang dijaga

ThesisTwin **tidak**:

- Menulis bab secara otomatis.
- Mengarang referensi.
- Menentukan bahwa suatu metodologi pasti benar.
- Menggantikan persetujuan dosen.
- Mengirim dokumen atau keputusan tanpa tindakan pengguna.

---

## 8. Research Gap dan Novelty

### 8.1 Gap utama

> Sistem AI akademik saat ini banyak berfokus pada generasi atau review teks, tetapi masih terbatas dalam mempertahankan konsistensi longitudinal, dependency keputusan, provenance feedback, dan status perjalanan skripsi mahasiswa.

### 8.2 Document-centric versus journey-centric

Sebagian besar alat AI menerima satu dokumen dan menghasilkan satu respons. Skripsi berlangsung dalam banyak versi dan keputusan. Kebutuhan utamanya bukan hanya kualitas respons, melainkan kontinuitas konteks serta kemampuan menjelaskan mengapa suatu peringatan muncul.

| Pendekatan umum | ThesisTwin |
|---|---|
| Dokumen sebagai input tunggal | Perjalanan dan versi sebagai state |
| Feedback berupa teks bebas | Feedback terhubung ke node dan tindakan |
| Jawaban sekali pakai | Decision memory longitudinal |
| LLM menentukan penilaian | LLM + constraints + retrieval + human approval |
| Fokus pada kualitas tulisan | Fokus pada alignment dan progress |

### 8.3 Keterbatasan LLM dalam scientific review

Riset ACL 2025 mengenai kemampuan LLM menemukan keterbatasan penelitian memperkenalkan benchmark **LimitGen** dan menunjukkan bahwa literature retrieval penting untuk menghasilkan kritik yang lebih konkret dan grounded. Ini mendukung desain ThesisTwin yang tidak hanya mengandalkan pengetahuan parametrik model.

Riset terhadap lebih dari 2.000 karya mengenai LLM juga menemukan tren meningkatnya penggunaan LLM sebagai evaluator tanpa human evaluation yang memadai. Karena itu, hasil ThesisTwin diposisikan sebagai **decision support, bukan penilaian final**.

### 8.4 Gap konteks Indonesia

Ruang riset yang dapat diuji mencakup:

- Proposal skripsi berbahasa Indonesia atau campuran Indonesia–Inggris.
- Feedback singkat, informal, dan ambigu dari percakapan bimbingan.
- SOP dan template yang berbeda antarkampus atau program studi.
- Proses dengan lebih dari satu pembimbing.
- Seminar proposal, pengumpulan data, sidang, dan revisi administratif.

### 8.5 Research questions

- **RQ1.** Apakah research dependency graph meningkatkan kemampuan sistem menemukan inkonsistensi proposal dibanding direct prompting pada LLM?
- **RQ2.** Apakah feedback-to-action mapping mengurangi waktu mahasiswa memahami dan menindaklanjuti feedback pembimbing?
- **RQ3.** Apakah decision memory mengurangi pengulangan isu yang sama antarsesi bimbingan?
- **RQ4.** Seberapa tinggi kesesuaian temuan ThesisTwin dengan penilaian dosen pembimbing?

### 8.6 Hipotesis

- **H1:** Pipeline graph + constraints menghasilkan precision temuan alignment yang lebih tinggi daripada LLM-only baseline.
- **H2:** Mahasiswa yang menggunakan ThesisTwin membutuhkan waktu lebih sedikit untuk membuat action plan setelah bimbingan.
- **H3:** Bimbingan brief meningkatkan proporsi isu yang berhasil diputuskan dalam satu sesi.

---

## 9. Desain Teknis

### 9.1 Arsitektur tingkat tinggi

```
Proposal / Guideline / Feedback / Version History
                    ↓
          Document Ingestion Layer
                    ↓
     Structured Research Element Extraction
                    ↓
            Thesis Knowledge Graph
                    ↓
 ┌──────────────────┼───────────────────┐
 ↓                  ↓                   ↓
LLM Reasoning   Constraint Engine   Retrieval Layer
 └──────────────────┼───────────────────┘
                    ↓
     Findings + Evidence + Confidence
                    ↓
        Human Confirmation Workflow
                    ↓
Route Map / Action Plan / Decision Memory / Brief
```

### 9.2 Komponen sistem

#### A. Document ingestion
- Mendukung DOCX dan PDF untuk MVP.
- Mengekstrak heading, paragraf, tabel, komentar, dan nomor halaman.
- Menyimpan hash dan versi dokumen.
- Mempertahankan lokasi sumber untuk setiap elemen.

#### B. Structured extraction
LLM menghasilkan structured output, bukan teks bebas:

```json
{
  "element_type": "research_question",
  "content": "Apakah X memengaruhi Y pada populasi Z?",
  "source": {"document": "proposal_v3", "page": 7},
  "status": "needs_user_confirmation",
  "confidence": 0.86
}
```

#### C. Thesis knowledge graph
- **Node utama:** Problem, question, objective, concept, variable; Population, sample, instrument, data source; Method, analysis, claim, limitation; Feedback, decision, action, milestone.
- **Edge utama:** addresses, requires, measured_by, analyzed_with; affected_by, approved_by, contradicts, supersedes.

#### D. Constraint engine
Contoh aturan MVP:
- Setiap research question harus terhubung ke minimal satu objective.
- Setiap objective harus memiliki data source dan analysis plan.
- Variabel yang dianalisis harus terhubung ke indikator atau instrumen.
- Klaim kausal memerlukan desain yang mendukung inferensi kausal atau harus diberi peringatan.
- Perubahan populasi memicu pemeriksaan sampling dan generalisasi.

Aturan bersifat configurable dan harus dikembangkan bersama dosen metodologi.

#### E. Retrieval layer
Sumber retrieval dibatasi pada:
- Panduan skripsi kampus.
- Rubrik proposal program studi.
- Catatan dan feedback pembimbing.
- Literatur yang dimasukkan pengguna.

Setiap output harus menyertakan sumber. Jika evidence tidak tersedia, sistem harus mengatakan bahwa temuan memerlukan konfirmasi.

#### F. Human confirmation
Status temuan: **AI-suggested**, **Student-confirmed**, **Supervisor-confirmed**, **Rejected**, **Resolved**. Status ini mencegah saran AI dianggap sebagai persetujuan akademik.

### 9.3 Stack implementasi MVP

| Layer | Pilihan teknologi |
|---|---|
| Frontend | Next.js PWA atau Flutter Web |
| Backend | FastAPI atau Node.js |
| Database | PostgreSQL |
| Graph | Relational graph model; Neo4j opsional |
| File storage | S3-compatible object storage |
| Retrieval | pgvector atau vector database |
| AI | LLM dengan structured JSON output |
| Processing | DOCX/PDF parser + version diff |
| Security | Encryption at rest, role-based access, audit log |

---

## 10. Scope MVP STACK 2026

### 10.1 In scope
- Proposal Bab 1–3.
- Satu format panduan kampus.
- Ekstraksi research question, objective, variable/concept, population, method, instrument, dan analysis.
- Visualisasi dependency graph.
- Lima sampai sepuluh aturan alignment.
- Input feedback pembimbing secara manual atau dari teks.
- Feedback-to-action mapping.
- Change impact analysis sederhana.
- Bimbingan brief.

### 10.2 Out of scope
- Penulisan otomatis seluruh bab.
- Pemeriksaan statistik tingkat lanjut.
- Integrasi penuh dengan semua LMS/SIAKAD.
- Keputusan kelayakan sidang otomatis.
- Plagiarism detection sebagai fitur utama.
- Fine-tuning model berskala besar.

### 10.3 Core demo flow
1. Mahasiswa mengunggah proposal versi pertama.
2. ThesisTwin membentuk dependency graph.
3. Sistem menemukan tiga isu alignment dengan bukti halaman.
4. Pengguna memasukkan feedback pembimbing.
5. Sistem mengubah feedback menjadi action items.
6. Mahasiswa mengunggah versi revisi.
7. Sistem memperlihatkan perubahan, isu terselesaikan, dan dampak baru.
8. Sistem menghasilkan bimbingan brief.

---

## 11. Rencana Riset Pengguna dan Validasi

### 11.1 Discovery research

Target awal:
- 15–30 mahasiswa yang sedang atau baru menyelesaikan skripsi.
- 3–5 dosen pembimbing.
- 1–2 koordinator tugas akhir atau staf akademik.

Pertanyaan yang dicari:
- Tahap mana yang paling sering membuat mahasiswa berhenti bergerak?
- Berapa banyak putaran revisi sebelum proposal diterima?
- Di mana feedback pembimbing disimpan?
- Berapa lama mahasiswa mengubah feedback menjadi daftar tindakan?
- Masalah alignment apa yang paling sering ditemukan dosen?
- Informasi apa yang perlu dilihat dosen sebelum bimbingan?

### 11.2 Dataset evaluasi kecil

Dengan persetujuan pemilik data:
- 20–30 proposal yang dianonimkan.
- 50–100 potongan feedback pembimbing.
- Label inkonsistensi dari minimal dua evaluator.
- Versi sebelum dan setelah revisi jika tersedia.

Jika dokumen nyata tidak dapat digunakan, tim dapat membuat dataset sintetis berbasis template, tetapi harus diberi label sebagai **data simulasi**.

### 11.3 Eksperimen

- **Baseline:** proposal langsung diberikan kepada LLM dengan prompt "review consistency".
- **Treatment:** structured extraction + knowledge graph + constraint engine + retrieval.

Evaluasi dilakukan pada:
- Precision temuan yang dinilai valid oleh dosen.
- Recall pada daftar inkonsistensi yang sudah diberi label.
- Evidence correctness: apakah halaman sumber sesuai?
- Actionability: apakah saran dapat ditindaklanjuti?
- Waktu penyelesaian tugas pengguna.

### 11.4 Success metrics

| Tujuan | Metrik | Target awal MVP |
|---|---|---|
| Menghemat waktu | Waktu membuat action plan | Turun ≥30% |
| Meningkatkan tindak lanjut | Feedback yang menjadi action item | ≥80% |
| Menjaga ketepatan | Precision temuan alignment | ≥75% setelah konfirmasi |
| Menjaga provenance | Temuan dengan sumber valid | ≥90% |
| Memperjelas proses | Task completion pada user test | ≥80% |
| Meningkatkan usability | System Usability Scale | ≥70 |

> Target tersebut merupakan hipotesis awal dan tidak boleh dipresentasikan sebagai hasil sebelum diuji.

---

## 12. Integritas Akademik, Privasi, dan Risiko

### 12.1 Prinsip integritas akademik
- Sistem membantu navigasi, bukan menghasilkan karya untuk diserahkan.
- Semua saran ditandai sebagai AI-generated.
- Tidak ada referensi yang dibuat tanpa sumber.
- Mahasiswa tetap harus menjelaskan keputusan penelitian.
- Persetujuan metodologi hanya dapat diberikan dosen.
- Riwayat penggunaan dan perubahan tersedia sebagai audit trail.

### 12.2 Privasi

Dokumen skripsi dapat mengandung ide penelitian, data peserta, atau informasi sensitif. Kontrol minimum:
- Consent eksplisit sebelum upload.
- Enkripsi saat transit dan saat tersimpan.
- Pengaturan siapa yang dapat membuka dokumen.
- Pemisahan data identitas dan isi penelitian.
- Opsi penghapusan permanen.
- Tidak menggunakan dokumen untuk training tanpa persetujuan terpisah.
- Redaction otomatis untuk NIM, nomor telepon, email, dan data peserta.

### 12.3 Risiko dan mitigasi

| Risiko | Dampak | Mitigasi |
|---|---|---|
| AI salah menilai metode | Mahasiswa mengikuti saran yang keliru | Evidence, confidence, constraint, dan supervisor confirmation |
| Mahasiswa terlalu bergantung | Penurunan proses berpikir mandiri | Socratic prompts dan larangan auto-writing |
| Feedback ambigu salah dipahami | Action item tidak sesuai | Tampilkan interpretasi dan minta konfirmasi |
| Dokumen bocor | Kerugian akademik dan privasi | Encryption, RBAC, retention policy |
| Dosen merasa digantikan | Adopsi rendah | Positioning sebagai preparation and memory layer |
| Aturan berbeda antarkampus | Temuan tidak relevan | Campus-specific policy pack |

---

## 13. Strategi Implementasi di Kampus

- **Fase 1 — Student-side pilot.** Dimulai tanpa integrasi sistem kampus. Mahasiswa mengunggah proposal, mengonfirmasi graph, dan memasukkan feedback secara mandiri. Mengurangi hambatan adopsi dan memungkinkan validasi cepat.
- **Fase 2 — Supervisor workspace.** Dosen memperoleh bimbingan brief, kemampuan mengonfirmasi keputusan, serta dashboard mahasiswa bimbingan. Fokus: mengurangi waktu membaca ulang konteks.
- **Fase 3 — Program study integration.** Program studi memasukkan SOP, milestone, rubrik, dan template resmi. Data agregat dapat menunjukkan bottleneck umum tanpa mengekspos isi skripsi individual.
- **Model keberlanjutan:**
  - Lisensi institusi untuk program studi atau fakultas.
  - Versi mahasiswa gratis dengan batas jumlah proyek.
  - Campus-hosted deployment untuk institusi dengan kebutuhan privasi tinggi.
  - Tidak memonetisasi atau menjual isi skripsi mahasiswa.

---

## 14. Roadmap Pengembangan

| Fase | Fokus | Deliverable |
|---|---|---|
| Preliminary | Problem validation | Abstract, interview awal, problem evidence |
| Semifinal | Product definition | Proposal, user journey, prototype design |
| Pre-final | Core build | Parser, graph, rules, feedback mapping |
| Final Day | Working demo | End-to-end core interaction dan test result |
| Post-hackathon | Pilot | Uji pada satu prodi dan perbaikan model |

Prioritas engineering:
1. Structured extraction yang stabil.
2. Evidence linking ke halaman sumber.
3. Dependency visualization.
4. Rule-based alignment checks.
5. Feedback-to-action.
6. Version comparison.

---

## 15. Competitive Positioning

| Alternatif | Kekuatan | Keterbatasan yang dijawab ThesisTwin |
|---|---|---|
| General AI chatbot | Fleksibel dan cepat | Tidak mempertahankan state perjalanan secara terstruktur |
| Grammar checker | Meningkatkan kualitas bahasa | Tidak memahami dependency penelitian |
| Reference manager | Mengelola sitasi | Tidak mengelola feedback dan keputusan |
| Project management tool | Mengelola tugas | Tidak memahami hubungan metodologis |
| LMS/SIAKAD | Menyimpan milestone resmi | Tidak membantu navigasi kognitif dan alignment |
| **ThesisTwin** | Journey-aware dan evidence-grounded | Memerlukan validasi dosen serta konfigurasi kampus |

Moat utama bukan akses ke model AI, melainkan:
- Struktur thesis ontology.
- Dataset alignment dan feedback yang dianonimkan.
- Constraint library yang dikembangkan bersama dosen.
- Longitudinal decision graph.
- Integrasi workflow kampus dan kepercayaan pengguna.

---

## 16. Contoh Skenario Lengkap

### Kondisi awal
Nadia meneliti pengaruh penggunaan platform video pendek terhadap konsentrasi belajar mahasiswa. Pada proposal awal, ia menggunakan survei satu kali dan analisis korelasi. Namun, research question memakai kata "pengaruh" dan kesimpulan yang direncanakan menyatakan hubungan sebab-akibat.

### Temuan ThesisTwin

```
Potential alignment issue — High priority

Research question:
"Bagaimana pengaruh penggunaan platform video pendek terhadap konsentrasi?"

Current design:    Cross-sectional survey
Current analysis:  Correlation analysis

Why flagged:
The current design may identify an association but may not establish causal impact.

Evidence:
- Research Question: page 5
- Research Design: page 21
- Analysis Plan: page 29

Suggested clarification:
Discuss whether the research question should be reframed as an association,
or whether a different design is needed.
```

### Feedback pembimbing
> "Jangan terlalu berani menyimpulkan pengaruh. Sesuaikan lagi pertanyaan dan batasannya."

### Hasil feedback-to-action
1. Konfirmasi apakah fokus penelitian adalah hubungan atau pengaruh kausal.
2. Revisi research question jika fokusnya korelasional.
3. Perbarui tujuan penelitian.
4. Periksa hipotesis dan istilah "mempengaruhi".
5. Tambahkan limitation mengenai desain cross-sectional.

### Setelah revisi
ThesisTwin membandingkan proposal baru dan menunjukkan bahwa research question serta objective sudah berubah, tetapi abstrak masih menggunakan kata "impact". Sistem menandainya sebagai **unresolved dependency**. Nadia dapat memperbaikinya sebelum sesi bimbingan berikutnya.

---

## 17. Narasi Pitch

- **Problem hook:** "Mahasiswa tidak selalu terlambat skripsi karena tidak mampu menulis. Sering kali mereka tersesat di antara feedback, versi dokumen, dan keputusan yang saling bergantung."
- **Solution hook:** "ThesisTwin turns a thesis from a static document into a navigable research journey."
- **Differentiator:** "Unlike an AI writer, ThesisTwin maps the logic of a research project, remembers why decisions were made, and shows what must change when one decision changes."
- **Closing:** "We are not replacing supervisors or student thinking. We are removing the coordination and consistency barriers that prevent both from working effectively."

---

## 18. Kesimpulan

ThesisTwin memandang skripsi sebagai perjalanan akademik yang membutuhkan navigasi, continuity, dan accountability. Solusi ini mengurangi hambatan yang konkret: feedback yang tersebar, keputusan yang terlupakan, perubahan yang tidak sinkron, serta ketidakjelasan langkah berikutnya.

Nilai AI pada ThesisTwin tidak terletak pada kemampuannya menghasilkan lebih banyak teks. Nilainya terletak pada kemampuan untuk mengekstrak struktur, membangun dependency, menghubungkan evidence, mendeteksi perubahan, dan membantu manusia mengambil keputusan dengan konteks yang lebih lengkap.

Dengan scope MVP yang terkontrol, human-in-the-loop, serta metrik yang dapat diuji, ThesisTwin memiliki kesesuaian kuat dengan Case 1 STACK 2026: mengurangi barrier pada student journey melalui solusi digital yang memiliki user journey jelas dan manfaat terukur.

---

## Referensi

1. GDGoC ITB. (2026). *Handbook STACK 2026. Case 1: Smarter Campus and Learning.*
2. Kementerian Pendidikan Tinggi, Sains, dan Teknologi. (2026). *Statistik Pendidikan Tinggi 2025.* https://kemdiktisaintek.go.id/library/book/statistik-pendidikan-tinggi-2025
3. Xu, Z., Zhao, Y., Patwardhan, M., Vig, L., & Cohan, A. (2025). *Can LLMs Identify Critical Limitations within Scientific Research? A Systematic Evaluation on AI Research Papers.* ACL 2025. https://aclanthology.org/2025.acl-long.1009/
4. de Wynter, A. (2025). *Awes, Laws, and Flaws From Today's LLM Research.* Findings of ACL 2025. https://aclanthology.org/2025.findings-acl.664/
5. Wu, S., et al. (2026). *Can AI Be a Good Peer Reviewer? A Survey of Peer Review Process, Evaluation, and the Future.* ACL 2026. https://aclanthology.org/2026.acl-long.1504/
6. Gao, M., Hu, X., Yin, X., Ruan, J., Pu, X., & Wan, X. (2025). *LLM-based NLG Evaluation: Current Status and Challenges.* Computational Linguistics, 51(2), 661–687. https://aclanthology.org/2025.cl-2.9/
