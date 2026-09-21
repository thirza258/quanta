import { describe, expect, it } from "vitest";
import { exams, trackLabel, tracks } from "./catalog";
import { lessonExercises } from "./progress";

const course = tracks.find((track) => track.id === "news-to-markets")!;

describe("news-to-company learning progression", () => {
  it("follows Security Analysis without renumbering existing lesson URLs", () => {
    const index = tracks.findIndex((track) => track.id === "security-analysis");
    expect(tracks[index + 1]).toBe(course);
    expect(trackLabel(course)).toBe("TRACK 04");
    expect(course.modules[0].id).toBe("8.1");
    expect(tracks[index + 2].modules[0].id).toBe("2.1");
    expect(
      tracks.find((track) => track.id === "stock-machine-learning")?.modules[0]
        .id,
    ).toBe("7.1");
  });

  it("provides twelve hours of applied study with a complete news research lifecycle", () => {
    expect(course.modules).toHaveLength(24);
    expect(course.parts).toHaveLength(6);
    expect(
      course.modules.reduce((sum, lesson) => sum + lesson.minutes, 0),
    ).toBe(720);
    expect(course.modules.flatMap(lessonExercises)).toHaveLength(48);
    expect(
      course.modules.some((lesson) => lesson.title.includes("Rupiah")),
    ).toBe(true);
    expect(course.modules.at(-1)?.title).toContain("Capstone");
    expect(course.readingGuide).toContain("exam time is additional");
    for (const lesson of course.modules) {
      expect(lesson.content.split(/\s+/).length).toBeGreaterThan(200);
      expect(lesson.assignment?.prompt.length).toBeGreaterThan(50);
      expect(lesson.assignment?.solution.length).toBeGreaterThan(100);
      expect(lesson.references?.length).toBeGreaterThanOrEqual(2);
      expect(lesson.reading).toContain("fictional teaching case");
    }
  });

  it("assesses every unit with separate practice, checkpoint and final questions", () => {
    expect(course.exams).toHaveLength(7);
    const final = course.exams.at(-1)!;
    expect(final.version).toBe(1);
    expect(final.questions).toHaveLength(24);
    expect(exams).toContain(final);
    for (const [index, checkpoint] of course.exams.slice(0, -1).entries()) {
      expect(checkpoint.moduleIds).toEqual(
        course.modules.slice(index * 4, index * 4 + 4).map((m) => m.id),
      );
      expect(checkpoint.questions).toHaveLength(4);
    }
    const prompts = [
      ...course.modules.flatMap(lessonExercises),
      ...course.exams.flatMap((exam) => exam.questions),
    ].map((q) => q.question);
    expect(new Set(prompts).size).toBe(96);
  });
});
