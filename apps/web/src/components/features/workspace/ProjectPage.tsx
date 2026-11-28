"use client";

import { ArrowRight, CircleAlert } from "lucide-react";
import Link from "next/link";
import type { ReactNode } from "react";
import { buttonClass } from "@/components/ui/Button";
import type { ProjectOut, VersionOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { useProject } from "./useProject";

export interface ProjectContext {
  project: ProjectOut;
  versions: VersionOut[];
  version: VersionOut;
  unit: "page" | "section";
  reload: () => void;
}

interface ProjectPageProps {
  step: number; // 1-based, urutan di copy.steps
  versionPicker?: boolean;
  children: (ctx: ProjectContext) => ReactNode;
}

/** Kerangka seragam tiap halaman alur kerja: langkah, judul, penjelasan, pilihan versi, isi,
 *  dan tautan ke langkah berikutnya. Satu konsep per halaman. */
export function ProjectPage({ step, versionPicker = true, children }: ProjectPageProps) {
  const { state, version, setVersionId, unit, reload } = useProject();
  const steps = copy.steps;
  const current = steps[step - 1];
  const next = steps[step];

  return (
    <main className="flex flex-1 flex-col bg-surface">
      <header className="border-b border-line px-4 pt-6 pb-5 md:px-8">
        <div className="mx-auto max-w-5xl">
        <p className="text-xs font-semibold uppercase tracking-wide text-brand-strong">
          {copy.stepLabel(step, steps.length)}
        </p>
        <h1 className="mt-1 text-2xl font-semibold tracking-tight">{current.title}</h1>
        <p className="mt-1 max-w-3xl text-sm text-muted">{current.description}</p>

        {/* Desktop: sidebar sudah menampilkan langkah yang sama. */}
        <ol className="mt-4 flex flex-wrap gap-1.5 md:hidden" aria-label={copy.shell.workflow}>
          {steps.map((s, i) => (
            <li key={s.href}>
              <Link
                href={s.href}
                aria-current={i + 1 === step ? "step" : undefined}
                className={`inline-flex min-h-9 items-center gap-1.5 rounded-full border px-3 text-xs ${
                  i + 1 === step
                    ? "border-brand bg-brand-soft font-semibold text-brand-strong"
                    : "border-line text-muted hover:text-foreground"
                }`}
              >
                <span className="tabular-nums">{i + 1}</span>
                {s.short}
              </Link>
            </li>
          ))}
        </ol>
        </div>
      </header>

      <div className="flex-1 px-4 py-6 md:px-8">
        {state.status === "loading" ? <p className="text-sm text-muted">{copy.workspace.loading}</p> : null}
        {state.status === "error" ? (
          <p role="alert" className="flex items-start gap-2 rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
            <CircleAlert aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
            {state.message}
          </p>
        ) : null}
        {state.status === "none" ? (
          <div className="mx-auto max-w-md rounded-card border border-dashed border-line p-8 text-center">
            <p className="text-sm text-muted">{copy.workspace.empty}</p>
            <Link href="/upload" className={buttonClass("primary", "mt-4")}>
              {copy.workspace.goUpload}
            </Link>
          </div>
        ) : null}

        {state.status === "ready" && version ? (
          <div className="mx-auto max-w-5xl space-y-6">
            {versionPicker && state.versions.length > 0 ? (
              <div className="flex flex-wrap items-center gap-2" role="group" aria-label={copy.workspace.version}>
                <span className="text-xs font-medium text-muted">{copy.workspace.version}</span>
                {state.versions.map((v) => (
                  <button
                    key={v.id}
                    type="button"
                    aria-pressed={v.id === version.id}
                    onClick={() => setVersionId(v.id)}
                    title={v.filename}
                    className={`min-h-9 max-w-xs truncate rounded-full border px-3 text-sm ${
                      v.id === version.id ? "border-brand bg-brand-soft font-medium text-brand-strong" : "border-line"
                    }`}
                  >
                    v{v.version_no}
                  </button>
                ))}
                <span className="truncate text-xs text-muted">{version.filename}</span>
              </div>
            ) : null}

            {children({ project: state.project, versions: state.versions, version, unit, reload })}

            {next ? (
              <div className="flex justify-end border-t border-line pt-5">
                <Link href={next.href} className={buttonClass("secondary")}>
                  {copy.nextStep}: {next.short}
                  <ArrowRight aria-hidden="true" className="size-4" />
                </Link>
              </div>
            ) : null}
          </div>
        ) : null}
      </div>
    </main>
  );
}
