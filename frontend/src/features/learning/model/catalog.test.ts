import {
  exams,
  findLesson,
  lessons,
  lessonTrack,
  tracks,
} from "@/features/learning/model/catalog";
import { lessonExercises } from "@/features/learning/model/progress";
import { percent } from "@/shared/lib/format";
import { describe, expect, it } from "vitest";
describe("curriculum integrity", () => {
  it.each([
    ["econometrics", 32, 8, 2],
    ["web3", 24, 6, 2],
    ["stock-machine-learning", 24, 6, 1],
  ])(
    "provides the complete applied %s course",
    (slug, count, units, version) => {
      const course = tracks.find((track) => track.id === slug)!;
      expect(course.studyType).toBe("applied");
      expect(course.modules).toHaveLength(Number(count));
      expect(course.parts).toHaveLength(Number(units));
      expect(course.exams).toHaveLength(Number(units));
      expect(course.exams.at(-1)?.version).toBe(version);
      expect(course.exams.at(-1)?.questions).toHaveLength(Number(count));
      expect(course.exams.at(-1)?.moduleIds).toEqual(
        course.modules.map((m) => m.id),
      );
      const prompts = course.exams.flatMap((exam) =>
        exam.questions.map((q) => q.question),
      );
      expect(new Set(prompts).size).toBe(prompts.length);
      for (const part of course.parts!) {
        expect(course.modules.filter((m) => m.part === part.id)).toHaveLength(
          4,
        );
      }
      for (const lesson of course.modules) {
        expect(lesson.kind).toBe("applied-study");
        expect(lessonExercises(lesson)).toHaveLength(2);
        expect(lesson.content.split(/\s+/).length).toBeGreaterThan(200);
        expect(lesson.assignment?.prompt.length).toBeGreaterThan(30);
        expect(lesson.assignment?.solution.length).toBeGreaterThan(30);
      }
    },
  );
  it("budgets twelve hours of ML lessons separately from its exams", () => {
    const course = tracks.find(
      (track) => track.id === "stock-machine-learning",
    )!;
    expect(
      course.modules.reduce((total, lesson) => total + lesson.minutes, 0),
    ).toBe(720);
    expect(course.modules.every((lesson) => lesson.minutes === 30)).toBe(true);
    expect(course.readingGuide).toContain("exam time is additional");
  });
  it("attributes every course and lesson to named sources", () => {
    for (const item of [...tracks, ...lessons]) {
      expect(item.references?.length).toBeGreaterThan(0);
      for (const reference of item.references ?? []) {
        expect(reference.title.length).toBeGreaterThan(10);
        expect(new URL(reference.url).protocol).toBe("https:");
      }
    }
  });
  it("provides an applied bot course with independent assessments and downloadable projects", () => {
    const course = tracks.find((track) => track.id === "stock-bots")!;
    expect(course.studyType).toBe("applied");
    expect(course.modules).toHaveLength(48);
    expect(course.parts).toHaveLength(12);
    expect(course.exams).toHaveLength(12);
    expect(course.resources).toHaveLength(5);
    expect(course.exams.at(-1)?.version).toBe(3);
    expect(course.exams.at(-1)?.moduleIds).toEqual(
      course.modules.map((lesson) => lesson.id),
    );
    const prompts = course.exams.flatMap((exam) =>
      exam.questions.map((question) => question.question),
    );
    expect(new Set(prompts).size).toBe(92);
    for (const lesson of course.modules) {
      expect(lesson.kind).toBe("applied-study");
      expect(lessonExercises(lesson)).toHaveLength(2);
      expect(lesson.assignment?.prompt).toBeTruthy();
      expect(lesson.assignment?.solution).toBeTruthy();
      expect(lesson.content.split(/\s+/).length).toBeGreaterThan(200);
    }
  });
  it("resolves unique lessons to their parent tracks", () => {
    expect(tracks).toHaveLength(11);
    expect(tracks[0].id).toBe("trading-fundamentals");
    expect(lessons).toHaveLength(256);
    expect(new Set(lessons.map((l) => l.id)).size).toBe(256);
    expect(findLesson("1.1")?.title).toBe("Foundations of Graham & Dodd");
    for (const lesson of lessons) {
      expect(findLesson(lesson.id)).toBe(lesson);
      expect(lessonTrack(lesson.id)?.modules).toContain(lesson);
    }
  });
  it("offers complete, uniquely identified exams and valid practice questions", () => {
    expect(exams).toHaveLength(64);
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
      expect(lesson.code).toContain(
        lesson.codeLanguage === "c" ? "int main(void)" : "def strategy(data)",
      );
    }
  });
  it("does not display an undefined risk ratio as zero", () => {
    expect(percent(null)).toBe("—");
    expect(percent(undefined)).toBe("—");
    expect(percent(0)).toBe("0.0%");
    expect(percent(-0.25)).toBe("-25.0%");
  });
  it("provides a complete reading map and independent assessments for both book courses", () => {
    for (const [slug, count, parts] of [
      ["security-analysis", 24, 8],
      ["statistical-foundations", 28, 14],
    ] as const) {
      const track = tracks.find((item) => item.id === slug)!;
      expect(track.modules).toHaveLength(count);
      expect(track.parts).toHaveLength(parts);
      expect(new Set(track.modules.map((lesson) => lesson.part))).toEqual(
        new Set(track.parts!.map((part) => part.id)),
      );
      expect(
        track.exams.filter((exam) => exam.kind === "checkpoint"),
      ).toHaveLength(4);
      const final = track.exams.find((exam) => exam.kind === "final")!;
      expect(final.version).toBe(2);
      expect(final.moduleIds).toEqual(track.modules.map((lesson) => lesson.id));
      const allQuestions = track.exams.flatMap((exam) =>
        exam.questions.map((question) => question.question),
      );
      expect(new Set(allQuestions).size).toBe(allQuestions.length);
      for (const lesson of track.modules) {
        expect(lessonExercises(lesson)).toHaveLength(2);
        expect(lesson.reading).toBeTruthy();
        expect(lesson.assignment?.prompt).toBeTruthy();
        expect(lesson.assignment?.solution).toBeTruthy();
        expect(lesson.content).toContain("$$");
      }
      expect(track.modules.at(-1)?.title).toContain("Capstone");
    }
    expect(findLesson("1.5")?.part).toBe("VIII");
    expect(findLesson("1.5")?.reading).toContain(
      "not presented as methods from the 1940 text",
    );
  });
});
