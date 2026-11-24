import type { Finding } from "@/types/domain";

// DATA SIMULASI (berlabel). Contoh dari docs/technical-design.md §5.
export const sampleFindings: Finding[] = [
  {
    id: "F-001",
    ruleId: "R-CAUSAL-01",
    priority: "high",
    title: "Potential alignment issue: pertanyaan kausal vs desain",
    whyFlagged: "Desain mungkin hanya mengidentifikasi asosiasi, bukan dampak kausal.",
    suggestedClarification: "Apakah RQ1 ingin dirumuskan ulang sebagai asosiasi, atau desain perlu diperkuat?",
    evidence: [
      { element: "RQ1", document: "proposal_v3", page: 5 },
      { element: "Desain", document: "proposal_v3", page: 21 },
      { element: "Analisis", document: "proposal_v3", page: 29 },
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
    status: "ai_suggested",
    aiGenerated: true,
  },
];
