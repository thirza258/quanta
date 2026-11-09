import type { Skipped } from "@/features/research/model/registry";
import type { Tone } from "@/features/research/model/experiment";
import { shortHash } from "@/features/research/model/experiment";
import { Loading } from "@/shared/components/ui";
import {
  Check,
  CircleCheck,
  CircleDashed,
  CircleMinus,
  CircleX,
  Copy,
  LoaderCircle,
  TriangleAlert,
} from "lucide-react";
import type { ReactNode } from "react";
import { useEffect, useRef, useState } from "react";

const TONE_ICON = {
  pass: CircleCheck,
  warn: TriangleAlert,
  fail: CircleX,
  neutral: CircleMinus,
  active: LoaderCircle,
} as const;

/** The icon that goes with a tone; decorative, the label carries meaning. */
export function ToneIcon({ tone, size = 15 }: { tone: Tone; size?: number }) {
  const Icon = TONE_ICON[tone];
  return (
    <Icon
      size={size}
      aria-hidden="true"
      className={`xd-tone-icon is-${tone}${tone === "active" ? " spin" : ""}`}
    />
  );
}

/** A status pill: icon plus text, never colour alone. */
export function StatusBadge({
  tone,
  label,
  icon,
  size = "normal",
  title,
}: {
  tone: Tone;
  label: ReactNode;
  icon?: ReactNode;
  size?: "normal" | "large";
  title?: string;
}) {
  return (
    <span
      className={`xd-badge is-${tone}${size === "large" ? " is-large" : ""}`}
      title={title}
    >
      {icon ?? <ToneIcon tone={tone} size={size === "large" ? 17 : 13} />}
      <span>{label}</span>
    </span>
  );
}

/** Why a section has no result: always the backend's reason. */
export function SkippedNote({
  value,
  what,
}: {
  value: Skipped;
  what?: string;
}) {
  return (
    <div className="xd-skipped">
      <CircleDashed size={16} aria-hidden="true" />
      <p>
        <strong>
          {value.status === "undefined" ? "Undefined" : "Not run"}
          {what ? ` · ${what}` : ""}.
        </strong>{" "}
        {value.reason}
      </p>
    </div>
  );
}

export function SectionHeading({
  id,
  eyebrow,
  title,
  description,
}: {
  id: string;
  eyebrow: string;
  title: string;
  description?: ReactNode;
}) {
  return (
    <div className="xd-section-head">
      <span className="eyebrow">{eyebrow}</span>
      <h2 id={`${id}-title`} tabIndex={-1}>
        {title}
      </h2>
      {description ? <p>{description}</p> : null}
    </div>
  );
}

/** A labelled figure: value first, context underneath. */
export function Stat({
  label,
  value,
  sub,
  tone,
}: {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  tone?: "negative";
}) {
  return (
    <div className="xd-stat">
      <span className="xd-stat-label">{label}</span>
      <strong className={tone === "negative" ? "xd-stat-negative" : ""}>
        {value}
      </strong>
      {sub ? <span className="xd-stat-sub">{sub}</span> : null}
    </div>
  );
}

/** Legend entries keyed by the mark they describe (line or bar swatch). */
export function ChartLegend({
  items,
}: {
  items: {
    label: ReactNode;
    tone: "strategy" | "context" | "loss" | "marker" | "break-even";
    mark?: "line" | "bar" | "dashed" | "dot" | "tick";
  }[];
}) {
  return (
    <ul className="xd-legend">
      {items.map((item, index) => (
        <li key={index}>
          <i
            className={`xd-key xd-key-${item.mark ?? "line"} is-${item.tone}`}
            aria-hidden="true"
          />
          {item.label}
        </li>
      ))}
    </ul>
  );
}

/** Space held for a lazy chart so anchors below do not jump. */
export function ChartFallback({ height }: { height: number }) {
  return (
    <div className="xd-chart-fallback" style={{ height }}>
      <Loading label="Drawing chart…" />
    </div>
  );
}

/** A truncated hash; the full value is in the title and copied on click. */
export function HashValue({
  value,
  label,
}: {
  value: string | null | undefined;
  label: string;
}) {
  const [copied, setCopied] = useState(false);
  const timer = useRef(0);
  useEffect(() => () => window.clearTimeout(timer.current), []);
  if (!value) return <span className="muted">—</span>;
  return (
    <span className="xd-hash">
      <code title={value} tabIndex={0} aria-label={`${label}: ${value}`}>
        {shortHash(value)}
      </code>
      <button
        type="button"
        className="icon-button"
        aria-label={copied ? `Copied ${label}` : `Copy full ${label}`}
        title={copied ? "Copied" : "Copy full value"}
        onClick={async () => {
          try {
            await navigator.clipboard.writeText(value);
            setCopied(true);
            window.clearTimeout(timer.current);
            timer.current = window.setTimeout(() => setCopied(false), 1600);
          } catch {
            setCopied(false);
          }
        }}
      >
        {copied ? <Check size={14} /> : <Copy size={14} />}
      </button>
    </span>
  );
}

/** A 0–1 meter on a lighter step of the same hue. */
export function Meter({ value, label }: { value: number; label: string }) {
  const clamped = Math.min(1, Math.max(0, value));
  return (
    <span
      className="xd-meter"
      role="img"
      aria-label={`${label}: ${Math.round(clamped * 100)} of 100`}
    >
      <span style={{ width: `${clamped * 100}%` }} />
    </span>
  );
}

export function Notice({
  tone,
  title,
  children,
  action,
  onDismiss,
}: {
  tone: "warn" | "fail" | "info";
  title?: ReactNode;
  children?: ReactNode;
  action?: ReactNode;
  onDismiss?: () => void;
}) {
  return (
    <div
      className={`xd-notice is-${tone}`}
      role={tone === "fail" ? "alert" : "status"}
    >
      <ToneIcon tone={tone === "info" ? "neutral" : tone} size={17} />
      <div className="xd-notice-body">
        {title ? <strong>{title}</strong> : null}
        {children ? <div>{children}</div> : null}
      </div>
      {action || onDismiss ? (
        <div className="xd-notice-actions">
          {action}
          {onDismiss ? (
            <button
              type="button"
              className="button secondary small"
              onClick={onDismiss}
            >
              Dismiss
            </button>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}
