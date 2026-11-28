import { tracks } from "@/features/learning/model/catalog";
import { trackProgress } from "@/features/learning/model/progress";
import type { Track } from "@/features/learning/model/types";
import type { WorkspaceState } from "@/features/workspace/model/types";

export type CourseDomain =
  | "fundamentals"
  | "value"
  | "quant"
  | "systems"
  | "specialized"
  | "crypto"
  | "professional";

export type CourseStage = 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12;

export type CourseConnection = {
  id: string;
  stage: CourseStage;
  stageName: string;
  domain: CourseDomain;
  domainLabel: string;
  prerequisites: string[];
  /** The learner must complete at least one of these, not all of them. */
  prerequisitesAnyOf: string[];
  recommendedBefore: string[];
  unlocks: string[];
  whyPrerequisites: string;
  whyUnlocks: string;
  focusSummary: string;
  skillsGained: string[];
  courseType: string;
  difficulty: number;
  sequence: number;
  isCore: boolean;
  isSpecialization: boolean;
  isCapstone: boolean;
};

export type LearningPathway = {
  id: string;
  title: string;
  subtitle: string;
  targetRole: string;
  badge: string;
  description: string;
  steps: {
    step: number;
    trackId: string;
    whyThisStep: string;
    keyDeliverable: string;
  }[];
};

export const STAGE_CONFIG: Record<
  CourseStage,
  { name: string; subtitle: string; badge: string }
> = {
  1: {
    name: "Orientation & Market Mechanics",
    subtitle:
      "Vocabulary, ownership, orders, returns, costs, and the first research plan.",
    badge: "Orientation",
  },
  2: {
    name: "Financial & Investment Foundations",
    subtitle:
      "Conduct, careful-investor principles, and supervised simulator practice.",
    badge: "Foundations",
  },
  3: {
    name: "Fundamental Analysis & Market Information",
    subtitle:
      "Financial statements, security analysis, and verified news-to-valuation reasoning.",
    badge: "Fundamental Core",
  },
  4: {
    name: "Advanced Fundamental Analysis",
    subtitle:
      "Forensics, credit, quality, banks, cyclicals, intangibles, and documented cases.",
    badge: "Value Specializations",
  },
  5: {
    name: "Quantitative Foundations & Applied Valuation",
    subtitle:
      "Data hygiene, Python, probability, statistics, regression, risk, and valuation under uncertainty.",
    badge: "Quant Foundations",
  },
  6: {
    name: "Empirical Finance & Econometrics",
    subtitle:
      "Identification, time series, volatility, factor tests, causal designs, and state-space models.",
    badge: "Econometrics",
  },
  7: {
    name: "Research Methodology & Strategy Development",
    subtitle:
      "Point-in-time data, backtest hygiene, strategy construction, portfolio constraints, and validation.",
    badge: "Strategy Research",
  },
  8: {
    name: "Machine Learning for Markets",
    subtitle:
      "Features, labels, purged validation, regularized and tree models, deployment, and monitoring.",
    badge: "Machine Learning",
  },
  9: {
    name: "Algorithmic & AI Trading",
    subtitle:
      "Event-driven bots, execution, risk gates, AI evidence, operations, and capacity.",
    badge: "Algorithmic Trading",
  },
  10: {
    name: "High-Performance Computing",
    subtitle:
      "C17 systems, cache layout, profiling, threads, SIMD, GPUs, and distributed research.",
    badge: "HPC",
  },
  11: {
    name: "Specializations & Professional Practice",
    subtitle:
      "Web3/DeFi, conduct and compliance, and an alternative MSME financial-literacy on-ramp.",
    badge: "Specializations",
  },
  12: {
    name: "Capstone: Research Evaluation",
    subtitle:
      "Audit an algorithm's returns, risk, execution, uncertainty, and reproducibility in a final report.",
    badge: "Capstone",
  },
};

export const STAGE_ORDER: CourseStage[] = [
  1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12,
];

export const DOMAIN_CONFIG: Record<
  CourseDomain,
  { label: string; color: string }
> = {
  fundamentals: { label: "Foundations & Ethics", color: "var(--accent)" },
  value: { label: "Fundamental & Value", color: "#2563eb" },
  quant: { label: "Quantitative & Econometrics", color: "#7c3aed" },
  systems: { label: "Systems & Algorithmic Bots", color: "#ea580c" },
  specialized: { label: "Advanced Security Analysis", color: "#0891b2" },
  crypto: { label: "Web3 & Cryptography", color: "#d97706" },
  professional: { label: "Conduct & Professional Practice", color: "#64748b" },
};

const trackById = new Map(tracks.map((track) => [track.id, track]));

function courseStage(track: Track): CourseStage {
  const stage = track.stage_number;
  return (stage && stage >= 1 && stage <= 12 ? stage : 12) as CourseStage;
}

function courseDomain(track: Track): CourseDomain {
  const domain = track.domain;
  return domain && domain in DOMAIN_CONFIG
    ? (domain as CourseDomain)
    : "fundamentals";
}

function focusSummary(track: Track): string {
  if (track.focus_summary) return track.focus_summary;
  const firstSentence = track.description
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/[*_`]/g, "")
    .split(/(?<=\.)\s/)[0];
  return firstSentence.replace(/\.$/, "") + ".";
}

function titleOf(id: string): string {
  return trackById.get(id)?.title ?? id;
}

function joinedTitles(ids: string[]): string {
  const titles = ids.map(titleOf);
  if (titles.length <= 1) return titles[0] ?? "";
  if (titles.length === 2) return `${titles[0]} and ${titles[1]}`;
  return `${titles.slice(0, -1).join(", ")}, and ${titles.at(-1)}`;
}

// An "unlocks" edge exists when a course is a hard prerequisite or one of the
// accepted alternatives for a later course.
const unlocksById = new Map<string, string[]>(
  tracks.map((track) => [track.id, []]),
);
for (const track of tracks) {
  for (const prerequisite of [
    ...(track.prerequisite_course_ids ?? []),
    ...(track.prerequisite_any_of ?? []),
  ]) {
    unlocksById.get(prerequisite)?.push(track.id);
  }
}

export const courseConnections: CourseConnection[] = tracks.map((track) => {
  const stage = courseStage(track);
  const domain = courseDomain(track);
  const prerequisites = track.prerequisite_course_ids ?? [];
  const prerequisitesAnyOf = track.prerequisite_any_of ?? [];
  const recommendedBefore = track.recommended_course_ids ?? [];
  const unlocks = unlocksById.get(track.id) ?? [];
  const requiredParts: string[] = [];
  if (prerequisites.length) {
    requiredParts.push(`requires ${joinedTitles(prerequisites)}`);
  }
  if (prerequisitesAnyOf.length) {
    requiredParts.push(
      `requires at least one of ${joinedTitles(prerequisitesAnyOf)}`,
    );
  }
  if (!requiredParts.length) {
    requiredParts.push("has no hard prerequisites");
  }
  const notes = track.prerequisites?.trim();
  return {
    id: track.id,
    stage,
    stageName: STAGE_CONFIG[stage].name,
    domain,
    domainLabel: DOMAIN_CONFIG[domain].label,
    prerequisites,
    prerequisitesAnyOf,
    recommendedBefore,
    unlocks,
    whyPrerequisites: requiredParts.join("; ") + (notes ? `. ${notes}` : "."),
    whyUnlocks: unlocks.length
      ? `Builds the foundation for ${joinedTitles(unlocks)}.`
      : "Terminal course in this branch; it consolidates earlier skills rather than unlocking a new course.",
    focusSummary: focusSummary(track),
    skillsGained:
      track.skills ?? track.learning_outcomes ?? track.outcomes ?? [],
    courseType: track.course_type ?? "core",
    difficulty: track.difficulty ?? 0,
    sequence: track.sequence ?? 0,
    isCore: track.is_core ?? false,
    isSpecialization: track.is_specialization ?? false,
    isCapstone: track.is_capstone ?? false,
  };
});

const connectionMap = new Map<string, CourseConnection>(
  courseConnections.map((connection) => [connection.id, connection]),
);

export function getConnection(trackId: string): CourseConnection | undefined {
  return connectionMap.get(trackId);
}

function completed(trackId: string, state: WorkspaceState): boolean {
  const track = trackById.get(trackId);
  return track ? trackProgress(track, state).complete : false;
}

export function arePrerequisitesMet(
  trackId: string,
  state: WorkspaceState,
): boolean {
  const connection = connectionMap.get(trackId);
  if (!connection) return true;
  const hardMet = connection.prerequisites.every((id) => completed(id, state));
  const anyMet =
    connection.prerequisitesAnyOf.length === 0 ||
    connection.prerequisitesAnyOf.some((id) => completed(id, state));
  return hardMet && anyMet;
}

export function getMissingPrerequisites(
  trackId: string,
  state: WorkspaceState,
): Track[] {
  const connection = connectionMap.get(trackId);
  if (!connection) return [];
  const missingIds = connection.prerequisites.filter(
    (id) => !completed(id, state),
  );
  if (
    connection.prerequisitesAnyOf.length > 0 &&
    !connection.prerequisitesAnyOf.some((id) => completed(id, state))
  ) {
    missingIds.push(...connection.prerequisitesAnyOf);
  }
  return [...new Set(missingIds)]
    .map((id) => trackById.get(id))
    .filter((track): track is Track => track !== undefined);
}

export type CourseReadiness = "completed" | "in_progress" | "ready" | "locked";

export function getCourseReadiness(
  track: Track,
  state: WorkspaceState,
): CourseReadiness {
  const progress = trackProgress(track, state);
  if (progress.complete) return "completed";
  if (progress.percent > 0) return "in_progress";
  return arePrerequisitesMet(track.id, state) ? "ready" : "locked";
}

export function getRecommendedNextTracks(state: WorkspaceState): Track[] {
  const inProgress = tracks.filter((track) => {
    const progress = trackProgress(track, state);
    return progress.percent > 0 && !progress.complete;
  });
  if (inProgress.length > 0) return inProgress.slice(0, 3);

  const ready = tracks.filter((track) => {
    const progress = trackProgress(track, state);
    return progress.percent === 0 && arePrerequisitesMet(track.id, state);
  });
  if (ready.length > 0) {
    return ready
      .sort((a, b) => (a.sequence ?? 0) - (b.sequence ?? 0))
      .slice(0, 3);
  }
  return tracks.filter((track) => track.id === "trading-fundamentals");
}

export const learningPathways: LearningPathway[] = [
  {
    id: "complete-quant",
    title: "Complete Quantitative Finance Path",
    subtitle:
      "The full progression from market literacy to econometrics, strategy research, ML, bots, HPC, and the capstone.",
    targetRole:
      "Quantitative Analyst · Portfolio Researcher · Systematic Trader",
    badge: "Core Quantitative Path",
    description:
      "The default path for a learner who wants the whole discipline: foundations, fundamental analysis, quantitative methods, empirical finance, research methodology, machine learning, algorithmic systems, high-performance computing, and a final evaluation capstone.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Establish ownership, order mechanics, returns, costs, risk, and the vocabulary every later course assumes.",
        keyDeliverable: "A written research and paper-trading plan.",
      },
      {
        step: 2,
        trackId: "trading-ethics",
        whyThisStep:
          "Settle whose interest a trade serves before learning to value or automate one.",
        keyDeliverable: "A personal trading charter with do-and-do-not rules.",
      },
      {
        step: 3,
        trackId: "intelligent-investor",
        whyThisStep:
          "Build the temperament, allocation policy, and margin-of-safety discipline that precede security selection.",
        keyDeliverable: "A written careful-investor policy.",
      },
      {
        step: 4,
        trackId: "security-analysis",
        whyThisStep:
          "Learn to read statements, senior claims, earnings quality, and asset value before any quantitative model.",
        keyDeliverable:
          "A normalized earnings and valuation range for a company.",
      },
      {
        step: 5,
        trackId: "statistical-foundations",
        whyThisStep:
          "Acquire time value, probability, inference, regression, factor risk, VaR, and backtest hygiene in one coherent toolkit.",
        keyDeliverable: "A reproducible quantitative research report.",
      },
      {
        step: 6,
        trackId: "econometrics",
        whyThisStep:
          "Move from statistical description to identification, time series, volatility, factor tests, and causal designs.",
        keyDeliverable:
          "A factor regression with robust inference and diagnostics.",
      },
      {
        step: 7,
        trackId: "lab-workshop",
        whyThisStep:
          "Practise the research platform only after the statistics and regression it exposes.",
        keyDeliverable:
          "A complete saved research loop from hypothesis to evidence.",
      },
      {
        step: 8,
        trackId: "strategy-lab",
        whyThisStep:
          "Turn hypotheses into falsifiable, cost-aware strategies with portfolio constraints and honest validation.",
        keyDeliverable: "A defended reproducible strategy dossier.",
      },
      {
        step: 9,
        trackId: "stock-machine-learning",
        whyThisStep:
          "Add point-in-time features, purged validation, regularized and tree models, and production monitoring.",
        keyDeliverable: "A validated stock-ML pipeline and model card.",
      },
      {
        step: 10,
        trackId: "stock-bots",
        whyThisStep:
          "Integrate signals, execution, risk gates, AI evidence, and operations into an event-driven bot.",
        keyDeliverable:
          "A durable paper bot with an acceptance and incident dossier.",
      },
      {
        step: 11,
        trackId: "c-hpc-trading",
        whyThisStep:
          "Optimize only after the algorithms are understood: C17, profiling, threads, SIMD, and GPUs.",
        keyDeliverable: "A reproducible C trading research engine.",
      },
      {
        step: 12,
        trackId: "algorithm-evaluation",
        whyThisStep:
          "Close the program by auditing returns, risk, execution, robustness, and uncertainty in a final report.",
        keyDeliverable: "A complete algorithm evaluation and results dossier.",
      },
    ],
  },
  {
    id: "fundamental-investor",
    title: "Fundamental Equity & Value Investor",
    subtitle:
      "Statements, forensics, credit, quality, banks, and valuation under uncertainty, ending in a documented casebook.",
    targetRole: "Equity Analyst · Value Fund Analyst · Buy-Side Researcher",
    badge: "Value & Fundamental",
    description:
      "For learners who want the fundamental-analysis branch: careful investing, Security Analysis, verified news research, forensic accounting, credit, quality, bank analysis, valuation under uncertainty, and a documented real-world casebook.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Understand shares, quotes, costs, and risk before reading a company in detail.",
        keyDeliverable: "Market-mechanics and return-arithmetic fluency.",
      },
      {
        step: 2,
        trackId: "intelligent-investor",
        whyThisStep:
          "Establish temperament, diversification, and margin-of-safety discipline.",
        keyDeliverable: "A careful-investor policy statement.",
      },
      {
        step: 3,
        trackId: "security-analysis",
        whyThisStep:
          "Learn the full Graham-Dodd method from statements to senior claims and asset value.",
        keyDeliverable: "A normalized earnings and valuation-range memo.",
      },
      {
        step: 4,
        trackId: "news-to-markets",
        whyThisStep:
          "Convert news and macro releases into verified cash-flow and valuation implications.",
        keyDeliverable: "An evidence-led news research memo.",
      },
      {
        step: 5,
        trackId: "forensic-accounting",
        whyThisStep:
          "Detect aggressive accounting before trusting reported earnings.",
        keyDeliverable: "A forensic scorecard and red-team memo.",
      },
      {
        step: 6,
        trackId: "credit-distress",
        whyThisStep:
          "Test debt safety, covenants, and recovery before valuing the equity.",
        keyDeliverable: "A coverage and recovery-waterfall analysis.",
      },
      {
        step: 7,
        trackId: "quality-moats",
        whyThisStep:
          "Separate durable business quality from a temporarily good year.",
        keyDeliverable: "A moat and capital-allocation scorecard.",
      },
      {
        step: 8,
        trackId: "bank-analysis",
        whyThisStep:
          "Handle financial institutions, where leverage and liquidity change the analysis.",
        keyDeliverable: "A bank capital, liquidity, and valuation review.",
      },
      {
        step: 9,
        trackId: "statistical-foundations",
        whyThisStep:
          "Acquire the time-value and scenario arithmetic required for valuation under uncertainty.",
        keyDeliverable: "Time-value, regression, and risk literacy.",
      },
      {
        step: 10,
        trackId: "valuation-uncertainty",
        whyThisStep:
          "Value high-uncertainty businesses with scenarios, real options, and reverse DCF.",
        keyDeliverable: "A scenario valuation with a price ceiling.",
      },
      {
        step: 11,
        trackId: "real-world-casebook",
        whyThisStep:
          "Apply the toolkit to documented accounting, solvency, and disclosure failures.",
        keyDeliverable: "A professional casebook investment memo.",
      },
    ],
  },
  {
    id: "quant-researcher",
    title: "Quantitative Researcher & Alpha Modeler",
    subtitle:
      "Statistics, econometrics, research methodology, strategy validation, ML, and the evaluation capstone.",
    targetRole: "Quant Researcher · Factor Modeler · Risk Analyst",
    badge: "Quant Research",
    description:
      "For mathematically minded learners who want the research core without the systems-engineering branch: statistical foundations, econometrics, the research platform, strategy lab, stock ML, and the capstone.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Anchor abstract statistics in actual market frictions and return arithmetic.",
        keyDeliverable: "Return, cost, and execution literacy.",
      },
      {
        step: 2,
        trackId: "statistical-foundations",
        whyThisStep:
          "Build probability, inference, regression, factor risk, and backtest foundations.",
        keyDeliverable: "A reproducible quantitative research report.",
      },
      {
        step: 3,
        trackId: "econometrics",
        whyThisStep:
          "Add identification, time series, volatility, panel, causal, and asset-pricing methods.",
        keyDeliverable: "A factor regression with robust diagnostics.",
      },
      {
        step: 4,
        trackId: "lab-workshop",
        whyThisStep:
          "Learn the research platform with the theory already in place.",
        keyDeliverable: "A saved research loop and evidence trail.",
      },
      {
        step: 5,
        trackId: "strategy-lab",
        whyThisStep:
          "Build and defend strategies with point-in-time data, costs, and portfolio constraints.",
        keyDeliverable: "A reproducible strategy dossier.",
      },
      {
        step: 6,
        trackId: "stock-machine-learning",
        whyThisStep:
          "Apply purged validation and regularized models to financial prediction.",
        keyDeliverable: "A validated ML pipeline and monitoring plan.",
      },
      {
        step: 7,
        trackId: "algorithm-evaluation",
        whyThisStep:
          "Audit the result for selection bias, costs, robustness, and uncertainty.",
        keyDeliverable: "An institutional-style algorithm evaluation report.",
      },
    ],
  },
  {
    id: "algorithmic-engineer",
    title: "Algorithmic Trading Engineer",
    subtitle:
      "Market mechanics, conduct, Python, strategy research, bots, C17/HPC, and execution evaluation.",
    targetRole:
      "Algorithmic Trader · Execution Engineer · Low-Latency Systems Developer",
    badge: "Engineering & Bots",
    description:
      "For learners who want to build trading systems: market and conduct foundations, programming, statistics, strategy research, an event-driven Python bot, C17 high-performance computing, and the evaluation capstone.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Learn orders, fills, costs, and risk before automating them.",
        keyDeliverable: "Exchange-mechanics fluency.",
      },
      {
        step: 2,
        trackId: "trading-ethics",
        whyThisStep: "Embed conduct rules before writing execution logic.",
        keyDeliverable: "A compliance and charter ruleset.",
      },
      {
        step: 3,
        trackId: "simulator-workshop",
        whyThisStep:
          "Practise order handling, slippage, margin, and short selling in the paper terminal.",
        keyDeliverable: "A supervised simulator trading week.",
      },
      {
        step: 4,
        trackId: "python-reluctant-investor",
        whyThisStep:
          "Acquire the Python basics used by every later worksheet and project.",
        keyDeliverable: "Working scripts for data, math, and charts.",
      },
      {
        step: 5,
        trackId: "statistical-foundations",
        whyThisStep:
          "Learn the statistics and risk metrics needed to evaluate signals.",
        keyDeliverable: "A quantitative research report.",
      },
      {
        step: 6,
        trackId: "econometrics",
        whyThisStep:
          "Understand inference, time series, and factor models before optimizing code.",
        keyDeliverable: "A robust factor and time-series analysis.",
      },
      {
        step: 7,
        trackId: "strategy-lab",
        whyThisStep:
          "Build cost-aware, validated strategies before deploying a bot.",
        keyDeliverable: "A defended strategy dossier.",
      },
      {
        step: 8,
        trackId: "stock-bots",
        whyThisStep:
          "Integrate execution, accounting, risk gates, ML, and operations.",
        keyDeliverable: "A durable event-driven paper bot.",
      },
      {
        step: 9,
        trackId: "c-hpc-trading",
        whyThisStep:
          "Re-engineer the research engine in C17 and optimize it with profiling and parallelism.",
        keyDeliverable: "A reproducible C trading research engine.",
      },
      {
        step: 10,
        trackId: "algorithm-evaluation",
        whyThisStep:
          "Evaluate returns, execution quality, computing performance, and uncertainty.",
        keyDeliverable: "A complete execution and algorithm report.",
      },
    ],
  },
  {
    id: "web3-defi",
    title: "Web3 & Decentralized Finance",
    subtitle:
      "Cryptography, ledgers, smart contracts, tokenomics, AMMs, DeFi risk, and research validation.",
    targetRole: "Web3 Researcher · Crypto Quant · Protocol Analyst",
    badge: "Crypto & DeFi",
    description:
      "A specialization branch that can be taken after the quantitative foundations without interrupting the equity and algorithmic core. It covers cryptography, blockchain ledgers, ERC-20 contracts, tokenomics, AMMs, impermanent loss, and DeFi risk.",
    steps: [
      {
        step: 1,
        trackId: "trading-fundamentals",
        whyThisStep:
          "Contrast traditional order books and settlement with on-chain markets.",
        keyDeliverable: "Market-microstructure baseline.",
      },
      {
        step: 2,
        trackId: "python-reluctant-investor",
        whyThisStep:
          "Acquire scripting and data basics used by the guided Web3 labs.",
        keyDeliverable: "Working Python data scripts.",
      },
      {
        step: 3,
        trackId: "data-hygiene",
        whyThisStep:
          "Chain data is unusually easy to misread; learn tidy, dated, reconciled evidence first.",
        keyDeliverable: "A cleaned, reproducible dataset.",
      },
      {
        step: 4,
        trackId: "statistical-foundations",
        whyThisStep:
          "Build probability, risk, and backtest literacy for token and pool analysis.",
        keyDeliverable: "A quantitative research report.",
      },
      {
        step: 5,
        trackId: "econometrics",
        whyThisStep:
          "Add time-series and factor methods for crypto return and liquidity research.",
        keyDeliverable: "A crypto time-series and factor analysis.",
      },
      {
        step: 6,
        trackId: "web3",
        whyThisStep:
          "Study cryptography, ledgers, smart contracts, tokenomics, AMMs, and DeFi risk.",
        keyDeliverable: "A signed native-coin and ERC-20 project dossier.",
      },
      {
        step: 7,
        trackId: "strategy-lab",
        whyThisStep:
          "Test multi-asset and DeFi strategies with the same validation discipline as equity research.",
        keyDeliverable: "A validated multi-asset strategy dossier.",
      },
      {
        step: 8,
        trackId: "algorithm-evaluation",
        whyThisStep:
          "Audit the strategy's returns, costs, risk, and uncertainty in a final report.",
        keyDeliverable: "A complete algorithm evaluation report.",
      },
    ],
  },
];
