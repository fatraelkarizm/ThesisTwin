# ThesisTwin

> *ThesisTwin does not write the student's thesis. It stops students from getting lost while finishing it.*

**AI-powered navigation and consistency engine for the undergraduate thesis journey.**
STACK 2026 · Case 1: Smarter Campus and Learning

---

## 1. Project and Team Identity

| | |
|---|---|
| **Project title** | ThesisTwin: AI-Powered Navigation and Consistency Engine for the Undergraduate Thesis Journey |
| **Selected case** | Case 1, Smarter Campus and Learning |
| **Team name** | `TODO` |
| **Members and roles** | `TODO` (name, role, contribution) |
| **Proposal version** | v1.0, 8 November 2026 ([full text](docs/source/01-proposal-full.md), [original PDF](docs/source/ThesisTwin_Detailed_Proposal_STACK_2026.pdf)) |

## 2. Problem and User Analysis

**Problem.** A thesis is not one document. It is a chain of dependent decisions: research problem, questions, objectives, variables, data, sampling, instrument, analysis, claims. Changing one link silently breaks others. Context is scattered across file versions, document comments, WhatsApp messages, personal notes, and decisions that were never written down. Students lose track of where they stand, why a revision was requested, and what a change affects. Supervisors re-read everything before every meeting to rebuild context.

**Target users**
- **Primary:** undergraduate students preparing a thesis proposal or thesis; thesis supervisors handling several students at once.
- **Supporting:** peer mentors, thesis coordinators, academic services.

**Supporting evidence.** Indonesia's *Statistik Pendidikan Tinggi 2025* records 289,670 students who dropped out, up 2.62% from 2024. This shows that study continuity matters, but it does **not** show that the thesis causes dropout, and we make no causal claim. Thesis-specific evidence comes from our discovery research: 7 student interviews and 1 supervisor interview (small, exploratory; being expanded toward the 15-30 students / 3-5 supervisors in the [research plan](docs/research-validation-plan.md)). Interview guide, consent template, anonymised log, and literature notes live in [docs/feedback/evidence/](docs/feedback/evidence/README.md). Any number we report is labelled as measured or simulated and must trace to a row in that log.

**What students and supervisors use today** (hypotheses to be validated; full comparison and test design in [docs/feedback/comparison.md](docs/feedback/comparison.md))

| Real practice | What it does well | Suspected gap |
|---|---|---|
| Word track changes / Compare, Google Docs version history | Familiar; text-level diff; comments anchored to text | Diff is by text, not by research element; no record of *why* a decision was made |
| WhatsApp / email feedback, supervision card | Fast; official record | Unstructured; not linked to the part of the proposal |
| Chatbot with project memory | Keeps documents and chat in one place | LLM judgement without deterministic rules, quote/page verification, or student/supervisor confirmation |
| Grammar checker, reference manager, task manager, LMS | Mature in their niche | Do not understand methodological links |

The strongest competitor to beat is *Word/Docs Compare + a chatbot with project memory*, not a plain chatbot.

## 3. Proposed Solution

**Value offered.** ThesisTwin builds a *digital twin of the thesis journey* and answers four questions: **Where am I? What is inconsistent? What changes if I revise this? What should I do next?**

**Scope (MVP).** Proposal Chapters 1-3, one campus guideline format, 5-10 alignment rules. Out of scope: auto-writing chapters, advanced statistical checks, full LMS integration, automatic defense-eligibility decisions, plagiarism detection, large-scale fine-tuning.

**Main user journey**
1. Student uploads the first proposal version.
2. ThesisTwin builds a research dependency graph.
3. It flags three alignment issues, each with page evidence.
4. Student enters supervisor feedback.
5. Feedback becomes structured action items.
6. Student uploads a revised version.
7. ThesisTwin shows what changed, what is resolved, and the new impact.
8. It generates a one-page supervision brief.

**Core differentiators (demo focus).** Our edge is the **version record** and the **supervision brief**:
- **Version record and diff at research-element level:** what changed, what is resolved, what a change affects.
- **Supervision brief:** one-page pre-meeting summary built from structured state, not free text.

**Supporting the core**
- **Dependency graph and Alignment Checker:** deterministic rules that raise verifiable *questions*, not verdicts, each with page evidence.
- **Feedback-to-Action:** vague feedback mapped to affected components and concrete actions, confirmed by the student.

**Later (not in the demo):** Thesis Route Map, Decision Memory, multi-supervisor conflict flag.
**Open item:** *Defense Stress-Test* appears in the abstract; its specification is pending (see [docs/feedback/features.md](docs/feedback/features.md)).

**Guardrails.** ThesisTwin never writes thesis content, never invents references, never decides that a methodology is correct, and never replaces supervisor approval. Every AI output is labelled AI-generated and goes through human confirmation.

## 4. Technical Design

**System flow**

```
Proposal / Guideline / Feedback / Versions
   -> Document ingestion (DOCX/PDF -> structure + page + hash)
   -> Redaction (NIM, phone, email)
   -> Structured extraction (LLM -> validated JSON)
   -> Thesis knowledge graph (nodes + edges + provenance)
   -> Constraint engine (deterministic) + Retrieval + LLM explanation
   -> Findings with evidence and confidence
   -> Human confirmation (AI-suggested -> Student -> Supervisor -> Resolved / Rejected)
   -> Route map / Action plan / Decision memory / Brief
```

**Core design decisions**
- The **LLM does not decide alignment.** A deterministic, configurable constraint engine does; the LLM only extracts and explains.
- Every node and finding carries **evidence** (document + page) or is marked *needs confirmation*.
- Document versions are **append-only**; superseded nodes are marked, never deleted.

**Extraction error mitigation** (implemented and tested in `apps/api`; details in [docs/feedback/gap.md](docs/feedback/gap.md) §5)

| Risk | Mitigation |
|---|---|
| Wrong page | Page numbers come from the parser, never from the LLM; the cited page must exist |
| Hallucinated quote | LLM must return a verbatim `quote`; it is fuzzy-matched (character level, tolerates OCR slips) against that page; failure downgrades the element to *needs confirmation* |
| Invalid JSON | Schema validation, bounded retries, then manual confirmation instead of guessing |
| PII sent to the LLM | Deterministic redaction (NIM, phone, email) before any LLM call |
| Unknown accuracy | Precision/recall per element type and evidence correctness against a labelled gold set |
| Equations / non-text | *Not yet handled*: to be flagged for manual confirmation |

**Technologies** (provisional, to be finalised via ADRs)

| Layer | Choice |
|---|---|
| Frontend | Next.js (App Router), TypeScript, Tailwind CSS |
| Backend | FastAPI, Pydantic v2, SQLAlchemy 2 |
| Database | SQLite for now; PostgreSQL + pgvector planned |
| Graph | Relational model first |
| AI | LLM with structured JSON output behind a provider adapter |
| Security | Consent gate, redaction before LLM, RBAC, audit log |

**Data sources.** User-uploaded proposals and feedback, campus thesis guidelines, program rubrics, user-supplied literature. Simulated data is always labelled.

**Documentation:** [technical design](docs/technical-design.md) · [data model](docs/data-model.md) · [alignment rules](docs/alignment-rules.md) · [folder structure and component rules](docs/worktree.md)

### Run locally

```bash
# Frontend -> http://localhost:3000
cd apps/web && npm install && npm run dev

# Backend -> http://localhost:8000/docs
cd apps/api && python -m venv .venv && . .venv/Scripts/activate
pip install -e ".[dev]" && uvicorn app.main:app --reload
```

Quality checks: `npm run lint && npm run typecheck && npm run build` (web); `ruff check . && pytest` (api).

## 5. Development Plan

**Milestones** (full breakdown in [step-plan](docs/step-plan.md)). Dates marked `TODO` must be filled from the official STACK 2026 calendar.

| Phase | Date | Focus | Deliverable | Status |
|---|---|---|---|---|
| Preliminary | `TODO` | Problem validation | Abstract, early interviews | Done. Score 86.0/100 ([feedback](docs/feedback/README.md)) |
| Semifinal | `TODO` | Product definition | Proposal, user journey, prototype design | In progress |
| Checkpoint | **30 Nov 2026** | Extraction on real proposals | Extract elements from 10 proposals (abstract commitment) | Not reached; extraction pipeline built, no real proposals processed yet |
| Pre-final | `TODO` | Core build | Parser, graph, rules, feedback mapping | Not started beyond parser/verification |
| Final Day | `TODO` | Working demo | End-to-end core interaction and test results | Not started |
| Post-hackathon | `TODO` | Pilot | One study program (Mathematics, per abstract) | Planned |

**Current progress** (honest status)
- Done: full documentation set; project scaffold; domain UI components with **simulated, labelled** data; backend status state machine, evidence invariant, SQLite tables (findings, evidence, audit log); PDF page parser; PII redaction; extraction service with schema retry; quote/page verification; accuracy metrics. All unit-tested with a fake LLM.
- Not yet built: a real LLM provider (ADR-003), DOCX parsing, knowledge graph, constraint engine, feedback mapping, version diff, authentication. No real proposal has been processed yet.

**Member contributions.** `TODO`

**Planned Final Day tasks.** End-to-end demo of the 8-step core flow ([demo script](docs/pitch-and-demo-script.md)), baseline-versus-treatment evaluation, privacy and guardrail hardening, three consecutive clean demo runs with cached fallback data.

## 6. Validation and Impact

**Validation plan** ([details](docs/research-validation-plan.md))
- *Discovery:* 15-30 students, 3-5 supervisors, 1-2 coordinators.
- *Small evaluation set:* 20-30 anonymised proposals and 50-100 feedback snippets, labelled by at least two evaluators; if real documents are unavailable, a **labelled synthetic set**.
- *Experiment:* baseline (LLM prompted to "review consistency") versus treatment (extraction + graph + constraints + retrieval).

**Initial targets (hypotheses, not results)**

| Goal | Metric | Target |
|---|---|---|
| Save time (abstract target) | Supervisor/student review time | down 50% (hypothesis) |
| Save time | Time to build an action plan | down 30% or more |
| Follow-through | Feedback turned into action items | 80% or more |
| Accuracy | Alignment finding precision after confirmation | 75% or more |
| Provenance | Findings with a valid source | 90% or more |
| Usability | Task completion / SUS | 80% or more / 70 or more |

**Expected benefit.** Less time rebuilding context, fewer late-found inconsistencies, clearer supervision meetings.

**Risks and mitigations** ([risk register](docs/risk-register.md))

| Risk | Mitigation |
|---|---|
| AI misjudges a method | Evidence, confidence, deterministic rules, supervisor confirmation |
| Student over-reliance | No auto-writing; clarification questions instead of answers |
| Ambiguous feedback misread | Show interpretation and ask the student to confirm |
| Document leak | Encryption, RBAC, retention policy, permanent delete |
| Supervisor feels replaced | Positioned as a preparation and memory layer |
| Campus rules differ | Campus-specific policy packs |

**Privacy.** Explicit consent before upload, redaction of NIM / phone / email before any LLM call, minimum context sent, identity separated from research content, no training on user documents without separate consent, permanent deletion on request. Whether the chosen LLM provider stores or trains on data **still needs to be verified**.

**Sustainability.** Institutional licences per program or faculty; free student tier with a project limit; campus-hosted deployment for high-privacy needs; student thesis content is never monetised.

## 7. References and Declaration

**Third-party resources**
- Next.js, React, Tailwind CSS, FastAPI, Pydantic, SQLAlchemy (open source).
- Shared Claude Code agent skills in `.claude/skills/` (caveman, ponytail, ui-ux-pro-max, antislop, Vercel React skills, Supabase Postgres skills, FastAPI skill, Anthropic webapp-testing, obra/superpowers). Sources are recorded in [skills-lock.json](skills-lock.json).

**Material AI assistance.** The documentation set, project scaffold, and initial code in this repository were drafted with the help of Claude (via Claude Code) and reviewed by the team. The product itself is designed so that AI never writes the student's thesis.

**References**
1. GDGoC ITB. (2026). *Handbook STACK 2026. Case 1: Smarter Campus and Learning.*
2. Kementerian Pendidikan Tinggi, Sains, dan Teknologi. (2026). *Statistik Pendidikan Tinggi 2025.* https://kemdiktisaintek.go.id/library/book/statistik-pendidikan-tinggi-2025
3. Xu, Z., Zhao, Y., Patwardhan, M., Vig, L., & Cohan, A. (2025). *Can LLMs Identify Critical Limitations within Scientific Research?* ACL 2025. https://aclanthology.org/2025.acl-long.1009/
4. de Wynter, A. (2025). *Awes, Laws, and Flaws From Today's LLM Research.* Findings of ACL 2025. https://aclanthology.org/2025.findings-acl.664/
5. Wu, S., et al. (2026). *Can AI Be a Good Peer Reviewer?* ACL 2026. https://aclanthology.org/2026.acl-long.1504/
6. Gao, M., et al. (2025). *LLM-based NLG Evaluation: Current Status and Challenges.* Computational Linguistics, 51(2), 661-687. https://aclanthology.org/2025.cl-2.9/

**Originality declaration.** `TODO`: to be signed by the team members. This is a signed document and cannot be completed by a tool.

---

## Contributing

All work happens on the `features` branch; never commit to `main` directly. Rules for contributors and AI agents: [AGENTS.md](AGENTS.md) · [CLAUDE.md](CLAUDE.md). Full documentation index: [docs/README.md](docs/README.md).
