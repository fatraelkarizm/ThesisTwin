# Abstract STACK 2026 (transkripsi)

> Transkripsi dari [Abstract STACK 2026.pdf](Abstract%20STACK%202026.pdf) (2 halaman), yang diserahkan ke juri fase Preliminary (skor 86.0/100, lihat [../feedback/](../feedback/README.md)). Teks diketik ulang apa adanya; periksa PDF bila ada keraguan.
> **Prioritas sumber:** abstrak = komitmen yang dinilai juri. Bila bertentangan dengan [01-proposal-full.md](01-proposal-full.md), tandai konfliknya di [../feedback/baseline-audit.md](../feedback/baseline-audit.md) §3 dan putuskan sebagai tim.

| | |
|---|---|
| **Team name** | Reuni Kejauhan 🗿 |
| **Project title** | ThesisTwin: AI-Assisted Consistency Checking and Supervision Briefs for Undergraduate Thesis Proposals |
| **Selected case** | Case 1: Smarter Campus and Learning |
| **Members** | Alief Nuzula (leader), Fatra Al Khawarizmi, Renadi Wilantara |

## Abstract

**1. Problem.** Thesis proposals often stall between supervision meetings. A supervisor with several students must re-read each draft to find what changed and which comments were addressed, which slows feedback, while mismatches between research question, objectives, method, and analysis go unnoticed until the proposal seminar.

**2. Intended Users.** Final-year undergraduates at Indonesian universities writing a thesis proposal (Chapters 1–3), and their supervisors, who receive summaries without creating an account.

**3. Supporting Observations or Evidence.** In preliminary interviews with seven final-year students and one supervisor [1], students reported waiting 7–14 days for feedback per revision, and the supervisor noted that revised drafts rarely state what changed. Published studies agree: among 113 Indonesian supervisors, 51.3% named methodology choice as the main Chapter 3 problem and 45.1% said students struggle to tie Chapters 1–4 together [2], and four of six seminar proposals mismatched research questions and design [3]. Timely feedback keeps students on schedule [4], but supervisor workload affects how it is given [5]. A larger survey before the semifinal will test these findings.

**4. Proposed Solution and Core User Flow.** ThesisTwin keeps a structured record of the proposal across revisions and writes no thesis text. Planned core flow (first version, one Mathematics study program):
1. The student selects their program's rule set and uploads the initial or revised draft (DOCX/PDF) with the supervisor's latest comments.
2. The system extracts the research question, objectives, variables, method, and analysis into a dependency graph and flags mismatches, such as a causal question tested with a one-group pre-test/post-test design [3], and missing sections the program guideline requires.
3. Each revision yields a one-page Supervision Brief (what changed, which comments were addressed, which decisions remain open), sent as a PDF or chat message.
4. Before the seminar, a Defense Stress-Test turns the graph's weakest links into 3–5 likely examiner questions and asks the student to justify each choice.

**5. How It Differs from Existing Alternatives.** A general-purpose chatbot keeps no versioned record of the research design, cannot tell which supervisor comments were resolved, needs program rules pasted in each session, and will write thesis text on request. ThesisTwin keeps the record, applies the rules, and writes for the supervisor.

**6. Planned Technologies.** A web application (Next.js, FastAPI) with PostgreSQL and pgvector for guideline retrieval, an LLM that extracts and diffs research elements into a versioned JSON schema, and a deterministic rule engine so each flag cites a rule. Data: program guidelines and consented sample proposals, never used for training.

**7. Expected Benefit and Development Plan.** Expected benefit: a pilot with 10 students and 3 supervisors will measure review time per revision (target: 50% lower using the brief), extraction agreement with manual annotation (target: 80%), and supervisor ratings of stress-test questions (target: 4/5 relevance), each ≥ against an LLM-only baseline. Development plan: upload, extraction, and consistency checks will run end to end on 10 anonymized proposals by the semifinal (30 November), and the brief and stress-test will follow by Final Day (16 December). Supervisor adoption is the main risk, so supervisors never need an account.

## Source Acknowledgments

[1] Preliminary interviews conducted by the team with seven final-year undergraduate students and one thesis supervisor (unpublished data).
[2] Rangkuti, A. A., Listyasari, W. D., & Wahyuni, L. D. U. (2013). Kendala dosen dalam proses pembimbingan skripsi mahasiswa. *Perspektif Ilmu Pendidikan*, 27(2), 143–151.
[3] Hapsari, A. D. (2026). Mapping the challenges: An in-depth analysis of common flaws in six undergraduate ELT research proposals. *Bliss Journal: Broadening Linguistics, Literature, Education, and Study of Learning Media*, 2(1), 1–14.
[4] Syafi'i, A., Munir, A., Anam, S., & Suhartono, S. (2024). Unleashing the power of supervisory feedback in academic writing: Strategies for timely undergraduate thesis completion. *TEFLIN Journal*, 35(2), 330–351.
[5] Rahma, M., Laksmi, E. D., & Febrianti, Y. (2025). Balancing workload and thesis guidance: How supervisors provide effective feedback to students. *Scope: Journal of English Language Teaching*, 9(2), 785–796.
