import type { Exam } from "@/features/assessments/model/types";
export type Exercise = {
  question: string;
  options: string[];
  answer: number;
  explanation: string;
};

export type Lesson = {
  id: string;
  title: string;
  subtitle: string;
  minutes: number;
  content: string;
  formula: string;
  exercise: Exercise;
  code: string;
  codeLanguage?: "python" | "c";
  expectedOutput?: string;
  kind: string;
  objective?: string;
  exercises?: Exercise[];
  terms?: { term: string; definition: string }[];
  part?: string;
  reading?: string;
  references?: { title: string; url: string }[];
  assignment?: { prompt: string; solution: string };
};

export type Track = {
  id: string;
  number: number;
  title: string;
  description: string;
  source: string;
  level: string;
  icon: string;
  modules: Lesson[];
  outcomes?: string[];
  prerequisites?: string;
  readingGuide?: string;
  studyType?: string;
  resources?: { title: string; url: string }[];
  references?: { title: string; url: string }[];
  parts?: { id: string; title: string; description: string }[];
  exams: Exam[];
};
