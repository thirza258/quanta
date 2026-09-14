import { describe, expect, it } from "vitest";
import { tracks } from "./catalog";
import { lessonExercises } from "./progress";

const course = tracks.find((track) => track.id === "algorithm-evaluation")!;
describe("final algorithm evaluation track", () => {
  it("closes the learning sequence after the algorithm and ML courses", () => {
    expect(tracks.at(-1)).toBe(course);
    expect(tracks.at(-2)?.id).toBe("stock-machine-learning");
    expect(course.modules[0].id).toBe("10.1");
    expect(course.modules.at(-1)?.id).toBe("10.16");
  });
  it("provides complete report-building study and a distinct final assessment", () => {
    expect(course.modules).toHaveLength(16);
    expect(course.parts).toHaveLength(4);
    expect(
      course.modules.reduce((sum, lesson) => sum + lesson.minutes, 0),
    ).toBe(480);
    expect(course.exams).toHaveLength(5);
    expect(course.exams.at(-1)?.questions).toHaveLength(16);
    expect(course.exams.at(-1)?.version).toBe(1);
    const prompts = [
      ...course.modules.flatMap(lessonExercises),
      ...course.exams.flatMap((exam) => exam.questions),
    ].map((q) => q.question);
    expect(prompts).toHaveLength(64);
    expect(new Set(prompts).size).toBe(64);
    for (const lesson of course.modules) {
      expect(lesson.content.split(/\s+/).length).toBeGreaterThan(200);
      expect(lesson.assignment?.solution).toBeTruthy();
      expect(lesson.references?.length).toBeGreaterThanOrEqual(2);
    }
  });
  it("assesses every unit before the final dossier", () => {
    for (const [index, exam] of course.exams.slice(0, -1).entries()) {
      expect(exam.moduleIds).toEqual(
        course.modules
          .slice(index * 4, index * 4 + 4)
          .map((lesson) => lesson.id),
      );
    }
    expect(course.exams.at(-1)?.moduleIds).toEqual(
      course.modules.map((lesson) => lesson.id),
    );
    expect(course.readingGuide).toContain("exam time is additional");
  });
});
