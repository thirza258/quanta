import * as Dialog from "@radix-ui/react-dialog";
import {
  X,
  ArrowUpRight,
  BookOpen,
  ChartNoAxesCombined,
  FlaskConical,
  Bot,
  BrainCircuit,
  Network,
  Sigma,
} from "lucide-react";
import type { ReactNode } from "react";
export function Modal({
  open,
  onOpenChange,
  title,
  description,
  children,
  wide = false,
  container,
}: {
  open: boolean;
  onOpenChange: (v: boolean) => void;
  title: string;
  description?: string;
  children: ReactNode;
  wide?: boolean;
  container?: HTMLElement | null;
}) {
  return (
    <Dialog.Root open={open} onOpenChange={onOpenChange}>
      <Dialog.Portal container={container}>
        <Dialog.Overlay className="modal-overlay" />
        <Dialog.Content className={`modal ${wide ? "modal-wide" : ""}`}>
          <div className="modal-heading">
            <Dialog.Title>{title}</Dialog.Title>
            <Dialog.Close className="icon-button" aria-label="Close dialog">
              <X size={19} />
            </Dialog.Close>
          </div>
          <Dialog.Description
            className={description ? "modal-description" : "sr-only"}
          >
            {description || title}
          </Dialog.Description>
          {children}
        </Dialog.Content>
      </Dialog.Portal>
    </Dialog.Root>
  );
}
export function TrackIcon({
  kind,
  size = 20,
}: {
  kind: string;
  size?: number;
}) {
  const Icon =
    kind === "book"
      ? BookOpen
      : kind === "distribution"
        ? Sigma
        : kind === "factors"
          ? ChartNoAxesCombined
          : kind === "lab"
            ? FlaskConical
            : kind === "bot"
              ? Bot
              : kind === "machine-learning"
                ? BrainCircuit
                : Network;
  return <Icon size={size} strokeWidth={1.6} />;
}
export function EmptyState({
  icon,
  title,
  description,
  children,
}: {
  icon: ReactNode;
  title: string;
  description: string;
  children?: ReactNode;
}) {
  return (
    <div className="empty-state">
      <span className="empty-icon">{icon}</span>
      <h3>{title}</h3>
      <p>{description}</p>
      {children}
    </div>
  );
}
export function Loading({ label = "Loading workspace…" }: { label?: string }) {
  return (
    <div className="loading-state">
      <span className="spinner" />
      {label}
    </div>
  );
}
export function ExternalLink({
  href,
  children,
}: {
  href: string;
  children: ReactNode;
}) {
  return (
    <a href={href} target="_blank" rel="noreferrer" className="text-link">
      {children}
      <ArrowUpRight size={15} />
    </a>
  );
}
export function TrackArt({
  kind,
  large = false,
}: {
  kind: string;
  large?: boolean;
}) {
  const lines = Array.from({ length: 7 }, (_, i) => i);
  return (
    <svg
      className={`track-art ${large ? "large" : ""}`}
      viewBox="0 0 200 120"
      fill="none"
      aria-hidden="true"
    >
      <defs>
        <pattern
          id={`grid-${kind}-${large}`}
          width="20"
          height="20"
          patternUnits="userSpaceOnUse"
        >
          <path
            d="M20 0H0V20"
            stroke="currentColor"
            strokeWidth=".5"
            opacity=".12"
          />
        </pattern>
      </defs>
      <rect width="200" height="120" fill={`url(#grid-${kind}-${large})`} />
      {kind === "book" ? (
        <g stroke="currentColor">
          <path
            d="M100 32Q76 16 40 24V91Q74 83 100 101Q126 83 160 91V24Q124 16 100 32Z"
            fill="var(--art-fill)"
          />
          <path d="M100 32V101M34 31V98Q73 89 100 107Q127 89 166 98V31" />
          <path
            d="M51 40Q71 36 88 45M51 51Q71 47 88 56M51 62Q71 58 88 67M51 73Q69 69 80 75M112 45Q129 36 149 40M112 56Q129 47 149 51M112 67Q129 58 149 62M120 75Q133 70 149 73"
            opacity=".5"
          />
        </g>
      ) : null}
      {kind === "distribution" ? (
        <g stroke="currentColor">
          <path d="M20 96H183M35 96V20" opacity=".3" />
          {lines.map((i) => (
            <path
              key={i}
              d={`M25 95 C${65 - i * 3} 95 ${77 - i * 2} ${7 + i * 9} 105 ${7 + i * 9} S${143 + i * 2} 95 183 95`}
              opacity={0.2 + i * 0.1}
            />
          ))}
        </g>
      ) : null}
      {kind === "factors" ? (
        <g stroke="currentColor">
          {lines.slice(0, 5).map((i) => (
            <path
              key={i}
              d={`M32 ${100 - i * 14} 77 ${78 - i * 13} 113 ${90 - i * 17} 168 ${49 - i * 7}`}
              opacity={0.2 + i * 0.16}
            />
          ))}
          <path d="M32 16v86h142" opacity=".25" />
          <circle cx="113" cy="39" r="4" fill="var(--art-fill)" />
          <circle cx="77" cy="39" r="3" fill="var(--art-fill)" />
        </g>
      ) : null}
      {kind === "lab" ? (
        <g stroke="currentColor">
          <path d="M85 17h30M91 17v37l-33 48q-5 10 8 10h68q13 0 8-10l-33-48V17" />
          <path
            d="m76 79 12-5 18 9 17-6 15 24q4 7-6 7H69q-9 0-5-7z"
            fill="var(--art-fill)"
          />
          <circle cx="96" cy="91" r="3" />
          <circle cx="111" cy="99" r="2" />
          <path d="M142 35h28M156 21v28M35 59h18M44 50v18" opacity=".35" />
        </g>
      ) : null}
      {kind === "bot" ? (
        <g stroke="currentColor">
          <rect
            x="65"
            y="38"
            width="70"
            height="49"
            rx="8"
            fill="var(--art-fill)"
          />
          <path d="M100 38V23M87 97h26M52 51v23M148 51v23" />
          <circle cx="100" cy="19" r="4" />
          <circle cx="84" cy="58" r="4" />
          <circle cx="116" cy="58" r="4" />
          <path d="M88 74h24M32 39H18v46h26M165 34h17v57h-17" opacity=".35" />
        </g>
      ) : null}
      {kind === "crypto" ? (
        <g stroke="currentColor">
          <path d="m100 15 48 29v48l-48 28-48-28V44zM100 15v49m48-20-48 20-48-20m48 20v56M52 92l48-28 48 28" />
          <path d="m100 32 31 19v31l-31 18-31-18V51z" fill="var(--art-fill)" />
          <path
            d="m100 41 13 22-13 8-13-8zM87 68l13 18 13-18-13 8z"
            opacity=".65"
          />
        </g>
      ) : null}
      {kind === "machine-learning" ? (
        <g stroke="currentColor">
          <path
            d="M42 32L100 24M42 32L100 60M42 32L100 96M42 60L100 24M42 60L100 60M42 60L100 96M42 88L100 24M42 88L100 60M42 88L100 96M100 24L158 42M100 24L158 78M100 60L158 42M100 60L158 78M100 96L158 42M100 96L158 78"
            opacity=".3"
          />
          {[32, 60, 88].map((y) => (
            <circle
              key={`input-${y}`}
              cx="42"
              cy={y}
              r="7"
              fill="var(--art-fill)"
            />
          ))}
          {[24, 60, 96].map((y) => (
            <circle
              key={`hidden-${y}`}
              cx="100"
              cy={y}
              r="9"
              fill="var(--art-fill)"
            />
          ))}
          {[42, 78].map((y) => (
            <circle
              key={`output-${y}`}
              cx="158"
              cy={y}
              r="7"
              fill="var(--art-fill)"
            />
          ))}
        </g>
      ) : null}
    </svg>
  );
}
