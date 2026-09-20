import type { Track } from "@/features/learning/model/types";
import type { Certificate } from "./types";

export function matchesCourse(certificate: Certificate, track: Track) {
  return (
    certificate.trackId === track.id &&
    certificate.lessonIds.length === track.modules.length &&
    track.modules.every((lesson) =>
      certificate.lessonIds.includes(lesson.id),
    ) &&
    Object.keys(certificate.examVersions).length === track.exams.length &&
    track.exams.every(
      (exam) => certificate.examVersions[exam.id] === exam.version,
    )
  );
}

export const certificateDate = (issuedAt: string) =>
  new Intl.DateTimeFormat("en-GB", {
    day: "numeric",
    month: "long",
    year: "numeric",
    timeZone: "UTC",
  }).format(new Date(issuedAt));
export const verificationPath = (id: string) =>
  `/verify/${encodeURIComponent(id)}`;
