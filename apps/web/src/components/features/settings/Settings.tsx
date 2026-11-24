"use client";

import { CircleAlert, Trash2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useId, useState } from "react";
import { Badge } from "@/components/ui/Badge";
import { Button } from "@/components/ui/Button";
import { Section } from "@/components/ui/Section";
import { api, ApiError, type ProjectOut, type ShareLinkOut } from "@/lib/api";
import { copy } from "@/lib/copy";
import { PROJECT_KEY, savedProjectId } from "@/lib/project";

const fmt = (iso: string) => new Date(iso).toLocaleDateString("id-ID", { day: "numeric", month: "short", year: "numeric" });

export function Settings() {
  const t = copy.settings;
  const router = useRouter();
  const confirmId = useId();
  const [project, setProject] = useState<ProjectOut | null>(null);
  const [links, setLinks] = useState<ShareLinkOut[]>([]);
  const [loaded, setLoaded] = useState(false);
  const [confirm, setConfirm] = useState("");
  const [error, setError] = useState<string | null>(null);
  // Waktu sekarang diambil setelah data tiba (bukan saat render: nilai tak stabil saat prerender).
  const [now, setNow] = useState(0);

  useEffect(() => {
    const pid = savedProjectId();
    (pid ? Promise.all([api.project(pid), api.shareLinks(pid)]) : Promise.resolve(null))
      .then((res) => {
        if (res) {
          setProject(res[0]);
          setLinks(res[1]);
        }
        setNow(Date.now());
      })
      .catch((e: unknown) => setError(e instanceof ApiError ? e.message : String(e)))
      .finally(() => setLoaded(true));
  }, []);

  async function revoke(linkId: string) {
    if (!project) return;
    const updated = await api.revokeLink(project.id, linkId);
    setLinks((prev) => prev.map((l) => (l.id === linkId ? updated : l)));
  }

  async function remove() {
    if (!project) return;
    try {
      await api.deleteProject(project.id);
      window.localStorage.removeItem(PROJECT_KEY);
      router.push("/");
    } catch (e) {
      setError(e instanceof ApiError ? e.message : String(e));
    }
  }

  if (!loaded) return <p className="p-6 text-sm text-muted">{copy.workspace.loading}</p>;

  return (
    <div className="mx-auto w-full max-w-3xl space-y-8 p-4 md:p-6">
      {error ? (
        <p role="alert" className="flex items-start gap-2 rounded-lg bg-tone-danger-bg p-3 text-sm text-tone-danger-fg">
          <CircleAlert aria-hidden="true" className="mt-0.5 size-4 shrink-0" />
          {error}
        </p>
      ) : null}
      {!project ? (
        <p className="text-sm text-muted">{t.none}</p>
      ) : (
        <>
          <Section title={t.linksTitle} description={t.linksDescription}>
            {links.length === 0 ? (
              <p className="text-sm text-muted">{t.noLinks}</p>
            ) : (
              <ul className="space-y-2">
                {links.map((l) => {
                  const expired = new Date(l.expires_at).getTime() <= now;
                  return (
                    <li key={l.id} className="flex flex-wrap items-center gap-3 rounded-card border border-line bg-surface p-3 shadow-card">
                      <span className="text-sm">
                        {t.created} {fmt(l.created_at)} · {t.expires} {fmt(l.expires_at)}
                      </span>
                      <Badge tone={l.revoked || expired ? "neutral" : "success"}>
                        {l.revoked ? t.revoked : expired ? t.expired : t.active}
                      </Badge>
                      {!l.revoked && !expired ? (
                        <Button variant="secondary" className="ml-auto" onClick={() => revoke(l.id)}>
                          {t.revoke}
                        </Button>
                      ) : null}
                    </li>
                  );
                })}
              </ul>
            )}
          </Section>

          <section className="rounded-card border border-tone-danger-fg/30 bg-tone-danger-bg/40 p-5">
            <h2 className="text-lg font-semibold text-tone-danger-fg">{t.dangerTitle}</h2>
            <p className="mt-1 text-sm">{t.dangerDescription}</p>
            <label htmlFor={confirmId} className="mt-4 block text-sm font-medium">
              {t.confirmLabel(project.title)}
              <input
                id={confirmId}
                name="confirm"
                value={confirm}
                onChange={(e) => setConfirm(e.target.value)}
                autoComplete="off"
                className="mt-1 w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm"
              />
            </label>
            <button
              type="button"
              onClick={remove}
              disabled={confirm !== project.title}
              className="mt-3 inline-flex min-h-11 items-center gap-2 rounded-lg bg-tone-danger-fg px-4 text-sm font-medium text-tone-danger-bg disabled:cursor-not-allowed disabled:opacity-50"
            >
              <Trash2 aria-hidden="true" className="size-4" />
              {t.delete}
            </button>
          </section>
        </>
      )}
    </div>
  );
}
