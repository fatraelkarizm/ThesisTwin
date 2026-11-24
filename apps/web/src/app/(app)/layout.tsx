import { Sidebar } from "@/components/features/shell/Sidebar";
import { Topbar } from "@/components/features/shell/Topbar";

// Tata letak mahasiswa (sidebar + topbar). Halaman dosen (/dosen) sengaja di luar grup ini.
export default function AppLayout({ children }: LayoutProps<"/">) {
  return (
    <div className="flex min-h-dvh">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar />
        <div className="flex flex-1 flex-col">{children}</div>
      </div>
    </div>
  );
}
