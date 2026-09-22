import { lessonExercises } from "@/features/learning/model/progress";
import { describe, expect, it } from "vitest";
import { findLesson, trackLabel, tracks } from "./catalog";

const course = tracks.find((track) => track.id === "trading-ethics")!;

describe("trading ethics and market conduct", () => {
  it("follows the fundamentals so conduct is taught before valuation or automation", () => {
    const index = tracks.findIndex((track) => track.id === "trading-ethics");
    expect(tracks[index - 1].id).toBe("trading-fundamentals");
    expect(trackLabel(course)).toBe("TRACK 01");
    expect(course.level).toBe("Foundational");
    expect(course.prerequisites).toContain("Trading & market fundamentals");
    // The course must not be mistaken for professional advice.
    expect(course.prerequisites).toContain("not legal or compliance advice");
    expect(course.readingGuide).toContain("jurisdiction");
  });

  it("provides sixteen lessons in four units with independent assessments", () => {
    expect(course.studyType).toBe("applied");
    expect(course.modules).toHaveLength(16);
    expect(course.parts).toHaveLength(4);
    expect(course.modules.map((lesson) => lesson.id)).toEqual(
      Array.from({ length: 16 }, (_, i) => `12.${i + 1}`),
    );
    expect(
      course.modules.reduce((sum, lesson) => sum + lesson.minutes, 0),
    ).toBe(480);
    expect(course.exams).toHaveLength(5);
    expect(
      course.exams.filter((exam) => exam.kind === "checkpoint"),
    ).toHaveLength(4);
    expect(course.exams.at(-1)?.questions).toHaveLength(16);
    expect(course.exams.at(-1)?.moduleIds).toEqual(
      course.modules.map((lesson) => lesson.id),
    );
    for (const [index, checkpoint] of course.exams.slice(0, -1).entries()) {
      expect(checkpoint.moduleIds).toEqual(
        course.modules.slice(index * 4, index * 4 + 4).map((m) => m.id),
      );
      expect(checkpoint.questions).toHaveLength(4);
    }
    for (const part of course.parts!) {
      expect(course.modules.filter((m) => m.part === part.id)).toHaveLength(4);
    }
  });

  it("asks sixty-four distinct questions and never reuses a prompt", () => {
    const prompts = [
      ...course.modules.flatMap(lessonExercises),
      ...course.exams.flatMap((exam) => exam.questions),
    ].map((question) => question.question);
    expect(prompts).toHaveLength(64);
    expect(new Set(prompts).size).toBe(64);
    for (const question of course.exams.flatMap((exam) => exam.questions)) {
      expect(question.options.length).toBeGreaterThanOrEqual(3);
      expect(question.answer).toBeGreaterThanOrEqual(0);
      expect(question.answer).toBeLessThan(question.options.length);
      expect(question.explanation.length).toBeGreaterThan(20);
    }
  });

  it("gives every lesson a checkable do-and-do-not rule and named sources", () => {
    for (const lesson of course.modules) {
      expect(lesson.kind).toBe("applied-study");
      expect(lesson.minutes).toBe(30);
      expect(lesson.content.split(/\s+/).length).toBeGreaterThan(250);
      // The practical half of the course: every lesson ends in a rule you can follow.
      expect(lesson.content).toContain("### Do and do not");
      expect(lesson.content).toContain("- **Do not**");
      expect(lesson.content).toContain("Add it to your charter");
      expect(lessonExercises(lesson)).toHaveLength(2);
      expect(lesson.assignment?.solution.length).toBeGreaterThan(100);
      expect(lesson.references?.length).toBeGreaterThanOrEqual(2);
      for (const reference of lesson.references ?? []) {
        expect(new URL(reference.url).protocol).toBe("https:");
      }
      expect(lesson.realWorld?.caseId).toBeTruthy();
      expect(lesson.reading).toContain("invented");
    }
  });

  it("builds from duty and disclosure to a written charter", () => {
    expect(findLesson("12.1")?.title).toBe(
      "Whose interest the decision serves",
    );
    expect(findLesson("12.5")?.title).toBe("Material non-public information");
    expect(findLesson("12.9")?.title).toBe(
      "Accountability for a system that trades",
    );
    expect(findLesson("12.16")?.title).toBe("Your written trading charter");
    expect(course.parts?.map((part) => part.title)).toEqual([
      "Duty, conflict and disclosure",
      "Market integrity",
      "Conduct in automated and quantitative work",
      "Care, refusal and record",
    ]);
  });
});
