import { describe, it, expect } from "vitest";
import { tracks, lessons, exams, findLesson, lessonTrack } from "./catalog";
import { lessonExercises } from "./learning";
import { percent } from "./api";
describe("curriculum integrity", () => {
  it("resolves unique lessons to their parent tracks", () => {
    expect(tracks).toHaveLength(7);
    expect(tracks[0].id).toBe("trading-fundamentals");
    expect(lessons).toHaveLength(37);
    expect(new Set(lessons.map((l) => l.id)).size).toBe(37);
    expect(findLesson("1.1")?.title).toBe("Foundations of Graham & Dodd");
    for (const lesson of lessons) {
      expect(findLesson(lesson.id)).toBe(lesson);
      expect(lessonTrack(lesson.id)?.modules).toContain(lesson);
    }
  });
  it("offers complete, uniquely identified exams and valid practice questions", () => {
    expect(exams).toHaveLength(8);
    expect(new Set(exams.map((exam) => exam.id)).size).toBe(exams.length);
    for (const track of tracks) {
      expect(track.exams.filter((exam) => exam.kind === "final")).toHaveLength(
        1,
      );
      for (const exam of track.exams) {
        expect(exam.questions.length).toBeGreaterThanOrEqual(4);
        expect(new Set(exam.questions.map((q) => q.id)).size).toBe(
          exam.questions.length,
        );
        expect(exam.passingScore).toBeGreaterThan(0);
        expect(exam.passingScore).toBeLessThanOrEqual(100);
        expect(new Set(exam.questions.map((q) => q.lessonId))).toEqual(
          new Set(exam.moduleIds),
        );
        for (const q of exam.questions) {
          expect(exam.moduleIds).toContain(q.lessonId);
          expect(track.modules.some((lesson) => lesson.id === q.lessonId)).toBe(
            true,
          );
          expect(Number.isInteger(q.answer)).toBe(true);
          expect(q.options[q.answer]).toBeTruthy();
          expect(q.explanation.length).toBeGreaterThan(20);
          expect(
            lessonExercises(findLesson(q.lessonId)!).map((p) => p.question),
          ).not.toContain(q.question);
        }
      }
      for (const lesson of track.modules) {
        for (const q of lessonExercises(lesson))
          expect(q.options[q.answer]).toBeTruthy();
        for (const [, slug] of lesson.content.matchAll(
          /\]\(\/curriculum\/([a-z-]+)\)/g,
        )) {
          expect(tracks.some((item) => item.id === slug)).toBe(true);
        }
      }
    }
    expect(
      tracks[0].modules.reduce(
        (sum, lesson) => sum + lessonExercises(lesson).length,
        0,
      ),
    ).toBe(24);
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
