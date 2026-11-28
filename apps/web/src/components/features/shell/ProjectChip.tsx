"use client";

import { useEffect, useState } from "react";
import { api, type ProjectOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { PROJECT_EVENT, savedProjectId } from "@/lib/project";

const programLabel = (p: string) => (copy.upload.programs as Record<string, string>)[p] ?? p;

/** Judul proyek aktif di topbar, agar mahasiswa tahu proyek mana yang sedang dibuka. */
export function ProjectChip() {
  const [project, setProject] = useState<ProjectOut | null>(null);
  useEffect(() => {
    const load = () => {
      const pid = savedProjectId();
      (pid ? api.project(pid) : Promise.resolve(null)).then(setProject, () => setProject(null));
    };
    load();
    window.addEventListener(PROJECT_EVENT, load);
    return () => window.removeEventListener(PROJECT_EVENT, load);
  }, []);
  return (
    <span className="min-w-0 leading-tight">
      <span className="block truncate text-sm font-medium">{project?.title ?? copy.shell.noProject}</span>
      {project ? <span className="block truncate text-xs text-muted">{programLabel(project.program)}</span> : null}
    </span>
  );
}
