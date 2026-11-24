# rules/

Aturan alignment sebagai **data** (YAML/JSON), bukan kode. Katalog: [docs/alignment-rules.md](../../../docs/alignment-rules.md).
Menambah aturan = tambah satu file `R-<TOPIK>.yaml`, tanpa mengubah engine ([domain/rules.py](../app/domain/rules.py)).

Isi wajib tiap file:
- `id`, `priority` (high/medium/low), `title`, `why_flagged`, `suggested_clarification` (harus diakhiri tanda tanya, bukan vonis)
- `check`: salah satu `conflict` (a + b sama-sama ada), `requires` (source ada, target tidak ada), `required_sections` (istilah bagian wajib tidak ditemukan)
- `examples.fires` dan `examples.quiet`: contoh yang **harus** memicu dan yang **tidak boleh** memicu. `pytest` menjalankan semuanya otomatis.
- opsional: `programs` (default semua), `enabled`, `reviewed_by_supervisor` (default `false` sampai dosen metodologi meninjau)

Keterbatasan: pencocokan per kata kunci; negasi ("tidak memakai one-group") tidak dipahami. Karena itu temuan selalu berupa pertanyaan dan wajib dikonfirmasi manusia.
