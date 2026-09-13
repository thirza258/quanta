import { describe, it, expect } from "vitest";
import { tracks, lessons, findLesson, lessonTrack } from "./catalog";
import { percent } from "./api";
describe("curriculum integrity", () => {
  it("resolves unique lessons to their parent tracks", () => {
    expect(tracks).toHaveLength(6);
    expect(lessons).toHaveLength(29);
    expect(new Set(lessons.map((l) => l.id)).size).toBe(29);
    for (const lesson of lessons) {
      expect(findLesson(lesson.id)).toBe(lesson);
      expect(lessonTrack(lesson.id)?.modules).toContain(lesson);
    }
  });
  it("contains valid exercises and original worked examples", () => {
    for (const lesson of lessons) {
      expect(lesson.exercise.answer).toBeLessThan(
        lesson.exercise.options.length,
      );
      expect(lesson.exercise.answer).toBeGreaterThanOrEqual(0);
      expect(lesson.content).toContain("## A worked example");
      expect(lesson.code).toContain("def strategy(data)");
    }
  });
  it("does not display an undefined risk ratio as zero", () => {
    expect(percent(null)).toBe("—");
    expect(percent(undefined)).toBe("—");
    expect(percent(0)).toBe("0.0%");
    expect(percent(-0.25)).toBe("-25.0%");
  });
});
