// Proyek aktif disimpan di browser (belum ada akun mahasiswa). Dipakai halaman Unggah & Ruang Kerja.
export const PROJECT_KEY = "thesistwin.projectId";

export function savedProjectId(): string | null {
  return typeof window === "undefined" ? null : window.localStorage.getItem(PROJECT_KEY);
}
