# Data Model & Ontologi Thesis

**Versi:** 1.0 (draft) · Sumber: proposal §5.2, §9.2C · Entitas turunan (tabel) adalah usulan penyusun dokumen.

## 1. Ontologi Graph (dari proposal)

**Node:** Problem, Question, Objective, Concept, Variable · Population, Sample, Instrument, Data Source · Method, Analysis, Claim, Limitation · Feedback, Decision, Action, Milestone.

**Edge:** `addresses`, `requires`, `measured_by`, `analyzed_with`, `affected_by`, `approved_by`, `contradicts`, `supersedes`.

**Rantai dependency utama:**
`Problem → Questions → Objectives → Concepts/Variables → Evidence & Data → Population & Sampling → Instrument → Analysis → Claims`

Setiap node menyimpan: lokasi sumber, status verifikasi, versi terakhir, feedback terkait, hubungan dengan node lain.

## 2. Skema Relasional (usulan MVP)

```
users(id, role[student|supervisor|admin], name, email, ...)
projects(id, student_id, program_id, title, consent_at, created_at, deleted_at)
project_members(project_id, user_id, role[student|supervisor|mentor])
programs(id, name, policy_pack_id)
policy_packs(id, name, guideline_doc_id, milestones_json, rules_config_json)

documents(id, project_id, kind[proposal|guideline|rubric|literature|feedback_doc], filename, storage_key, sha256, created_at)
document_versions(id, document_id, version_no, sha256, parsed_json, uploaded_at)
passages(id, version_id, page, section, text_redacted, embedding)   -- pgvector

nodes(id, project_id, type, content, status[ai_suggested|student_confirmed|supervisor_confirmed|rejected|resolved],
      confidence, source_version_id, source_page, source_span, active_from_version, superseded_by)
edges(id, project_id, src_node, dst_node, type, status, created_by[ai|user])

findings(id, project_id, rule_id, priority, title, why_flagged, suggested_clarification,
         confidence, status, ai_generated, version_id, created_at)
finding_evidence(finding_id, node_id, page)

feedback_items(id, project_id, session_id, source[manual|pasted|docx_comment], author_id, original_text, interpretation,
               status, created_at)
feedback_nodes(feedback_id, node_id)
actions(id, feedback_id, text, status[todo|doing|done|dropped], node_id)

decisions(id, project_id, decision, reason, confirmed_by, decided_at, evidence_ref, status)
decision_nodes(decision_id, node_id)

sessions(id, project_id, held_at, notes)            -- sesi bimbingan
briefs(id, session_id, content_json, generated_at)
milestones(id, project_id, name, due, status)

audit_log(id, actor_id, action, entity, entity_id, at, meta_json)
```

## 3. Aturan Integritas

- Setiap `nodes` dan `findings` **wajib** punya sumber (`source_*` / `finding_evidence`) atau berstatus "needs confirmation".
- Perubahan status hanya melalui transisi valid (lihat [technical-design.md](technical-design.md) §4).
- `supervisor_confirmed` hanya dapat diset peran `supervisor`.
- Versi bersifat append-only; node lama ditandai `superseded_by`, bukan dihapus.
- Hard delete (permintaan pengguna) menghapus dokumen, passages, embedding, dan turunan.
