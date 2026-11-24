// Klien API bertipe. Tipe mencerminkan apps/api/app/schemas/project.py (ubah keduanya bersamaan).

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
  versions: (projectId: string) => request<VersionOut[]>(`/projects/${projectId}/versions`),
};
