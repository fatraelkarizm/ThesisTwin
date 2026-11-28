import { copy } from "@/lib/copy";

// Posisi mahasiswa di 5 langkah alur kerja (BR-01 / FR-090), dihitung dari data nyata proyek.

export interface JourneyInput {
  elements: number;
  verified: number;
  findingsTotal: number;
  findingsOpen: number;
  questions: number;
  answered: number;
  versions: number;
  commentsPending: number; // komentar dosen yang belum ditandai sudah/belum ditangani
  linksCreated: number;
}

// later = belum relevan (mis. perbandingan versi sebelum ada revisi), bukan tertinggal.
export type StepState = "done" | "next" | "todo" | "later";

export interface JourneyStep {
  href: string;
  title: string;
  detail: string;
  state: StepState;
}

export interface Journey {
  steps: JourneyStep[];
  done: number;
  next: { href: string; title: string; body: string; cta: string };
}

export function journey(i: JourneyInput): Journey {
  const j = copy.home.journey;
  const reviewed = i.findingsTotal - i.findingsOpen;
  const raw: { detail: string; done: boolean; applicable: boolean }[] = [
    { detail: j.elements(i.elements, i.verified), done: i.elements > 0, applicable: true },
    { detail: j.findings(reviewed, i.findingsTotal), done: i.elements > 0 && i.findingsOpen === 0, applicable: true },
    { detail: j.questions(i.answered, i.questions), done: i.questions > 0 && i.answered === i.questions, applicable: true },
    {
      detail: i.versions < 2 ? j.singleVersion : j.comments(i.commentsPending),
      done: i.versions >= 2 && i.commentsPending === 0,
      applicable: i.versions >= 2,
    },
    { detail: j.links(i.linksCreated), done: i.linksCreated > 0, applicable: true },
  ];
  const nextIndex = raw.findIndex((s) => s.applicable && !s.done);
  const steps = copy.steps.map((s, k) => ({
    href: s.href,
    title: s.short,
    detail: raw[k].detail,
    state: (raw[k].done ? "done" : k === nextIndex ? "next" : raw[k].applicable ? "todo" : "later") as StepState,
  }));
  const actions = [
    j.next.elements,
    j.next.findings(i.findingsOpen),
    j.next.questions(i.questions),
    j.next.comments(i.commentsPending),
    j.next.brief,
  ];
  return {
    steps,
    done: raw.filter((s) => s.done).length,
    next: nextIndex === -1 ? { href: "/upload", ...j.next.revise } : { href: steps[nextIndex].href, ...actions[nextIndex] },
  };
}
