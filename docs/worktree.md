# Worktree — Struktur Folder, Tujuan, & Aturan Komponen

Dokumen ini adalah **kontrak struktur**. AI agent & kontributor wajib mengikutinya saat menambah file. Bila perlu menyimpang → ubah dokumen ini lewat PR dulu.

Rujukan: [technical-design.md](technical-design.md) · [data-model.md](data-model.md) · [alignment-rules.md](alignment-rules.md) · [../AGENTS.md](../AGENTS.md)

## 1. Peta Folder

```
ThesisTwin/
├── AGENTS.md / CLAUDE.md        # aturan agent (baca dulu)
├── .claude/skills/              # skill bersama tim
├── docs/                        # dokumentasi produk & teknis (source of truth = proposal)
│   └── adr/                     # Architecture Decision Records (ADR-001..)
├── apps/
│   ├── web/                     # Next.js frontend
│   │   └── src/
│   │       ├── app/             # ROUTING SAJA: page/layout/loading/error. Tanpa logika bisnis.
│   │       ├── components/
│   │       │   ├── ui/          # primitif generik (Button, Badge, Card). Tanpa tahu domain.
│   │       │   ├── domain/      # komponen sadar-domain reusable (StatusBadge, EvidenceChip, FindingCard)
│   │       │   └── features/    # rakitan per fitur (shell/, dashboard/, graph/, findings/, brief/). Tidak diimpor lintas fitur; shell/ hanya dipakai app/layout.tsx.
│   │       ├── lib/             # api-client, util murni, konstanta
│   │       ├── types/           # tipe domain bersama (cermin skema API)
│   │       └── hooks/           # hook reusable (tanpa JSX)
│   └── api/                     # FastAPI backend
│       ├── app/
│       │   ├── api/             # router tipis: parse request → panggil service → return schema
│       │   ├── core/            # config, security, logging
│       │   ├── domain/          # LOGIKA MURNI tanpa IO: status machine, constraint engine, redaction
│       │   ├── schemas/         # Pydantic: request/response & kontrak ekstraksi LLM
│       │   ├── services/        # orkestrasi use-case (ingestion, extraction, brief)
│       │   ├── llm/             # antarmuka + adapter provider LLM (satu-satunya tempat memanggil LLM)
│       │   ├── parsing/         # DOCX/PDF -> {halaman: teks}; nomor halaman dari parser, bukan LLM
│       │   └── db/              # model SQLAlchemy, sesi, migrasi
│       ├── rules/               # aturan alignment sebagai DATA (YAML/JSON), bukan kode
│       ├── config/              # ontologi (tipe, relasi, dampak, label) & kosakata judul bab sebagai DATA
│       └── tests/               # cermin struktur app/
└── (eval/, datasets/ — nanti, M9)
```

## 2. Tujuan & Batas Tiap Folder

| Folder | Boleh | Dilarang |
|---|---|---|
| `web/src/app` | routing, fetch data server, merakit fitur | logika bisnis, styling ad-hoc, komponen reusable |
| `web/components/ui` | primitif generik, variant via props | import dari `domain/`, `features/`, `lib/api`; teks Indonesia hard-coded |
| `web/components/domain` | tampilan entitas domain (status, evidence, confidence) | fetch data, state global, import dari `features/` |
| `web/components/features/<x>` | state & komposisi satu fitur | import dari `features/<y>` |
| `web/lib` | util murni, API client bertipe | JSX, import dari `components/` |
| `api/app/api` | routing, auth dependency, status code | logika domain, query SQL langsung, panggilan LLM |
| `api/app/domain` | fungsi/kelas murni, deterministik | IO (DB, HTTP, file, LLM), `datetime.now()` langsung (inject clock) |
| `api/app/services` | orkestrasi: DB + LLM + domain | aturan bisnis inti (taruh di `domain/`) |
| `api/app/storage.py` | simpan/baca file unggahan | logika bisnis |
| `api/app/parsing` | membaca file, memetakan halaman | memanggil LLM, aturan bisnis |
| `api/app/llm` | prompt, panggilan provider, validasi skema, retry | keputusan alignment |
| `api/rules` | aturan sebagai data + metadata (id, prioritas, pesan) | kode |

Arah dependensi satu arah: `api → services → domain` dan `services → llm/db`. `domain` tidak mengimpor siapa pun. Frontend: `app → features → domain → ui`.

## 3. Aturan Ketat Komponen Reusable (Frontend)

Berlaku untuk semua file di `components/ui` dan `components/domain`.

1. **Satu komponen = satu file = satu tanggung jawab.** Nama file = nama komponen (`StatusBadge.tsx`). Tanpa barrel `index.ts` besar.
2. **Props bertipe eksplisit**, `interface XProps`. Tanpa `any`. Tanpa boolean-prop berlipat — pakai `variant` union (`"success" | "warning"`) atau compound components.
3. **Presentational murni.** `ui/` & `domain/` tidak fetch, tidak membaca router/global store. Data & callback masuk via props.
4. **Semua status dari satu sumber:** `FindingStatus`, `NodeStatus`, `Priority` didefinisikan sekali di `types/` dan dipetakan ke tampilan di **`StatusBadge`** saja. Dilarang membuat badge status sendiri di fitur.
5. **Evidence wajib terlihat.** Menampilkan node/finding memakai `EvidenceChip` (dokumen + halaman) atau `NeedsConfirmation`. Dilarang merender temuan tanpa keduanya.
6. **Label AI wajib.** Konten AI dirender lewat `AiLabel`/prop `aiGenerated`; tidak boleh tampak seperti tulisan manusia.
7. **Bahasa temuan = pertanyaan/peringatan.** Komponen tidak boleh punya copy bernada vonis ("Salah", "Gagal"). Copy dari konstanta di `lib/copy.ts`.
8. **Aksesibel:** kontras ≥ WCAG AA, fokus keyboard terlihat, status tidak hanya warna (ikon/teks), target sentuh ≥ 44px. Lihat skill `antislop-human`.
9. **Styling:** Tailwind + token (`tailwind` theme). Tanpa warna/ukuran literal di komponen. Tanpa CSS inline kecuali nilai dinamis.
10. **Tanpa efek samping di render.** Hindari `useEffect` untuk data turunan. Ikuti `vercel-react-best-practices`.
11. **Test:** tiap komponen `domain/` punya test render + a11y dasar; tiap varian terdokumentasi di test.
12. **Buat baru hanya jika** tidak ada padanan di `ui/`/`domain/` **dan** dipakai ≥2 tempat. Selain itu, tetap lokal di fitur.

### Daftar komponen inti (MVP) & kontraknya

| Komponen | Lokasi | Props kunci | Catatan |
|---|---|---|---|
| `Button`, `Badge`, `Card`, `Dialog` | `ui/` | `variant`, `size` | generik; tanpa domain |
| `StatusBadge` | `domain/` | `status: FindingStatus \| NodeStatus` | satu-satunya pemetaan status → tampilan |
| `PriorityTag` | `domain/` | `priority: "high" \| "medium" \| "low"` | warna + ikon |
| `ConfidenceMeter` | `domain/` | `value: 0..1` | tampilkan sebagai teks juga; label "perkiraan AI" |
| `EvidenceChip` | `domain/` | `document`, `page` | klik → buka sumber |
| `AiLabel` | `domain/` | — | wajib untuk konten AI |
| `FindingCard` | `domain/` | `finding: Finding`, `onConfirm`, `onReject` | memakai StatusBadge + EvidenceChip + `why_flagged` |
| `BriefDocument` | `domain/` | `brief`, `stress`, `onDecide?`, `onRate?` | isi Supervision Brief; tanpa handler = pratinjau mahasiswa |
| `FindingGuidance` | `domain/` | `finding` (directions, basis, sourceTypes, references) | arah + landasan + rujukan, dilipat; dipakai `FindingCard` dan kartu kelompok temuan |
| `NodeDetailPanel` | `features/graph` | `node` | sumber, status, feedback terkait |

## 4. Aturan Ketat Modul Reusable (Backend)

1. **Router tipis** (≤ ~15 baris per handler): validasi lewat schema → service → return schema.
2. **`domain/` murni & deterministik**; dapat diuji tanpa DB/jaringan. Waktu & acak di-inject.
3. **Satu state machine** untuk status temuan/node di `domain/status.py`. Transisi tidak valid → `InvalidTransition`. Tidak ada kode lain yang boleh menulis status langsung.
4. **LLM hanya lewat `llm/`.** Output LLM selalu divalidasi Pydantic; invalid → retry terbatas → `needs_user_confirmation`, bukan menebak.
5. **Redaction di pintu masuk LLM** (`domain/redaction.py`); service tidak boleh memanggil `llm/` dengan teks mentah.
6. **Constraint engine membaca `rules/`, ontologi & ekstraksi membaca `config/`** (data, dimuat di `services/config.py`, dioper ke `domain/`). Menambah aturan, tipe elemen, relasi, atau judul bab = menambah data + test, bukan mengubah engine.
7. **Evidence invariant:** pembuat `Finding`/`Node` menolak input tanpa sumber kecuali `status=needs_user_confirmation`.
8. **Audit:** setiap perubahan status menulis `audit_log` (actor, action, entity, waktu).
9. **Schema = kontrak:** perubahan schema = perubahan `web/src/types/` pada PR yang sama.
10. **Tes:** `domain/` wajib unit test; `services/` test dengan fake LLM; tidak ada test yang memanggil LLM sungguhan.

## 5. Konvensi Penamaan

| Hal | Konvensi |
|---|---|
| React komponen / file | `PascalCase.tsx` |
| Hook | `useCamelCase.ts` |
| util / non-komponen TS | `kebab-case.ts` |
| Python modul | `snake_case.py` |
| Rule ID | `R-<TOPIK>-<NN>` (mis. `R-CAUSAL-01`) sesuai [alignment-rules.md](alignment-rules.md) |
| Branch | hanya `features` |
| ADR | `docs/adr/ADR-NNN-judul.md` |

## 6. Checklist Sebelum Menambah File/Komponen
- [ ] Sudah cari padanan yang ada di `ui/`, `domain/`, `lib/`, `services/`?
- [ ] Ada di folder yang benar menurut §2 (arah dependensi aman)?
- [ ] Menyentuh guardrail ([AGENTS.md](../AGENTS.md) §3)? Bila ya, ada test?
- [ ] Merujuk `FR-xxx`/`Txx.x`?
- [ ] Lint + typecheck + test lulus (bukti output, bukan asumsi)?
