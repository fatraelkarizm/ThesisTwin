"use client";

import { useCallback, useEffect, useState } from "react";
import { api, ApiError, type ProjectOut, type VersionOut } from "@/lib/api";
import { savedProjectId } from "@/lib/project";

export type ProjectState =
  | { status: "loading" }
  | { status: "none" } // belum ada proyek atau belum ada versi
  | { status: "error"; message: string }
  | { status: "ready"; project: ProjectOut; versions: VersionOut[] };

/** Data proyek aktif yang dipakai semua halaman alur kerja, plus pilihan versi. */
export function useProject() {
  const [state, setState] = useState<ProjectState>({ status: "loading" });
  const [versionId, setVersionId] = useState<string | null>(null);

  const load = useCallback(() => {
    const pid = savedProjectId();
    const loaded = pid ? Promise.all([api.project(pid), api.versions(pid)]) : Promise.resolve(null);
    loaded.then(
      (res) => {
        if (!res || res[1].length === 0) return setState({ status: "none" });
        const [project, versions] = res;
        setState({ status: "ready", project, versions });
        setVersionId((current) => current ?? versions.at(-1)!.id);
      },
      (e: unknown) =>
        setState(
          e instanceof ApiError && e.status === 404
            ? { status: "none" }
            : { status: "error", message: e instanceof ApiError ? e.message : String(e) },
        ),
    );
  }, []);

  useEffect(load, [load]);

  const version = state.status === "ready" ? state.versions.find((v) => v.id === versionId) : undefined;
  const unit: "page" | "section" = version?.media_type === "application/pdf" ? "page" : "section";
  return { state, version, setVersionId, unit, reload: load };
}
