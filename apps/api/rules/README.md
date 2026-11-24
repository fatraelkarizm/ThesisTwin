# rules/

Aturan alignment sebagai **data** (YAML/JSON), bukan kode. Katalog: [docs/alignment-rules.md](../../../docs/alignment-rules.md).
Menambah aturan = tambah satu file `R-<TOPIK>.yaml`, tanpa mengubah engine ([domain/rules.py](../app/domain/rules.py)).

Isi wajib tiap file:
- `id`, `priority` (high/medium/low), `title`, `why_flagged`, `suggested_clarification` (harus diakhiri tanda tanya, bukan vonis)
- `check`: salah satu `conflict` (a + b sama-sama ada), `requires` (source ada, target tidak ada), `required_sections` (istilah bagian wajib tidak ditemukan), `forbidden_sections`, `count_match`, `missing_terms`, `mixed_patterns` (≥2 gaya penulisan, masing-masing ≥ `min_each` kali; regex dicocokkan pada teks asli, tulis dengan kutip tunggal YAML)
- `source_types`: asal landasan aturan, minimal satu dari `prodi_guideline`, `methodology`, `math_writing`, `publication_style`
- `directions`: **minimal dua** arah `{option, implication}` yang bisa dieksplorasi mahasiswa. Arah adalah pilihan beserta konsekuensinya, bukan perintah ("Hapus…", "Tambahkan…") dan bukan penilaian ("bagus/jelek/salah/benar"). `pytest` menolak keduanya.
- `examples.fires` dan `examples.quiet`: contoh yang **harus** memicu dan yang **tidak boleh** memicu. `pytest` menjalankan semuanya otomatis.
- opsional: `basis` (prinsip landasan), `references` (rujukan APA tanpa halaman sampai diverifikasi), `programs` (default semua), `enabled`, `reviewed_by_supervisor` (default `false` sampai dosen metodologi meninjau)

Keterbatasan: pencocokan per kata kunci; negasi ("tidak memakai one-group") tidak dipahami. Karena itu temuan selalu berupa pertanyaan dan wajib dikonfirmasi manusia.
