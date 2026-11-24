import type { ReactNode } from "react";

interface CardProps {
  title?: string;
  description?: string;
  action?: ReactNode;
  as?: "section" | "div" | "article";
  className?: string;
  children: ReactNode;
}

export function Card({ title, description, action, as: Tag = "section", className = "", children }: CardProps) {
  return (
    <Tag className={`rounded-card border border-line bg-surface p-5 shadow-card ${className}`}>
      {title ? (
        <header className="mb-4 flex items-start justify-between gap-3">
          <div>
            <h2 className="text-base font-semibold">{title}</h2>
            {description ? <p className="mt-0.5 text-sm text-muted">{description}</p> : null}
          </div>
          {action}
        </header>
      ) : null}
      {children}
    </Tag>
  );
}
