import { describe, expect, it } from "vitest";
import { tracks } from "@/features/learning/model/catalog";
import { certificateDate, matchesCourse } from "./certificates";

describe("issued certificate course editions", () => {
  it("retains historical requirements when modules or exam versions change", () => {
    const track = tracks[0];
    const certificate = {
      id: "QTA-example",
      trackId: track.id,
      recipientName: "Ayu",
      courseTitle: track.title,
      issuedAt: "2026-09-20T23:59:00Z",
      studyMinutes: 96,
      lessonIds: track.modules.map((lesson) => lesson.id),
      examVersions: Object.fromEntries(
        track.exams.map((exam) => [exam.id, exam.version]),
      ),
    };
    expect(matchesCourse(certificate, track)).toBe(true);
    expect(
      matchesCourse(certificate, {
        ...track,
        modules: [...track.modules].reverse(),
      }),
    ).toBe(true);
    expect(
      matchesCourse(certificate, { ...track, modules: track.modules.slice(1) }),
    ).toBe(false);
    expect(
      matchesCourse(certificate, {
        ...track,
        exams: track.exams.map((exam) => ({
          ...exam,
          version: exam.version + 1,
        })),
      }),
    ).toBe(false);
  });
  it("shows the original issue date regardless of viewer timezone", () => {
    expect(certificateDate("2026-09-20T23:59:00Z")).toBe("20 September 2026");
  });
});
