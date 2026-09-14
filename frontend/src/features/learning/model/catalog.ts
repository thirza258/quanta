import type { Lesson, Track } from "@/features/learning/model/types";
import data from "@content/catalog/curriculum.json";
function codeLanguage(value: unknown): Lesson["codeLanguage"] {
  if (value === undefined || value === "python" || value === "c") return value;
  throw new Error(`Unsupported course language: ${String(value)}`);
}
export const tracks: Track[] = data.map((track) => ({
  ...track,
  modules: track.modules.map((lesson) => ({
    ...lesson,
    codeLanguage: codeLanguage(
      "codeLanguage" in lesson ? lesson.codeLanguage : undefined,
    ),
  })),
}));
export const lessons = tracks.flatMap((t) => t.modules);
export const exams = tracks.flatMap((t) => t.exams);
export function findExam(id: string) {
  return exams.find((exam) => exam.id === id);
}
export function examTrack(id: string) {
  return tracks.find((track) => track.exams.some((exam) => exam.id === id));
}
export function trackLabel(track: Track) {
  return track.number === 0
    ? "START HERE"
    : `TRACK ${String(tracks.findIndex((item) => item.id === track.id)).padStart(2, "0")}`;
}
export function findLesson(id: string) {
  return lessons.find((l) => l.id === id);
}
export function lessonTrack(id: string) {
  return tracks.find((t) => t.modules.some((l) => l.id === id));
}
