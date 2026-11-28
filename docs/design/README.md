# Design — Referensi & Keputusan Visual

Referensi utama: **Notalx** ([01-notalx-dashboard.png](references/01-notalx-dashboard.png)). Dua referensi lain dipakai sebagian. Bagian "Tidak diambil" sama pentingnya dengan bagian "Diambil", karena beberapa pola referensi melanggar guardrail produk ([AGENTS.md](../../AGENTS.md) §3).

## 1. Referensi

| File | Produk | Peran |
|---|---|---|
| [01-notalx-dashboard.png](references/01-notalx-dashboard.png) | Notalx (writing assistant) | **Acuan utama**: struktur dashboard, kartu, panel Tools |
| [02-journal-dashboard.png](references/02-journal-dashboard.png) | Journal app | Header sapaan, kartu insight berwarna, linimasa entri |
| [03-notelify-editor.png](references/03-notelify-editor.png) | Notelify (editor) | Hanya struktur tiga kolom; **bukan** fitur AI-nya |
| [Bimbingan – Thesis Progress Tracker](https://dribbble.com/shots/15731015-Bimbingan-Thesis-Final-Project-Progress-Tracker-Mobile-App) (Dribbble) | Pelacak skripsi | Beranda: posisi di alur + satu langkah berikutnya (§2a) |
| [Thesis AI Assistant](https://dribbble.com/shots/25547028-Thesis-AI-Assistant) (Dribbble) | Asisten skripsi | Hanya halaman awal yang tenang untuk pengguna baru; kolom chat "tulis apa saja" **tidak** diambil (guardrail 1) |

## 2. Yang diambil dari Notalx

| Pola Notalx | Versi ThesisTwin |
|---|---|
| Sidebar kiri: logo, menu, item aktif berbingkai | Dashboard, Proposal, Temuan, Versi, Supervision Brief, Defense Stress-Test. Menu yang belum dibangun = non-aktif + label "Segera" |
| Topbar: pencarian + "Upload File" + tombol "New Document" | Pencarian + "Unggah Draf" + tombol utama "Proyek Baru" |
| Judul bagian + subjudul kecil + ikon info | Setiap kartu: judul tebal, satu baris penjelasan abu-abu |
| **Kartu dokumen** dengan badge huruf, label kecil, angka besar berwarna | **Kartu versi proposal**: badge versi, label "Temuan terbuka", angka besar, ringkasan, waktu unggah |
| **Panel "Tools"**: ikon, judul, badge kecil, deskripsi satu baris, chevron | **Panel Tools ThesisTwin**: Cek Konsistensi, Bandingkan Versi, Supervision Brief, Defense Stress-Test. Badge = **status nyata** ("Data simulasi", "Segera"), bukan angka pertumbuhan |
| Ubin statistik: ikon, label, angka besar, satuan kecil | Elemen terverifikasi, komentar ditangani, temuan terbuka (berlabel simulasi) |
| Daftar "Suggestions" dengan aksi "Mark as Done" dan badge waktu | Daftar temuan dengan aksi **Konfirmasi / Tolak** (state machine), badge prioritas |
| "Recent Documents" dengan bar progres bersegmen | Riwayat versi dengan bar **bagian yang sudah dicek** (bersegmen) |
| Warna utama hijau, latar abu sangat muda, kartu putih, sudut membulat, bayangan halus | Struktur diadopsi; warna & huruf mengikuti arah **kertas & tinta** (§4) |

## 2a. Revisi alur (2026-11-28)

Audit UI menemukan dua navigasi yang urutan & namanya berbeda (sidebar vs penunjuk langkah), dashboard kosong berisi data simulasi, dan daftar temuan yang terlalu panjang. Perubahan:

| Sebelumnya | Sekarang |
|---|---|
| Sidebar: Dashboard, Proposal, Temuan, Riwayat Versi, Supervision Brief, Defense Stress-Test | Beranda, lalu **5 langkah bernomor** yang diturunkan dari `copy.steps` (tidak bisa beda dari penunjuk langkah), lalu Pengaturan. Penunjuk langkah di header halaman hanya tampil di mobile |
| Dashboard: kartu versi, antrean semua temuan, panel Tools, ubin statistik | **Beranda**: kartu *Langkah berikutnya* (satu aksi), daftar 5 langkah dengan status nyata, 3 temuan prioritas tertinggi. Logika di `features/dashboard/journey.ts` |
| Pengguna baru melihat data simulasi | Onboarding: apa yang dilakukan ThesisTwin, satu tombol unggah, apa yang terjadi setelahnya. Tidak ada data contoh |
| Topbar: pencarian non-aktif, dua tombol unggah, nama proyek statis | Judul & prodi proyek aktif + satu tombol "Unggah draf" |
| Unggah: input file bawaan, ID proyek & SHA-256, tautan kecil | Area tarik-lepas, judul proyek, tombol utama "Tinjau N temuan" setelah unggah |
| Brief: kotak teks mentah + tombol | **Pratinjau persis halaman dosen** (komponen bersama `BriefDocument`; tombol keputusan dosen diganti keterangan) + panel "Kirim ke dosen": buat/salin tautan, salin teks untuk chat |
| Judul halaman berbahasa campur (Defense Stress-Test, Riwayat Versi, Supervision Brief) | Judul = nama di sidebar (Latihan Seminar, Perubahan Versi, Kirim ke Dosen) |
| Ikon ⓘ di setiap deskripsi section | Dihapus: tampak bisa diklik padahal tidak |
| Temuan: semua detail terbuka, aturan yang sama berulang | Saringan (perlu ditinjau / prioritas tinggi / sudah ditinjau / semua), temuan per aturan digabung jadi satu kartu, arah & landasan dilipat |

## 3. Yang sengaja **tidak** diambil

| Pola referensi | Alasan |
|---|---|
| "Start generating", "AI Writing Tools", "Rephrase/Shorten Text" (Notalx), toolbar **Assistant** di editor (Notelify) | ThesisTwin **tidak menulis teks skripsi** (guardrail 1, abstrak §5) |
| Skor grammar "96 / 70" dan delta "+20% from last month" | Angka tampak seperti hasil nyata. Kami tidak punya skor tunggal yang jujur; tampilkan hitungan temuan dan status, berlabel simulasi |
| Kartu "Upgrade to Pro" | Bukan prioritas demo. Diganti kartu "Bagikan brief ke dosen (tanpa akun)" sesuai abstrak |
| Grafik tren mingguan | Belum ada data longitudinal; ditunda sampai ada riwayat nyata |
| Streak, emoji suasana hati (journal) | Tidak relevan; berisiko terasa main-main untuk konteks akademik |
| "AI Insight" tanpa label | Semua konten AI wajib berlabel `Dibuat AI` (guardrail 5) |
| Persentase progres per bab (Bimbingan) | Kami tidak bisa mengukur "seberapa selesai" sebuah bab. Yang dihitung hanya langkah alur kerja yang benar-benar dilalui |

## 4. Token

Didefinisikan di [globals.css](../../apps/web/src/app/globals.css), dipakai lewat kelas Tailwind (`bg-brand`, `rounded-card`, `shadow-card`, dst.). Komponen tidak boleh memakai warna literal ([worktree.md](../worktree.md) §3.9).

**Arah "kertas & tinta"** (keputusan 2026-11-28, menggantikan biru 2026-11-24). Biru `#2563eb` + label ungu + Geist adalah kombinasi bawaan Tailwind/Next.js, sehingga aplikasi terlihat seperti buatan template (lihat skill antislop-ui). ThesisTwin mendampingi naskah yang sedang dibimbing, jadi identitasnya diambil dari kertas naskah, tinta, dan satu warna "pena pembimbing". Kontras dihitung, bukan ditebak.

**Selalu tema terang** (keputusan tim 2026-11-24): aplikasi tidak mengikuti mode gelap sistem; `globals.css` memakai `color-scheme: light`.

| Token | Nilai | Kontras / catatan |
|---|---|---|
| `background` | `#f6f4ee` | kertas hangat; latar sidebar dan kolom kanan |
| `surface` | `#ffffff` | lembar kerja dan kartu |
| `foreground` | `#1d1f24` | tinta: 14.99:1 di background |
| `muted` | `#5e5b53` | teks sekunder: 6.78:1 di surface, 6.16:1 di background |
| `line` | `#e4dfd3` | batas kartu (kartu rata, tanpa bayangan) |
| `brand` | `#1e5b46` | **satu-satunya aksen**: tombol utama, item aktif, angka kunci. Teks putih 7.95:1 |
| `brand-strong` / `brand-soft` | `#174836` / `#e2ede6` | 8.67:1 |
| `tone-info` | `#4a4538` / `#f1eee6` | label "Saran otomatis"/"Dibuat AI": pasir netral, tanpa ikon ✦ (8.23:1) |
| `tone-warning` | `#8a3a12` / `#f6e7d8` | oker bata untuk celah/peringatan (6.44:1) |
| `tone-danger` | `#8c1f1a` / `#f6dedb` | 7.05:1 |
| `tone-success` | `#2f5419` / `#e6f0e0` | 7.45:1 |
| `radius-card` | 8px | badge 4px, bukan kapsul |
| `shadow-card` | tidak ada | elevasi hanya lewat garis |

**Huruf:** judul `h1–h3` memakai **Source Serif 4** (rasa naskah akademik); isi dan UI memakai **IBM Plex Sans** (terbaca baik di ukuran kecil, tidak serupa bawaan Next.js); kode/tautan **IBM Plex Mono**.

## 5. Aturan tata letak

- Desktop: sidebar 240px + konten selebar maksimal `max-w-5xl`.
- Section **terbuka**: judul + deskripsi langsung di halaman; yang berbingkai hanya item di dalamnya (komponen `Section`). `Card` dipakai untuk formulir.
- < 1024px: kolom kanan turun ke bawah. < 768px: sidebar disembunyikan.
- Satu tombol utama (aksen hijau tua) per area. Aksi lain sekunder.
- **Satu konsep per halaman** (keputusan tim 2026-11-24, setelah halaman "Ruang Kerja" dinilai terlalu bercampur). Alur kerja proyek = 5 halaman berurutan: `/proyek` Isi Proposal → `/temuan` Cek Konsistensi → `/stress-test` Defense Stress-Test → `/versi` Riwayat Versi → `/brief` Supervision Brief. Semua memakai `ProjectPage`: label langkah, judul, satu kalimat "apa ini", penunjuk alur, isi, dan tautan "Langkah berikutnya".
- Detail panjang dilipat (`<details>`): kutipan elemen, form tambah manual, temuan yang sudah ditinjau.
- Angka besar hanya untuk hitungan yang bisa dipertanggungjawabkan; selalu sebut satuannya.
- Setiap layar yang memakai data simulasi menampilkan label **"Data simulasi"** yang terlihat.
