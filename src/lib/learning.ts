import type {
  Exam,
  ExamAttempt,
  ExamDraft,
  Lesson,
  Track,
  WorkspaceState,
} from "./types";

export const lessonExercises = (lesson: Lesson) =>
  lesson.exercises ?? [lesson.exercise];
// The first question keeps the original key so existing progress survives.
export const exerciseKey = (lessonId: string, index: number) =>
  index === 0 ? lessonId : `${lessonId}:q${index + 1}`;
export const practiceComplete = (lesson: Lesson, state: WorkspaceState) =>
  lessonExercises(lesson).every(
    (_, index) => state.submissions[exerciseKey(lesson.id, index)]?.correct,
  );
export const examPassed = (exam: Exam, state: WorkspaceState) =>
  (state.examAttempts[exam.id] ?? []).some(
    (attempt) => attempt.version === exam.version && attempt.passed,
  );
export function trackProgress(track: Track, state: WorkspaceState) {
  const modules = track.modules.filter((lesson) =>
    state.completed.includes(lesson.id),
  ).length;
  const exams = track.exams.filter((exam) => examPassed(exam, state)).length;
  const total = track.modules.length + track.exams.length;
  return {
    modules,
    exams,
    total,
    percent: Math.round(((modules + exams) / total) * 100),
    complete: modules + exams === total,
  };
}
export function gradeExam(exam: Exam, draft: ExamDraft): ExamAttempt {
  if (draft.version !== exam.version)
    throw new Error("This exam has changed. Start a new attempt.");
  if (
    Object.keys(draft.answers).length !== exam.questions.length ||
    exam.questions.some((question) => {
      const answer = draft.answers[question.id];
      return (
        !Number.isInteger(answer) ||
        answer < 0 ||
        answer >= question.options.length
      );
    })
  )
    throw new Error("Answer every question before submitting the exam.");
  const correctCount = exam.questions.filter(
    (question) => draft.answers[question.id] === question.answer,
  ).length;
  return {
    ...draft,
    examId: exam.id,
    correctCount,
    total: exam.questions.length,
    score: Math.round((correctCount / exam.questions.length) * 10000) / 100,
    passed: correctCount * 100 >= exam.passingScore * exam.questions.length,
    submittedAt: new Date().toISOString(),
    grading: "device",
  };
}
export function retainAttempts(attempts: ExamAttempt[], next: ExamAttempt) {
  const sorted = [
    next,
    ...attempts.filter((attempt) => attempt.id !== next.id),
  ].sort((a, b) => b.submittedAt.localeCompare(a.submittedAt));
  if (sorted.length <= 20) return sorted;
  const best = sorted
    .filter((attempt) => attempt.version === next.version)
    .reduce((a, b) => (b.score > a.score ? b : a));
  const recent = sorted.slice(0, 19);
  return [
    ...recent,
    recent.some((attempt) => attempt.id === best.id) ? sorted[19] : best,
  ];
}

export function mergeExamHistory(
  state: WorkspaceState,
  exam: Exam,
  remote: ExamAttempt[],
): WorkspaceState {
  let attempts = state.examAttempts[exam.id] ?? [];
  for (const attempt of remote) {
    if (attempt.version === exam.version)
      attempts = retainAttempts(attempts, attempt);
  }
  const draft = state.examDrafts[exam.id];
  const submitted =
    draft &&
    attempts.find(
      (attempt) => attempt.id === draft.id && attempt.version === draft.version,
    );
  // A recorded submission can outlive a lost response. Only retire its draft
  // automatically when doing so will not discard answers edited afterward.
  const recovered =
    submitted &&
    draft &&
    Object.keys(draft.answers).length ===
      Object.keys(submitted.answers).length &&
    Object.entries(submitted.answers).every(
      ([id, answer]) => draft.answers[id] === answer,
    );
  if (
    !recovered &&
    JSON.stringify(attempts) ===
      JSON.stringify(state.examAttempts[exam.id] ?? [])
  )
    return state;
  const examDrafts = { ...state.examDrafts };
  if (recovered) delete examDrafts[exam.id];
  return {
    ...state,
    examDrafts,
    examAttempts: { ...state.examAttempts, [exam.id]: attempts },
  };
}
