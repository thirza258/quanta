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
      for (const prereqId of conn.prerequisites) {
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

  it("contains no circular dependencies in strict prerequisites (is a valid DAG)", () => {
    const adj = new Map<string, string[]>();
    for (const conn of courseConnections) {
      adj.set(conn.id, conn.prerequisites);
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

  it("retrieves a connection by track ID", () => {
    const conn = getConnection("security-analysis");
    expect(conn).toBeDefined();
    expect(conn?.domain).toBe("value");
    expect(conn?.stage).toBe(2);
    expect(conn?.prerequisites).toContain("trading-fundamentals");
  });
});
