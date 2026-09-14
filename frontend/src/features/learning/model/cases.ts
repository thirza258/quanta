import type { CaseStudy, Lesson, Track } from "@/features/learning/model/types";

export const caseKindLabels: Record<CaseStudy["kind"], string> = {
  documented: "Documented event",
  implementation: "Practical implementation",
  illustrative: "Everyday scenario",
};

export function lessonCase(track: Track, lesson: Lesson) {
  return track.caseStudies.find((item) => item.id === lesson.realWorld.caseId);
}

export function caseLessonLinks(track: Track, part?: string) {
  const modules =
    part === undefined
      ? track.modules
      : track.modules.filter((lesson) => lesson.part === part);
  const seen = new Set<string>();
  return modules.flatMap((lesson) => {
    const item = lessonCase(track, lesson);
    if (!item || seen.has(item.id)) return [];
    seen.add(item.id);
    return [{ caseStudy: item, lessonId: lesson.id }];
  });
}

export function caseNotebookPrompt(lesson: Lesson, item: CaseStudy) {
  return [
    `Real-world case: ${item.title}`,
    `Module ${lesson.id}: ${lesson.title}`,
    `${item.setting} · ${item.period}`,
    `Context: ${item.context}`,
    item.boundary,
    `Task: ${lesson.realWorld.task}`,
    `References:\n${item.references.map((ref) => `${ref.title}\n${ref.url}\nSupports: ${ref.scope}`).join("\n\n")}`,
    "My calculation or implementation:\n",
    "Evidence, assumptions, and limitations:\n",
    "My conclusion and next check:\n",
  ].join("\n\n");
}
