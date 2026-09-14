import type { WorkspaceState } from "@/features/workspace/model/types";
export const emptyWorkspace = (): WorkspaceState => ({
  completed: [],
  lastLesson: "0.1",
  drafts: {},
  notes: [],
  experiments: [],
  submissions: {},
  examDrafts: {},
  examAttempts: {},
  runs: 0,
});
export function normalize(raw: Partial<WorkspaceState> | null): WorkspaceState {
  const base = emptyWorkspace();
  if (!raw || typeof raw !== "object") return base;
  return {
    completed: Array.isArray(raw.completed)
      ? raw.completed.filter((x) => typeof x === "string")
      : [],
    lastLesson: typeof raw.lastLesson === "string" ? raw.lastLesson : "0.1",
    drafts: raw.drafts && typeof raw.drafts === "object" ? raw.drafts : {},
    notes: Array.isArray(raw.notes) ? raw.notes : [],
    experiments: Array.isArray(raw.experiments) ? raw.experiments : [],
    submissions:
      raw.submissions && typeof raw.submissions === "object"
        ? raw.submissions
        : {},
    runs: typeof raw.runs === "number" ? raw.runs : 0,
    examDrafts:
      raw.examDrafts &&
      typeof raw.examDrafts === "object" &&
      !Array.isArray(raw.examDrafts)
        ? raw.examDrafts
        : {},
    examAttempts:
      raw.examAttempts &&
      typeof raw.examAttempts === "object" &&
      !Array.isArray(raw.examAttempts)
        ? Object.fromEntries(
            Object.entries(raw.examAttempts).filter(([, attempts]) =>
              Array.isArray(attempts),
            ),
          )
        : {},
  };
}
