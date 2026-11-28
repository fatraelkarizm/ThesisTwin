import type { ReactNode } from "react";

interface SectionProps {
  title: string;
  description?: string;
  action?: ReactNode;
  id?: string;
  children: ReactNode;
}

// Section terbuka ala Notalx: judul di halaman, isinya kartu-kartu kecil (bukan satu kartu besar).
export function Section({ title, description, action, id, children }: SectionProps) {
  return (
    <section id={id} aria-labelledby={id ? `${id}-title` : undefined} className="scroll-mt-4">
      <header className="mb-3 flex items-start justify-between gap-3">
        <div>
          <h2 id={id ? `${id}-title` : undefined} className="text-lg font-semibold tracking-tight">
            {title}
          </h2>
          {description ? (
            <p className="mt-0.5 text-sm text-muted">{description}</p>
          ) : null}
        </div>
        {action}
      </header>
      {children}
    </section>
  );
}
