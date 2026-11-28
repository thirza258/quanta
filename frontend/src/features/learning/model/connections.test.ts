import { tracks } from "@/features/learning/model/catalog";
import {
  arePrerequisitesMet,
  courseConnections,
  getConnection,
  getCourseReadiness,
  getMissingPrerequisites,
  getRecommendedNextTracks,
  learningPathways,
} from "./connections";
import type { WorkspaceState } from "@/features/workspace/model/types";
import { describe, expect, it } from "vitest";

const emptyState: WorkspaceState = {
  completed: [],
  lastLesson: "",
  drafts: {},
  notes: [],
  experiments: [],
  submissions: {},
  examDrafts: {},
  examAttempts: {},
  runs: 0,
};

describe("courseConnections model", () => {
  it("covers all 28 tracks from curriculum.json", () => {
    expect(tracks.length).toBe(28);
    expect(courseConnections.length).toBe(tracks.length);

    const trackIds = new Set(tracks.map((t) => t.id));
    for (const conn of courseConnections) {
      expect(trackIds.has(conn.id)).toBe(true);
    }
  });

  it("has valid prerequisite and unlock IDs referencing real tracks", () => {
    const trackIds = new Set(tracks.map((t) => t.id));
    for (const conn of courseConnections) {
      for (const prereqId of [
        ...conn.prerequisites,
        ...conn.prerequisitesAnyOf,
      ]) {
        expect(
          trackIds.has(prereqId),
          `Invalid prereq ${prereqId} in ${conn.id}`,
        ).toBe(true);
        expect(prereqId).not.toBe(conn.id);
      }
      for (const recId of conn.recommendedBefore) {
        expect(
          trackIds.has(recId),
          `Invalid recommendedBefore ${recId} in ${conn.id}`,
        ).toBe(true);
        expect(recId).not.toBe(conn.id);
      }
      for (const unlockId of conn.unlocks) {
        expect(
          trackIds.has(unlockId),
          `Invalid unlock ${unlockId} in ${conn.id}`,
        ).toBe(true);
        expect(unlockId).not.toBe(conn.id);
      }
    }
  });

  it("orders the catalog by explicit sequence and keeps prerequisites earlier", () => {
    const sequences = tracks.map((track) => track.sequence ?? 0);
    expect(sequences).toEqual([...sequences].sort((a, b) => a - b));
    expect(new Set(sequences).size).toBe(tracks.length);
    const position = new Map(tracks.map((track, index) => [track.id, index]));
    for (const track of tracks) {
      for (const prerequisite of [
        ...(track.prerequisite_course_ids ?? []),
        ...(track.prerequisite_any_of ?? []),
        ...(track.recommended_course_ids ?? []),
      ]) {
        expect(
          position.get(prerequisite),
          `${prerequisite} must precede ${track.id}`,
        ).toBeLessThan(position.get(track.id)!);
      }
    }
  });

  it("exposes stage, difficulty, and course-role metadata", () => {
    for (const track of tracks) {
      expect(track.stage_number).toBeGreaterThanOrEqual(1);
      expect(track.stage_number).toBeLessThanOrEqual(12);
      expect(track.sequence).toBeGreaterThan(0);
      expect(track.difficulty).toBeGreaterThanOrEqual(0);
      expect(track.difficulty).toBeLessThanOrEqual(5);
      expect(track.focus_summary).toBeTruthy();
      expect(track.skills?.length).toBeGreaterThanOrEqual(3);
      expect(track.course_type).toBeTruthy();
    }
    expect(
      tracks.find((track) => track.id === "algorithm-evaluation")?.is_capstone,
    ).toBe(true);
    expect(tracks.find((track) => track.id === "web3")?.is_specialization).toBe(
      true,
    );
    expect(tracks.find((track) => track.id === "strategy-lab")?.is_core).toBe(
      true,
    );
  });

  it("contains no circular dependencies in strict prerequisites (is a valid DAG)", () => {
    const adj = new Map<string, string[]>();
    for (const conn of courseConnections) {
      adj.set(conn.id, [...conn.prerequisites, ...conn.prerequisitesAnyOf]);
    }

    const visited = new Set<string>();
    const recStack = new Set<string>();

    function hasCycle(node: string): boolean {
      visited.add(node);
      recStack.add(node);

      for (const neighbor of adj.get(node) || []) {
        if (!visited.has(neighbor)) {
          if (hasCycle(neighbor)) return true;
        } else if (recStack.has(neighbor)) {
          return true;
        }
      }

      recStack.delete(node);
      return false;
    }

    for (const conn of courseConnections) {
      if (!visited.has(conn.id)) {
        expect(hasCycle(conn.id)).toBe(false);
      }
    }
  });

  it("defines valid curated learning pathways", () => {
    expect(learningPathways.length).toBeGreaterThanOrEqual(4);
    const trackIds = new Set(tracks.map((t) => t.id));

    for (const pathway of learningPathways) {
      expect(pathway.title).toBeTruthy();
      expect(pathway.steps.length).toBeGreaterThan(0);
      pathway.steps.forEach((step, idx) => {
        expect(step.step).toBe(idx + 1);
        expect(
          trackIds.has(step.trackId),
          `Unknown track ${step.trackId} in pathway ${pathway.id}`,
        ).toBe(true);
        expect(step.whyThisStep).toBeTruthy();
        expect(step.keyDeliverable).toBeTruthy();
      });
    }
  });

  it("evaluates prerequisites and readiness correctly for an empty state", () => {
    // trading-fundamentals has no prerequisites, so it should be ready
    expect(arePrerequisitesMet("trading-fundamentals", emptyState)).toBe(true);
    expect(
      getCourseReadiness(
        tracks.find((t) => t.id === "trading-fundamentals")!,
        emptyState,
      ),
    ).toBe("ready");

    // trading-ethics requires trading-fundamentals, so it should be locked
    expect(arePrerequisitesMet("trading-ethics", emptyState)).toBe(false);
    expect(
      getCourseReadiness(
        tracks.find((t) => t.id === "trading-ethics")!,
        emptyState,
      ),
    ).toBe("locked");

    const missing = getMissingPrerequisites("trading-ethics", emptyState);
    expect(missing.map((t) => t.id)).toContain("trading-fundamentals");

    const recommended = getRecommendedNextTracks(emptyState);
    expect(recommended.length).toBeGreaterThan(0);
    expect(recommended[0].id).toBe("trading-fundamentals");
  });

  it("requires one-of algorithms for the final capstone, not every branch", () => {
    const complete = (trackId: string) => {
      const track = tracks.find((item) => item.id === trackId)!;
      const state: WorkspaceState = {
        ...emptyState,
        completed: track.modules.map((lesson) => lesson.id),
        examAttempts: Object.fromEntries(
          track.exams.map((exam) => [
            exam.id,
            [
              {
                id: `${exam.id}-pass`,
                examId: exam.id,
                version: exam.version,
                startedAt: "2026-01-01T00:00:00Z",
                submittedAt: "2026-01-01T00:01:00Z",
                answers: {},
                correctCount: exam.questions.length,
                total: exam.questions.length,
                score: 100,
                passed: true,
                grading: "device" as const,
              },
            ],
          ]),
        ),
      };
      return state;
    };
    const strategy = complete("strategy-lab");
    const withStrategy: WorkspaceState = {
      ...emptyState,
      ...strategy,
      completed: [...strategy.completed],
      examAttempts: { ...strategy.examAttempts },
    };
    expect(arePrerequisitesMet("algorithm-evaluation", withStrategy)).toBe(
      false,
    );

    const ml = complete("stock-machine-learning");
    const withMl: WorkspaceState = {
      ...withStrategy,
      completed: [...withStrategy.completed, ...ml.completed],
      examAttempts: {
        ...withStrategy.examAttempts,
        ...ml.examAttempts,
      },
    };
    expect(arePrerequisitesMet("algorithm-evaluation", withMl)).toBe(true);

    const casebookOptions = getMissingPrerequisites(
      "real-world-casebook",
      emptyState,
    ).map((track) => track.id);
    expect(casebookOptions).toEqual(
      expect.arrayContaining([
        "security-analysis",
        "forensic-accounting",
        "credit-distress",
        "bank-analysis",
      ]),
    );
  });

  it("retrieves a connection by track ID", () => {
    const conn = getConnection("security-analysis");
    expect(conn).toBeDefined();
    expect(conn?.domain).toBe("value");
    expect(conn?.stage).toBe(3);
    expect(conn?.prerequisites).toContain("trading-fundamentals");
  });
});
