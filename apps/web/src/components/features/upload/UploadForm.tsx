"use client";

import { CheckCircle2, CircleAlert, FileText, Info } from "lucide-react";
import Link from "next/link";
import { useEffect, useId, useState, type FormEvent } from "react";
import { Button } from "@/components/ui/Button";
import { Card } from "@/components/ui/Card";
import { api, ApiError, type UploadOut, type VersionOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { PROJECT_KEY } from "@/lib/project";

const DOCX = "application/vnd.openxmlformats-officedocument.wordprocessingml.document";

type State =
  | { kind: "idle" }
  | { kind: "busy" }
  | { kind: "done"; result: UploadOut }
  | { kind: "error"; message: string };

export function UploadForm() {
  const u = copy.upload;
  const ids = { title: useId(), program: useId(), file: useId(), consent: useId() };
  const [projectId, setProjectId] = useState<string | null>(null);
  const [versions, setVersions] = useState<VersionOut[]>([]);
  const [title, setTitle] = useState("");
  const [program, setProgram] = useState<keyof typeof u.programs>("matematika");
  const [file, setFile] = useState<File | null>(null);
  const [consent, setConsent] = useState(false);
  const [state, setState] = useState<State>({ kind: "idle" });

  useEffect(() => {
    const saved = window.localStorage.getItem(PROJECT_KEY);
    if (!saved) return;
    api.versions(saved).then(
      (list) => {
        setProjectId(saved);
        setVersions(list);
      },
      // Proyek lama tidak ada lagi (mis. database direset): mulai dari awal.
      () => window.localStorage.removeItem(PROJECT_KEY),
    );
  }, []);

  async function submit(e: FormEvent) {
    e.preventDefault();
    if (!file) return setState({ kind: "error", message: u.noFile });
    setState({ kind: "busy" });
    try {
      let pid = projectId;
      if (!pid) {
        pid = (await api.createProject(title.trim() || u.projectTitlePlaceholder, program)).id;
        window.localStorage.setItem(PROJECT_KEY, pid);
        setProjectId(pid);
      }
      await api.giveConsent(pid);
      const result = await api.upload(pid, file);
      setVersions(await api.versions(pid));
      setState({ kind: "done", result });
    } catch (err) {
      setState({ kind: "error", message: err instanceof ApiError ? err.message : String(err) });
    }
  }

  function reset() {
    window.localStorage.removeItem(PROJECT_KEY);
    setProjectId(null);
    setVersions([]);
    setState({ kind: "idle" });
  }

  const field = "mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm";

  return (
    <div className="grid gap-5 lg:grid-cols-[minmax(0,1fr)_340px]">
      <Card title={u.formTitle} description={u.formDescription}>
        <form onSubmit={submit} className="space-y-4">
          {projectId ? (
            <p className="flex items-center justify-between gap-3 rounded-lg bg-surface-muted px-3 py-2 text-sm">
              <span>
                {u.activeProject}: <span className="font-mono text-xs">{projectId.slice(0, 8)}</span>
              </span>
              <button type="button" onClick={reset} className="text-sm font-medium text-brand underline">
                {u.newProject}
              </button>
            </p>
          ) : (
            <div className="grid gap-4 sm:grid-cols-2">
              <label htmlFor={ids.title} className="block text-sm font-medium">
                {u.projectTitle}
                <input
                  id={ids.title}
                  name="title"
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder={u.projectTitlePlaceholder}
                  className={field}
                />
              </label>
              <label htmlFor={ids.program} className="block text-sm font-medium">
                {u.program}
                <select
                  id={ids.program}
                  name="program"
                  value={program}
                  onChange={(e) => setProgram(e.target.value as keyof typeof u.programs)}
                  className={field}
                >
                  {Object.entries(u.programs).map(([value, label]) => (
                    <option key={value} value={value}>
                      {label}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          )}

          <label htmlFor={ids.file} className="block text-sm font-medium">
            {u.file}
            <input
              id={ids.file}
              name="file"
              type="file"
              accept={`.pdf,.docx,application/pdf,${DOCX}`}
              onChange={(e) => setFile(e.target.files?.[0] ?? null)}
              className={`${field} file:mr-3 file:rounded-md file:border-0 file:bg-brand-soft file:px-3 file:py-1 file:text-sm file:font-medium file:text-brand`}
            />
          </label>

          <label htmlFor={ids.consent} className="flex items-start gap-3 rounded-lg border border-line p-3 text-sm">
            <input
              id={ids.consent}
              name="consent"
              type="checkbox"
              checked={consent}
              onChange={(e) => setConsent(e.target.checked)}
              className="mt-0.5 size-4 accent-brand"
            />
            <span>{u.consent}</span>
          </label>

          <Button type="submit" disabled={!consent || state.kind === "busy"}>
            {state.kind === "busy" ? u.submitting : u.submit}
          </Button>

          <div aria-live="polite">
            {state.kind === "error" ? (
              <p role="alert" className="flex items-start gap-2 rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
                <CircleAlert aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
                {state.message}
              </p>
            ) : null}
            {state.kind === "done" ? <UploadResult result={state.result} /> : null}
          </div>
        </form>
      </Card>

      <Card title={u.versionsTitle}>
        {versions.length === 0 ? (
          <p className="flex items-start gap-2 text-sm text-muted">
            <Info aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
            {u.subtitle}
          </p>
        ) : (
          <ul className="space-y-2">
            {versions.map((v) => (
              <li key={v.id} className="flex items-center gap-3 rounded-xl border border-line p-3">
                <span className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-brand-soft text-brand">
                  <FileText aria-hidden="true" className="size-4" />
                </span>
                <span className="min-w-0 flex-1">
                  <span className="block text-sm font-medium">
                    {copy.dashboard.proposal} v{v.version_no}
                  </span>
                  <span className="block truncate text-xs text-muted">{v.filename}</span>
                </span>
              </li>
            ))}
          </ul>
        )}
      </Card>
    </div>
  );
}

function UploadResult({ result }: { result: UploadOut }) {
  const u = copy.upload;
  const isDocx = result.version.media_type === DOCX;
  return (
    <div className="space-y-1 rounded-lg bg-tone-success-bg p-3 text-sm text-tone-success-fg">
      <p className="flex items-center gap-2 font-semibold">
        <CheckCircle2 aria-hidden="true" className="size-4" />
        {result.created ? u.created : u.duplicate}: v{result.version.version_no}
      </p>
      <p>
        {result.pages} {isDocx ? u.sectionsDocx : u.pagesPdf}
      </p>
      <p>{u.autoResult(result.auto_elements, result.findings)}</p>
      <p className="font-mono text-xs">SHA-256 {result.version.sha256.slice(0, 12)}…</p>
      <Link href="/proyek" className="inline-block font-medium underline">
        {u.openWorkspace}
      </Link>
    </div>
  );
}
