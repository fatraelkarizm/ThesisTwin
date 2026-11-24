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
  aiGenerated: true;
}
