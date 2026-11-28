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

export type FunnelCta = {
  label: string;
  target_course_id?: string;
  target_url?: string;
  secondary_label?: string;
  secondary_target_course_id?: string;
  secondary_target_url?: string;
};

export type CourseCompletionCriteria = {
  lessons_pct: number;
  assessment_pass_pct: number;
};

export type CourseCertificateConfig = {
  enabled: boolean;
  template_id: string;
  verification_required: boolean;
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
  slug?: string;
  subtitle?: string;
  audience_tags?: string[];
  estimated_minutes?: number;
  estimated_hours?: number;
  lesson_count?: number;
  assessment_count?: number;
  completion_criteria?: CourseCompletionCriteria;
  certificate?: CourseCertificateConfig;
  funnel_cta?: FunnelCta;
  language?: string[];
  /** Canonical curriculum architecture metadata. IDs above remain stable. */
  stage?: string;
  stage_number?: number;
  stage_name?: string;
  sequence?: number;
  difficulty?: number;
  prerequisite_course_ids?: string[];
  prerequisite_any_of?: string[];
  recommended_course_ids?: string[];
  learning_outcomes?: string[];
  skills?: string[];
  focus_summary?: string;
  domain?: string;
  course_type?:
    | "core"
    | "foundation"
    | "specialization"
    | "workshop"
    | "capstone"
    | "reference"
    | "on-ramp";
  is_core?: boolean;
  is_specialization?: boolean;
  is_capstone?: boolean;
};
