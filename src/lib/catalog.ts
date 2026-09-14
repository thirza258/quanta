import data from "../data/curriculum.json";
import type { Track } from "./types";
export const tracks: Track[] = data;
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
    : `TRACK ${String(track.number).padStart(2, "0")}`;
}
export function findLesson(id: string) {
  return lessons.find((l) => l.id === id);
}
export function lessonTrack(id: string) {
  return tracks.find((t) => t.modules.some((l) => l.id === id));
}
