import data from "../data/curriculum.json";
import type { Track } from "./types";
export const tracks: Track[] = data;
export const lessons = tracks.flatMap((t) => t.modules);
export function findLesson(id: string) {
  return lessons.find((l) => l.id === id);
}
export function lessonTrack(id: string) {
  return tracks.find((t) => t.modules.some((l) => l.id === id));
}
