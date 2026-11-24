import type { Finding } from "@/types/domain";

// DATA SIMULASI (berlabel di UI). Bukan hasil analisis proposal nyata.

export interface VersionSummary {
  version: number;
  openFindings: number;
  summary: string;
  uploadedAt: string;
  sectionsChecked: number;
  sectionsTotal: number;
  latest: boolean;
}

export const versions: VersionSummary[] = [
  {
    version: 2,
    openFindings: 2,
    summary: "RQ1 dirumuskan ulang sebagai asosiasi; tujuan 2 belum terpetakan ke instrumen.",
    uploadedAt: "22 Nov 2026, 14.10",
    sectionsChecked: 5,
    sectionsTotal: 6,
    latest: true,
  },
  {
    version: 1,
    openFindings: 4,
    summary: "Pertanyaan kausal diuji dengan desain one-group pre-test/post-test.",
    uploadedAt: "8 Nov 2026, 09.45",
    sectionsChecked: 3,
    sectionsTotal: 6,
    latest: false,
  },
];

export const stats = { verified: 12, extracted: 14, commentsDone: 4, commentsTotal: 6, waitingDays: 2 };

export const findings: Finding[] = [
  {
    id: "F-001",
    ruleId: "R-CAUSAL-01",
    priority: "high",
    title: "Pertanyaan kausal, desain belum mendukung inferensi kausal",
    whyFlagged: "RQ1 memakai kata 'pengaruh', sedangkan desainnya one-group pre-test/post-test tanpa kelompok kontrol.",
    suggestedClarification: "Apakah RQ1 ingin dirumuskan sebagai perubahan skor, atau desain perlu kelompok pembanding?",
    evidence: [
      { element: "RQ1", document: "proposal_v2", page: 5 },
      { element: "Desain", document: "proposal_v2", page: 21 },
    ],
    confidence: 0.8,
    status: "ai_suggested",
    aiGenerated: true,
  },
  {
    id: "F-002",
    ruleId: "R-OBJ-02",
    priority: "medium",
    title: "Tujuan 2 belum terpetakan ke instrumen",
    whyFlagged: "Tidak ditemukan instrumen yang mengukur variabel pada Tujuan 2.",
    suggestedClarification: "Instrumen mana yang dimaksudkan untuk mengukur variabel Tujuan 2?",
    evidence: [],
    confidence: 0.55,
    status: "needs_user_confirmation",
    aiGenerated: true,
  },
];
