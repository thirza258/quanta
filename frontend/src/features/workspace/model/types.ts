import type {
  ExamAttempt,
  ExamDraft,
} from "@/features/assessments/model/types";
import type { Note } from "@/features/notebook/model/types";
import type { Experiment } from "@/features/research/model/types";

export type WorkspaceState = {
  completed: string[];
  lastLesson: string;
  drafts: Record<string, string>;
  notes: Note[];
  experiments: Experiment[];
  submissions: Record<string, { answer: number; correct: boolean }>;
  examDrafts: Record<string, ExamDraft>;
  examAttempts: Record<string, ExamAttempt[]>;
  runs: number;
};

export type User = { id: string; name: string; email: string };
