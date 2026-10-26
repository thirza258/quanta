import { describe, expect, it } from "vitest";
import { findLesson, tracks } from "./catalog";
import { examPassed, lessonExercises, practiceComplete } from "./progress";
import { normalize } from "@/features/workspace/model/state";

describe("careful-investor and strategy research progression", () => {
  it("places the investor companion directly before Security Analysis and keeps evaluation last", () => {
    expect(tracks.slice(0, 7).map((course) => course.id)).toEqual([
      "trading-fundamentals",
      "trading-ethics",
      "simulator-workshop",
      "lab-workshop",
      "intelligent-investor",
      "security-analysis",
      "news-to-markets",
    ]);
    expect(tracks.at(-1)?.id).toBe("algorithm-evaluation");
    expect(
      tracks.find((course) => course.id === "intelligent-investor")
        ?.readingGuide,
    ).toContain("not the full book");
  });

  // The capstone is named rather than taken from the end of the course: the
  // investor course now carries a unit after it, and a positional lookup would
  // silently start checking whichever lesson happened to be last.
  it.each([
    ["strategy-lab", 32, 8, 2, "4.32"],
    ["intelligent-investor", 20, 5, 2, "11.16"],
  ] as const)(
    "provides complete %s lessons, references and independent assessments",
    (slug, count, units, version, capstoneId) => {
      const course = tracks.find((track) => track.id === slug)!;
      expect(course.modules).toHaveLength(count);
      expect(course.parts).toHaveLength(units);
      expect(
        course.modules.reduce((sum, lesson) => sum + lesson.minutes, 0),
      ).toBe(count * 30);
      expect(course.exams).toHaveLength(units + 1);
      expect(course.exams.at(-1)?.version).toBe(version);
      expect(course.exams.at(-1)?.questions).toHaveLength(count);
      const prompts = [
        ...course.modules.flatMap(lessonExercises),
        ...course.exams.flatMap((exam) => exam.questions),
      ].map((q) => q.question);
      expect(prompts).toHaveLength(count * 4);
      expect(new Set(prompts).size).toBe(count * 4);
      for (const [index, checkpoint] of course.exams.slice(0, -1).entries()) {
        expect(checkpoint.moduleIds).toEqual(
          course.modules.slice(index * 4, index * 4 + 4).map((m) => m.id),
        );
        expect(checkpoint.questions).toHaveLength(4);
      }
      for (const lesson of course.modules) {
        expect(lesson.content.split(/\s+/).length).toBeGreaterThan(250);
        expect(lesson.assignment?.solution.length).toBeGreaterThan(100);
        expect(lesson.references?.length).toBeGreaterThanOrEqual(2);
        expect(lessonExercises(lesson)).toHaveLength(2);
      }
      expect(course.resources).toHaveLength(3);
      expect(
        course.modules.find((lesson) => lesson.id === capstoneId)?.title,
      ).toContain("Capstone");
    },
  );

  it("preserves legacy strategy answer keys while requiring the expanded practice and final", () => {
    const expected = [
      ["4.1", "The systematic net-net screen", 1],
      ["4.2", "Quality at a reasonable price", 1],
      ["4.3", "Statistical arbitrage pairs", 1],
      ["4.4", "Cross-sectional machine learning", 2],
    ] as const;
    for (const [id, title, answer] of expected) {
      const lesson = findLesson(id)!;
      expect(lesson.title).toBe(title);
      expect(lesson.exercise.answer).toBe(answer);
      expect(lesson.exercises?.[0]).toEqual(lesson.exercise);
      const state = normalize({
        completed: [id],
        submissions: { [id]: { answer, correct: true } },
      });
      expect(state.completed).toContain(id);
      expect(practiceComplete(lesson, state)).toBe(false);
    }
    const exam = tracks
      .find((track) => track.id === "strategy-lab")!
      .exams.at(-1)!;
    const old = {
      id: "old-strategy-final",
      examId: exam.id,
      version: 1,
      startedAt: "2026-09-01T00:00:00Z",
      submittedAt: "2026-09-01T00:12:00Z",
      answers: {},
      correctCount: 4,
      total: 4,
      score: 100,
      passed: true,
      grading: "device" as const,
    };
    const state = normalize({ examAttempts: { [exam.id]: [old] } });
    expect(state.examAttempts[exam.id]).toHaveLength(1);
    expect(examPassed(exam, state)).toBe(false);
  });
});
