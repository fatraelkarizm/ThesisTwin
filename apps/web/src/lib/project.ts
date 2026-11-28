// Proyek aktif disimpan di browser (belum ada akun mahasiswa). Dipakai halaman Unggah & Ruang Kerja.
export const PROJECT_KEY = "thesistwin.projectId";
// Topbar sudah ter-mount saat proyek dibuat/diganti di halaman Unggah; event ini memberitahunya.
export const PROJECT_EVENT = "thesistwin:project";

export function savedProjectId(): string | null {
  return typeof window === "undefined" ? null : window.localStorage.getItem(PROJECT_KEY);
}

export function saveProjectId(id: string | null) {
  if (id) window.localStorage.setItem(PROJECT_KEY, id);
  else window.localStorage.removeItem(PROJECT_KEY);
  window.dispatchEvent(new Event(PROJECT_EVENT));
}
