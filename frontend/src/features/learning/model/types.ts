import type { Exam } from "@/features/assessments/model/types";
export type Exercise = {
  question: string;
  options: string[];
  answer: number;
  explanation: string;
};

export type CaseStudy = {
  id: string;
  title: string;
  kind: "documented" | "implementation" | "illustrative";
  setting: string;
  period: string;
  context: string;
  boundary: string;
  references: { title: string; url: string; scope: string }[];
};

export type RealWorldApplication = {
  caseId: string;
  connection: string;
  task: string;
  walkthrough: string;
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
  realWorld: RealWorldApplication;
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
  caseStudies: CaseStudy[];
  outcomes?: string[];
  prerequisites?: string;
  readingGuide?: string;
  studyType?: string;
  resources?: { title: string; url: string }[];
  references?: { title: string; url: string }[];
  parts?: { id: string; title: string; description: string }[];
  exams: Exam[];
};
