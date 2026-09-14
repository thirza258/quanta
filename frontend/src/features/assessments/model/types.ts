import type { Exercise } from "@/features/learning/model/types";

export type ExamQuestion = Exercise & { id: string; lessonId: string };

export type Exam = {
  id: string;
  title: string;
  kind: string;
  version: number;
  description: string;
  minutes: number;
  passingScore: number;
  moduleIds: string[];
  questions: ExamQuestion[];
};

export type ExamDraft = {
  id: string;
  version: number;
  startedAt: string;
  answers: Record<string, number>;
};

export type ExamAttempt = ExamDraft & {
  examId: string;
  submittedAt: string;
  correctCount: number;
  total: number;
  score: number;
  passed: boolean;
  grading: "server" | "device";
};
