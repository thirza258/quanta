import type { Exam, ExamDraft } from "@/features/assessments/model/types";
import { findLesson, tracks } from "@/features/learning/model/catalog";
import {
  examPassed,
  exerciseKey,
  gradeExam,
  mergeExamHistory,
  practiceComplete,
  retainAttempts,
  trackProgress,
} from "@/features/learning/model/progress";
import { emptyWorkspace, normalize } from "@/features/workspace/model/state";
import { describe, expect, it } from "vitest";

const foundation = tracks[0];
const final = foundation.exams[1];
function draft(exam: Exam, correct = exam.questions.length): ExamDraft {
  return {
    id: crypto.randomUUID(),
    version: exam.version,
    startedAt: "2026-09-14T01:00:00Z",
    answers: Object.fromEntries(
      exam.questions.map((q, i) => [
        q.id,
        i < correct ? q.answer : (q.answer + 1) % q.options.length,
      ]),
    ),
  };
}

describe("learning progression", () => {
  it("retains a version-2 bot pass as history without satisfying the expanded final", () => {
    const current = tracks
      .find((track) => track.id === "stock-bots")!
      .exams.at(-1)!;
    const previous: Exam = {
      ...current,
      version: 2,
      questions: current.questions.filter(
        (question) => Number(question.lessonId.split(".")[1]) <= 32,
      ),
      moduleIds: current.moduleIds.filter(
        (id) => Number(id.split(".")[1]) <= 32,
      ),
    };
    const state = emptyWorkspace();
    const attempt = gradeExam(previous, draft(previous));
    state.examAttempts[current.id] = [attempt];
    expect(attempt.passed).toBe(true);
    expect(examPassed(current, state)).toBe(false);
    expect(normalize(state).examAttempts[current.id][0]).toEqual(attempt);
  });
  it("migrates old workspaces without changing existing progress, code, or answers", () => {
    const previous = {
      completed: ["1.1"],
      lastLesson: "3.2",
      drafts: { "1.1": "my research" },
      submissions: { "1.1": { answer: 1, correct: true } },
    };
    expect(normalize(previous)).toMatchObject({
      ...previous,
      examDrafts: {},
      examAttempts: {},
    });
    expect(normalize(null).lastLesson).toBe("0.1");
    expect(practiceComplete(findLesson("1.1")!, normalize(previous))).toBe(
      false,
    );
    // The original completion is preserved, while the added practice remains unanswered.
    const expanded = normalize(previous);
    expanded.submissions["1.1:q2"] = { answer: 1, correct: true };
    expect(practiceComplete(findLesson("1.1")!, expanded)).toBe(true);
  });
  it("requires all beginner practice answers before lesson completion", () => {
    const state = emptyWorkspace();
    const lesson = foundation.modules[0];
    state.submissions[lesson.id] = { answer: 1, correct: true };
    expect(practiceComplete(lesson, state)).toBe(false);
    lesson.exercises!.forEach((q, i) => {
      state.submissions[exerciseKey(lesson.id, i)] = {
        answer: q.answer,
        correct: true,
      };
    });
    expect(practiceComplete(lesson, state)).toBe(true);
  });
  it("requires both modules and assessments and retains a pass after a failed retake", () => {
    const state = emptyWorkspace();
    state.completed = foundation.modules.map((lesson) => lesson.id);
    expect(trackProgress(foundation, state)).toMatchObject({
      complete: false,
      percent: 80,
    });
    for (const exam of foundation.exams)
      state.examAttempts[exam.id] = [gradeExam(exam, draft(exam))];
    expect(trackProgress(foundation, state)).toMatchObject({
      complete: true,
      percent: 100,
    });
    state.examAttempts[final.id].unshift(gradeExam(final, draft(final, 0)));
    expect(examPassed(final, state)).toBe(true);
    expect(examPassed({ ...final, version: 2 }, state)).toBe(false);
  });
});

describe("assessment grading and persistence", () => {
  it("uses exact thresholds for a 16-question exam", () => {
    expect(gradeExam(final, draft(final, 12))).toMatchObject({
      correctCount: 12,
      score: 75,
      passed: false,
    });
    expect(gradeExam(final, draft(final, 13))).toMatchObject({
      correctCount: 13,
      score: 81.25,
      passed: true,
    });
    const checkpoint = foundation.exams[0];
    expect(gradeExam(checkpoint, draft(checkpoint, 6))).toMatchObject({
      score: 75,
      passed: true,
    });
  });
  it("rejects unanswered, unknown, invalid, fractional, and stale-version answers", () => {
    const missing = draft(final);
    delete missing.answers[final.questions[0].id];
    expect(() => gradeExam(final, missing)).toThrow("every question");
    expect(() => gradeExam(final, { ...draft(final), version: 99 })).toThrow(
      "changed",
    );
    expect(() =>
      gradeExam(final, {
        ...draft(final),
        answers: { ...draft(final).answers, unknown: 0 },
      }),
    ).toThrow();
    for (const answer of [-1, 99, 0.5, NaN]) {
      const invalid = draft(final);
      invalid.answers[final.questions[0].id] = answer;
      expect(() => gradeExam(final, invalid)).toThrow();
    }
  });
  it("deduplicates retries and keeps the best result beyond twenty attempts", () => {
    const best = {
      ...gradeExam(final, draft(final)),
      submittedAt: "2026-08-01T00:00:00Z",
    };
    let attempts = [best];
    for (let i = 1; i <= 25; i++)
      attempts = retainAttempts(attempts, {
        ...gradeExam(final, draft(final, 0)),
        submittedAt: `2026-09-${String(i).padStart(2, "0")}T00:00:00Z`,
      });
    expect(attempts).toHaveLength(20);
    expect(attempts).toContainEqual(best);
    expect(retainAttempts(attempts, attempts[0])).toHaveLength(20);
  });
  it("retains a current-version pass when an older exam version had a higher score", () => {
    const oldBest = {
      ...gradeExam(final, draft(final)),
      submittedAt: "2026-07-01T00:00:00Z",
    };
    const updated = { ...final, version: 2 };
    const currentPass = {
      ...gradeExam(updated, draft(updated, 13)),
      submittedAt: "2026-08-01T00:00:00Z",
    };
    let attempts = [currentPass, oldBest];
    for (let i = 1; i <= 25; i++)
      attempts = retainAttempts(attempts, {
        ...gradeExam(updated, draft(updated, 0)),
        submittedAt: `2026-09-${String(i).padStart(2, "0")}T00:00:00Z`,
      });
    expect(attempts).toContainEqual(currentPass);
  });
  it("restores a recorded submission whose response was lost and retires its matching draft", () => {
    const state = emptyWorkspace();
    const pending = draft(final);
    const submitted = gradeExam(final, pending);
    state.examDrafts[final.id] = pending;
    // Recovery also works when the result was already merged into the workspace.
    state.examAttempts[final.id] = [submitted];
    const recovered = mergeExamHistory(state, final, [submitted]);
    expect(recovered.examDrafts[final.id]).toBeUndefined();
    expect(recovered.examAttempts[final.id]).toEqual([submitted]);
    expect(state.examDrafts[final.id]).toBe(pending);
    expect(mergeExamHistory(recovered, final, [submitted])).toBe(recovered);
  });
  it("preserves answers edited after submission and drafts belonging to a later retake", () => {
    const state = emptyWorkspace();
    const pending = draft(final);
    const submitted = gradeExam(final, pending);
    const edited = {
      ...pending,
      answers: {
        ...pending.answers,
        [final.questions[0].id]:
          (final.questions[0].answer + 1) % final.questions[0].options.length,
      },
    };
    state.examDrafts[final.id] = edited;
    const recovered = mergeExamHistory(state, final, [submitted]);
    expect(recovered.examDrafts[final.id]).toBe(edited);
    expect(recovered.examAttempts[final.id]).toEqual([submitted]);
    const retake = draft(final);
    recovered.examDrafts[final.id] = retake;
    expect(
      mergeExamHistory(recovered, final, [submitted]).examDrafts[final.id],
    ).toBe(retake);
  });
  it("ignores account history for other exam versions without rewriting the workspace", () => {
    const state = emptyWorkspace();
    state.examDrafts[final.id] = draft(final);
    const otherVersion = { ...final, version: final.version + 1 };
    const otherAttempt = gradeExam(otherVersion, draft(otherVersion));
    expect(mergeExamHistory(state, final, [otherAttempt])).toBe(state);
    expect(mergeExamHistory(state, final, [])).toBe(state);
  });
});
