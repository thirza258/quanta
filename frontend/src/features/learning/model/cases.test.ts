import { tracks } from "@/features/learning/model/catalog";
import {
  caseLessonLinks,
  caseNotebookPrompt,
  lessonCase,
} from "@/features/learning/model/cases";
import { describe, expect, it } from "vitest";

describe("real-world learning navigation", () => {
  it("links each course and unit case to a lesson that actually teaches it", () => {
    for (const track of tracks) {
      const links = caseLessonLinks(track);
      expect(new Set(links.map((link) => link.caseStudy.id))).toEqual(
        new Set(track.caseStudies.map((item) => item.id)),
      );
      for (const part of track.parts ?? []) {
        const unitLinks = caseLessonLinks(track, part.id);
        const modules = track.modules.filter(
          (lesson) => lesson.part === part.id,
        );
        expect(new Set(unitLinks.map((link) => link.caseStudy.id))).toEqual(
          new Set(modules.map((lesson) => lesson.realWorld.caseId)),
        );
        for (const link of unitLinks) {
          const lesson = modules.find((item) => item.id === link.lessonId)!;
          expect(lessonCase(track, lesson)).toBe(link.caseStudy);
        }
      }
    }
  });

  it("keeps the task, source, scope, and historical boundary in notebook prompts without giving away the walkthrough", () => {
    const track = tracks.find((item) => item.id === "news-to-markets")!;
    const lesson = track.modules.find((item) => item.id === "8.3")!;
    const caseStudy = lessonCase(track, lesson)!;
    const prompt = caseNotebookPrompt(lesson, caseStudy);
    expect(prompt).toContain(lesson.realWorld.task);
    expect(prompt).toContain(caseStudy.period);
    expect(prompt).toContain(caseStudy.boundary);
    expect(prompt).toContain(caseStudy.references[0].url);
    expect(prompt).toContain(caseStudy.references[0].scope);
    expect(prompt).not.toContain(lesson.realWorld.walkthrough);
    expect(prompt.length).toBeLessThan(20000);
  });
});
