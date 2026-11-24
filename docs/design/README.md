# Design — Referensi & Keputusan Visual

Referensi utama: **Notalx** ([01-notalx-dashboard.png](references/01-notalx-dashboard.png)). Dua referensi lain dipakai sebagian. Bagian "Tidak diambil" sama pentingnya dengan bagian "Diambil", karena beberapa pola referensi melanggar guardrail produk ([AGENTS.md](../../AGENTS.md) §3).

## 1. Referensi

| File | Produk | Peran |
|---|---|---|
| [01-notalx-dashboard.png](references/01-notalx-dashboard.png) | Notalx (writing assistant) | **Acuan utama**: struktur dashboard, kartu, panel Tools |
| [02-journal-dashboard.png](references/02-journal-dashboard.png) | Journal app | Header sapaan, kartu insight berwarna, linimasa entri |
| [03-notelify-editor.png](references/03-notelify-editor.png) | Notelify (editor) | Hanya struktur tiga kolom; **bukan** fitur AI-nya |

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
| Warna utama hijau, latar abu sangat muda, kartu putih, sudut membulat, bayangan halus | Struktur diadopsi; warna utama diganti **biru** (§4) |

## 3. Yang sengaja **tidak** diambil

| Pola referensi | Alasan |
|---|---|
| "Start generating", "AI Writing Tools", "Rephrase/Shorten Text" (Notalx), toolbar **Assistant** di editor (Notelify) | ThesisTwin **tidak menulis teks skripsi** (guardrail 1, abstrak §5) |
| Skor grammar "96 / 70" dan delta "+20% from last month" | Angka tampak seperti hasil nyata. Kami tidak punya skor tunggal yang jujur; tampilkan hitungan temuan dan status, berlabel simulasi |
| Kartu "Upgrade to Pro" | Bukan prioritas demo. Diganti kartu "Bagikan brief ke dosen (tanpa akun)" sesuai abstrak |
| Grafik tren mingguan | Belum ada data longitudinal; ditunda sampai ada riwayat nyata |
| Streak, emoji suasana hati (journal) | Tidak relevan; berisiko terasa main-main untuk konteks akademik |
| "AI Insight" tanpa label | Semua konten AI wajib berlabel `Dibuat AI` (guardrail 5) |

## 4. Token

Didefinisikan di [globals.css](../../apps/web/src/app/globals.css), dipakai lewat kelas Tailwind (`bg-brand`, `rounded-card`, `shadow-card`, dst.). Komponen tidak boleh memakai warna literal ([worktree.md](../worktree.md) §3.9).

| Token | Terang | Gelap | Catatan |
|---|---|---|---|
**Warna utama biru** (keputusan tim 2026-11-24, menggantikan hijau Notalx). Kontras dihitung, bukan ditebak.

**Selalu tema terang** (keputusan tim 2026-11-24): aplikasi tidak mengikuti mode gelap sistem; `globals.css` memakai `color-scheme: light`. Kolom "Gelap" di bawah hanya arsip nilai kalau mode gelap dihidupkan lagi; nilainya **tidak dipakai** di kode saat ini.

| Token | Terang | Gelap | Kontras / catatan |
|---|---|---|---|
| `brand` | `#2563eb` | `#60a5fa` | teks putih di atas brand 5.17:1; teks gelap di atas brand gelap 7.36:1 |
| `brand-strong` | `#1d4ed8` | `#93c5fd` | teks/ikon biru di atas `brand-soft`: 5.49:1 / 8.15:1 |
| `brand-soft` | `#dbeafe` | `#172554` | latar ikon, item aktif |
| `background` | `#f4f6fb` | `#0b1020` | latar sidebar dan kolom kanan (abu-biru sangat muda) |
| `surface` | `#ffffff` | `#131a2a` | kolom utama dan kartu |
| `line` | `#e3e8f0` | `#273149` | batas kartu tipis |
| `muted` | `#5b6475` | `#a3acbd` | teks sekunder: 5.96:1 di surface, 5.51:1 di background |
| `tone-info` | `#ede9fe` / `#5b21b6` | `#4c1d95` / `#ddd6fe` | **label AI berwarna ungu** (7.57:1) agar tidak tertukar dengan brand biru |
| `radius-card` | 12px | | kartu kecil-padat seperti referensi |
| `shadow-card` | sangat halus | | bayangan tipis, tidak dramatis |

## 5. Aturan tata letak

- Desktop: sidebar 240px + konten; konten dibagi **kolom utama putih + kolom kanan 360px berwarna `background`** (pola Notalx).
- Section **terbuka**: judul + deskripsi langsung di halaman; yang berbingkai hanya item di dalamnya (komponen `Section`). `Card` dipakai untuk formulir.
- < 1024px: kolom kanan turun ke bawah. < 768px: sidebar disembunyikan.
- Satu tombol utama (biru) per area. Aksi lain sekunder.
- **Satu konsep per halaman** (keputusan tim 2026-11-24, setelah halaman "Ruang Kerja" dinilai terlalu bercampur). Alur kerja proyek = 5 halaman berurutan: `/proyek` Isi Proposal → `/temuan` Cek Konsistensi → `/stress-test` Defense Stress-Test → `/versi` Riwayat Versi → `/brief` Supervision Brief. Semua memakai `ProjectPage`: label langkah, judul, satu kalimat "apa ini", penunjuk alur, isi, dan tautan "Langkah berikutnya".
- Detail panjang dilipat (`<details>`): kutipan elemen, form tambah manual, temuan yang sudah ditinjau.
- Angka besar hanya untuk hitungan yang bisa dipertanggungjawabkan; selalu sebut satuannya.
- Setiap layar yang memakai data simulasi menampilkan label **"Data simulasi"** yang terlihat.
