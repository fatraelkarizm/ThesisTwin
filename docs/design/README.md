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
| Topbar: pencarian + "Upload File" + tombol hijau "New Document" | Pencarian + "Unggah Draf" + tombol utama "Proyek Baru" |
| Judul bagian + subjudul kecil + ikon info | Setiap kartu: judul tebal, satu baris penjelasan abu-abu |
| **Kartu dokumen** dengan badge huruf, label kecil, angka besar berwarna | **Kartu versi proposal**: badge versi, label "Temuan terbuka", angka besar, ringkasan, waktu unggah |
| **Panel "Tools"**: ikon, judul, badge kecil, deskripsi satu baris, chevron | **Panel Tools ThesisTwin**: Cek Konsistensi, Bandingkan Versi, Supervision Brief, Defense Stress-Test. Badge = **status nyata** ("Data simulasi", "Segera"), bukan angka pertumbuhan |
| Ubin statistik: ikon, label, angka besar, satuan kecil | Elemen terverifikasi, komentar ditangani, temuan terbuka (berlabel simulasi) |
| Daftar "Suggestions" dengan aksi "Mark as Done" dan badge waktu | Daftar temuan dengan aksi **Konfirmasi / Tolak** (state machine), badge prioritas |
| "Recent Documents" dengan bar progres bersegmen | Riwayat versi dengan bar **bagian yang sudah dicek** (bersegmen) |
| Warna utama hijau, latar abu sangat muda, kartu putih, sudut membulat besar, bayangan halus | Diadopsi sebagai token (§4) |

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
| `brand` | `#15803d` | `#4ade80` | Hijau ala Notalx; kontras teks putih di atas `brand` ≈ 5:1 (AA) |
| `brand-soft` | `#dcfce7` | `#14532d` | Latar item aktif, ikon |
| `background` | `#f6f7f6` | `#0c0f0d` | Latar halaman abu-hijau sangat muda |
| `surface` | `#ffffff` | `#151a17` | Kartu |
| `line` | `#e3e7e4` | `#2a322d` | Batas kartu tipis |
| `muted` | `#5b645e` | `#a3aca6` | Teks sekunder; ≥ 4.5:1 di atas `surface` |
| `radius-card` | 16px | | Sudut kartu besar seperti referensi |
| `shadow-card` | sangat halus | | Bayangan tipis, tidak dramatis |

## 5. Aturan tata letak

- Desktop: sidebar 240px + konten; konten dibagi **kolom utama + kolom kanan 340px** (pola Notalx).
- < 1024px: kolom kanan turun ke bawah. < 768px: sidebar disembunyikan.
- Satu tombol utama (hijau) per layar. Aksi lain sekunder.
- Angka besar hanya untuk hitungan yang bisa dipertanggungjawabkan; selalu sebut satuannya.
- Setiap layar yang memakai data simulasi menampilkan label **"Data simulasi"** yang terlihat.
