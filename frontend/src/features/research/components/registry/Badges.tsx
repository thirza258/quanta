import type {
  LifecycleStatus,
  RiskLevel,
} from "@/features/research/model/registry";
import {
  BadgeCheck,
  CircleCheck,
  CircleDashed,
  CircleX,
  LoaderCircle,
  NotebookPen,
  ShieldAlert,
  ShieldCheck,
  ShieldX,
  TriangleAlert,
  type LucideIcon,
} from "lucide-react";
import "@/features/research/research-registry.css";

type Tone = "neutral" | "active" | "low" | "medium" | "high" | "info";
type Meta = { label: string; tone: Tone; icon: LucideIcon; hint: string };

// The backend's lifecycle (services/experiments.py `_lifecycle`).
const statuses: Record<LifecycleStatus, Meta> = {
  CONFIGURED: {
    label: "Configured",
    tone: "neutral",
    icon: CircleDashed,
    hint: "Hypothesis registered; no completed run yet",
  },
  RUNNING: {
    label: "Running",
    tone: "active",
    icon: LoaderCircle,
    hint: "A run is queued or in progress",
  },
  FAILED: {
    label: "Failed",
    tone: "high",
    icon: CircleX,
    hint: "The latest run stopped before producing results",
  },
  PASSED: {
    label: "Passed",
    tone: "low",
    icon: CircleCheck,
    hint: "Completed with low research risk",
  },
  WARNINGS: {
    label: "Warnings",
    tone: "medium",
    icon: TriangleAlert,
    hint: "Completed; the red team raised warnings",
  },
  DOCUMENTED: {
    label: "Documented",
    tone: "info",
    icon: NotebookPen,
    hint: "A conclusion is recorded",
  },
  REPRODUCIBLE: {
    label: "Reproducible",
    tone: "low",
    icon: BadgeCheck,
    hint: "Documented, and a rerun reproduced the result",
  },
};

const risks: Record<RiskLevel, Meta> = {
  LOW: {
    label: "Low risk",
    tone: "low",
    icon: ShieldCheck,
    hint: "The red team found no serious weakness",
  },
  MEDIUM: {
    label: "Medium risk",
    tone: "medium",
    icon: ShieldAlert,
    hint: "The red team raised warnings worth reading",
  },
  HIGH: {
    label: "High risk",
    tone: "high",
    icon: ShieldX,
    hint: "The red team found evidence the result may not hold",
  },
};

function Badge({
  meta,
  prefix,
  spin,
}: {
  meta: Meta;
  prefix: string;
  spin?: boolean;
}) {
  const Icon = meta.icon;
  return (
    <span className={`registry-badge tone-${meta.tone}`} title={meta.hint}>
      <Icon
        size={13}
        aria-hidden="true"
        className={spin ? "spin" : undefined}
      />
      <span className="sr-only">{prefix}</span>
      {meta.label}
    </span>
  );
}

export function StatusBadge({ status }: { status: LifecycleStatus }) {
  return (
    <Badge
      meta={statuses[status] ?? statuses.CONFIGURED}
      prefix="Status: "
      spin={status === "RUNNING"}
    />
  );
}

export function RiskBadge({ risk }: { risk: RiskLevel }) {
  return <Badge meta={risks[risk] ?? risks.MEDIUM} prefix="Research " />;
}
