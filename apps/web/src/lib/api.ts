// Klien API bertipe. Tipe mencerminkan apps/api/app/schemas/project.py (ubah keduanya bersamaan).

import type { Finding, Priority, Status } from "@/types/domain";

export const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export interface ProjectOut {
  id: string;
  title: string;
  program: string;
  consent_at: string | null;
}

export interface VersionOut {
  id: string;
  version_no: number;
  filename: string;
  media_type: string;
  sha256: string;
  uploaded_at: string;
}

export interface UploadOut {
  version: VersionOut;
  created: boolean;
  pages: number;
  auto_elements: number;
  findings: number;
}

export type ElementType =
  | "research_question"
  | "objective"
  | "variable"
  | "population"
  | "method"
  | "instrument"
  | "analysis"
  | "claim"
  | "limitation";

export interface ElementOut {
  id: string;
  type: ElementType;
  content: string;
  quote: string;
  page: number;
  verified: boolean;
  source: "student" | "ai" | "auto";
  status: Status;
}

export interface FindingApi {
  id: string;
  rule_id: string;
  priority: Priority;
  title: string;
  why_flagged: string;
  suggested_clarification: string;
  confidence: number;
  status: Status;
  ai_generated: boolean;
  evidence: { element: string; document: string; page: number }[];
  basis: string | null;
  references: string[];
  suggestions: string[];
}

export interface CommentStatusOut {
  comment_id: string;
  author: string;
  text: string;
  anchor_text: string | null;
  state: "possibly_addressed" | "not_addressed" | "unknown";
  confirmed: boolean | null;
}

export interface BriefFindingOut {
  id: string;
  rule_id: string;
  title: string;
  priority: Priority;
  status: Status;
}

export interface BriefOut {
  project_title: string;
  program: string;
  from_version: number | null;
  to_version: number;
  generated_at: string;
  changes: string[];
  comments: CommentStatusOut[];
  open_findings: BriefFindingOut[];
  awaiting_supervisor: BriefFindingOut[];
  resolved_rules: string[];
  impacts: string[];
}

export interface GraphOut {
  nodes: ElementOut[];
  edges: { src: string; dst: string; type: string }[];
  gaps: { from_type: ElementType; to_type: ElementType; relation: string }[];
}

export interface ShareLinkOut {
  id: string;
  created_at: string;
  expires_at: string;
  revoked: boolean;
}

export interface StressQuestionOut {
  id: string;
  position: number;
  kind: "finding" | "gap" | "unverified" | "baseline";
  text: string;
  reason: string;
  answer: string | null;
  rating: number | null;
}

export interface ShareOut {
  token: string;
  path: string;
  expires_at: string;
}

/** Ubah temuan API (snake_case) ke tipe domain UI. DOCX/.tex: lokasi = nomor bagian. */
export function toFinding(f: FindingApi, unit: "page" | "section"): Finding {
  return {
    id: f.id,
    ruleId: f.rule_id,
    priority: f.priority,
    title: f.title,
    whyFlagged: f.why_flagged,
    suggestedClarification: f.suggested_clarification,
    evidence: f.evidence.map((e) => ({ ...e, unit })),
    confidence: f.confidence,
    status: f.status,
    aiGenerated: f.ai_generated,
    basis: f.basis ?? undefined,
    references: f.references ?? [],
    suggestions: f.suggestions ?? [],
  };
}

export class ApiError extends Error {
  constructor(
    message: string,
    readonly status: number,
  ) {
    super(message);
  }
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_URL}${path}`, init);
  } catch {
    throw new ApiError("Server tidak bisa dihubungi. Pastikan API berjalan.", 0);
  }
  if (!res.ok) {
    const body: unknown = await res.json().catch(() => null);
    const detail =
      body && typeof body === "object" && "detail" in body && typeof body.detail === "string"
        ? body.detail
        : `Permintaan gagal (${res.status}).`;
    throw new ApiError(detail, res.status);
  }
  return (await res.json()) as T;
}

const json = (body: unknown): RequestInit => ({
  method: "POST",
  headers: { "content-type": "application/json" },
  body: JSON.stringify(body),
});

export const api = {
  createProject: (title: string, program: string) =>
    request<ProjectOut>("/projects", json({ title, program })),
  giveConsent: (projectId: string) =>
    request<ProjectOut>(`/projects/${projectId}/consent`, { method: "POST" }),
  upload: (projectId: string, file: File) => {
    const form = new FormData();
    form.append("file", file);
    return request<UploadOut>(`/projects/${projectId}/documents`, { method: "POST", body: form });
  },
  project: (projectId: string) => request<ProjectOut>(`/projects/${projectId}`),
  deleteProject: async (projectId: string) => {
    const res = await fetch(`${API_URL}/projects/${projectId}`, { method: "DELETE" });
    if (!res.ok) throw new ApiError(`Gagal menghapus (${res.status}).`, res.status);
  },
  shareLinks: (projectId: string) => request<ShareLinkOut[]>(`/projects/${projectId}/share-links`),
  revokeLink: (projectId: string, linkId: string) =>
    request<ShareLinkOut>(`/projects/${projectId}/share-links/${linkId}/revoke`, { method: "POST" }),
  versions: (projectId: string) => request<VersionOut[]>(`/projects/${projectId}/versions`),
  elements: (versionId: string) => request<ElementOut[]>(`/versions/${versionId}/elements`),
  addElement: (versionId: string, body: { type: ElementType; content: string; quote: string; page: number }) =>
    request<ElementOut>(`/versions/${versionId}/elements`, json(body)),
  graph: (versionId: string) => request<GraphOut>(`/versions/${versionId}/graph`),
  stressTest: (versionId: string, regenerate = false) =>
    request<StressQuestionOut[]>(`/versions/${versionId}/stress-test${regenerate ? "?regenerate=true" : ""}`, {
      method: "POST",
    }),
  getStressTest: (versionId: string) => request<StressQuestionOut[]>(`/versions/${versionId}/stress-test`),
  answer: (questionId: string, answer: string) =>
    request<StressQuestionOut>(`/stress-questions/${questionId}/answer`, json({ answer })),
  sharedStress: (token: string) => request<StressQuestionOut[]>(`/share/${token}/stress-test`),
  rate: (token: string, questionId: string, score: number) =>
    request<StressQuestionOut>(`/share/${token}/stress-questions/${questionId}/rating`, json({ score })),
  check: (versionId: string) => request<FindingApi[]>(`/versions/${versionId}/check`, { method: "POST" }),
  findings: (versionId: string) => request<FindingApi[]>(`/versions/${versionId}/findings`),
  setStatus: (findingId: string, target: "student_confirmed" | "rejected") =>
    request<FindingApi>(`/findings/${findingId}/status`, json({ target })),
  comments: (projectId: string) => request<CommentStatusOut[]>(`/projects/${projectId}/comments`),
  reviewComment: (versionId: string, commentId: string, addressed: boolean) =>
    request<{ addressed: boolean }>(`/versions/${versionId}/comments/${commentId}`, json({ addressed })),
  brief: (projectId: string) => request<BriefOut>(`/projects/${projectId}/brief`),
  briefText: async (projectId: string) => {
    const res = await fetch(`${API_URL}/projects/${projectId}/brief.txt`);
    if (!res.ok) throw new ApiError(`Brief gagal dibuat (${res.status}).`, res.status);
    return res.text();
  },
  share: (projectId: string) => request<ShareOut>(`/projects/${projectId}/share`, { method: "POST" }),
  sharedBrief: (token: string) => request<BriefOut>(`/share/${token}`),
  decide: (token: string, findingId: string, confirm: boolean) =>
    request<FindingApi>(`/share/${token}/findings/${findingId}`, json({ confirm })),
};
