export type Status =
  | "ai_suggested"
  | "needs_user_confirmation"
  | "student_confirmed"
  | "supervisor_confirmed"
  | "rejected"
  | "resolved";

export type Priority = "high" | "medium" | "low";

export interface Evidence {
  element: string;
  document: string;
  page: number;
  // DOCX/.tex tidak punya halaman tetap: lokasinya nomor bagian.
  unit?: "page" | "section";
}

export interface Finding {
  id: string;
  ruleId: string;
  priority: Priority;
  title: string;
  whyFlagged: string;
  suggestedClarification: string;
  evidence: Evidence[];
  confidence: number;
  status: Status;
  // true = isi temuan/evidence berasal dari AI (ekstraksi). Temuan aturan atas elemen
  // yang dimasukkan mahasiswa = false; label AI tidak boleh dipasang palsu.
  aiGenerated: boolean;
  basis?: string; // dasar aturan
  references?: string[]; // rujukan akademik (APA)
  sourceTypes?: SourceType[];
  directions?: Direction[]; // arah yang bisa dieksplorasi, bukan vonis atau teks skripsi
}

export type SourceType = "prodi_guideline" | "methodology" | "math_writing" | "publication_style";

export interface Direction {
  option: string;
  implication: string;
}
