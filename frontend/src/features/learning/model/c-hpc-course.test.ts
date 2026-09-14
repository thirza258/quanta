import { describe, expect, it } from "vitest";
import { tracks } from "./catalog";
import { lessonExercises } from "./progress";

const course = tracks.find((track) => track.id === "c-hpc-trading")!;
describe("C and HPC course progression", () => {
  it("follows the Python bot course without changing existing lesson identifiers", () => {
    const index = tracks.findIndex((track) => track.id === "stock-bots");
    expect(tracks[index + 1]).toBe(course);
    expect(tracks[index].modules.some((lesson) => lesson.id === "5.1")).toBe(
      true,
    );
    expect(
      tracks[index + 2].modules.some((lesson) => lesson.id === "6.1"),
    ).toBe(true);
    expect(course.modules[0].id).toBe("9.1");
  });
  it("provides twelve hours of C lessons and independent unit/final assessments", () => {
    expect(course.modules).toHaveLength(24);
    expect(course.parts).toHaveLength(6);
    expect(
      course.modules.reduce((sum, lesson) => sum + lesson.minutes, 0),
    ).toBe(720);
    expect(course.exams).toHaveLength(7);
    expect(course.exams.at(-1)?.version).toBe(1);
    const prompts = [
      ...course.modules.flatMap(lessonExercises),
      ...course.exams.flatMap((exam) => exam.questions),
    ].map((q) => q.question);
    expect(prompts).toHaveLength(96);
    expect(new Set(prompts).size).toBe(96);
    for (const [index, checkpoint] of course.exams.slice(0, -1).entries()) {
      expect(checkpoint.moduleIds).toEqual(
        course.modules.slice(index * 4, index * 4 + 4).map((m) => m.id),
      );
    }
  });
  it("marks every worksheet as C with references, a local workflow and expected output", () => {
    for (const lesson of course.modules) {
      expect(lesson.codeLanguage).toBe("c");
      expect(lesson.code).not.toContain("def strategy");
      expect(lesson.expectedOutput).toBeTruthy();
      expect(lesson.content.split(/\s+/).length).toBeGreaterThan(200);
      expect(lesson.assignment?.prompt).toBeTruthy();
      expect(lesson.assignment?.solution).toBeTruthy();
      expect(lesson.references?.length).toBeGreaterThanOrEqual(2);
    }
  });
});
