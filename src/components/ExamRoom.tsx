import { useEffect, useRef, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  ClipboardCheck,
  RotateCcw,
} from "lucide-react";
import { api, ApiError, post } from "../lib/api";
import {
  examTrack,
  findExam,
  findLesson,
  trackLabel,
  tracks,
} from "../lib/catalog";
import {
  gradeExam,
  mergeExamHistory,
  retainAttempts,
  trackProgress,
} from "../lib/learning";
import type { Exam, ExamAttempt } from "../lib/types";
import { useWorkspace } from "../lib/workspace";

export default function ExamRoom() {
  const { examId } = useParams();
  const { user } = useWorkspace();
  const exam = findExam(examId ?? "");
  return exam ? (
    <Assessment key={`${user?.id ?? "guest"}:${exam.id}`} exam={exam} />
  ) : (
    <div className="page">
      <h1>Exam not found</h1>
      <Link className="button secondary" to="/curriculum">
        Browse the curriculum
      </Link>
    </div>
  );
}

function Assessment({ exam }: { exam: Exam }) {
  const { state, update, online, user } = useWorkspace();
  const track = examTrack(exam.id)!;
  const storedDraft = state.examDrafts[exam.id];
  const draft = storedDraft?.version === exam.version ? storedDraft : undefined;
  const attempts = (state.examAttempts[exam.id] ?? []).filter(
    (attempt) => attempt.version === exam.version,
  );
  const recordedAttempt = draft
    ? attempts.find((attempt) => attempt.id === draft.id)
    : undefined;
  const [index, setIndex] = useState(0);
  const [review, setReview] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [historyError, setHistoryError] = useState("");
  const [historyRetry, setHistoryRetry] = useState(0);
  const [selectedAttempt, setSelectedAttempt] = useState<string>();
  const submitting = useRef(false);
  const mounted = useRef(true);
  const heading = useRef<HTMLHeadingElement>(null);
  const result = !draft
    ? (attempts.find((attempt) => attempt.id === selectedAttempt) ??
      attempts[0])
    : undefined;
  const answered = draft
    ? exam.questions.filter((q) => draft.answers[q.id] !== undefined).length
    : 0;
  const required = Math.ceil((exam.questions.length * exam.passingScore) / 100);
  const nextExam =
    track.exams[track.exams.findIndex((item) => item.id === exam.id) + 1];
  const afterCheckpoint =
    track.modules[
      track.modules.findIndex((lesson) => lesson.id === exam.moduleIds.at(-1)) +
        1
    ];
  const nextTrack =
    tracks[tracks.findIndex((item) => item.id === track.id) + 1];
  const progress = trackProgress(track, state);

  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);

  useEffect(() => {
    if (!user || !online) return;
    let active = true;
    setHistoryError("");
    api<{ attempts: ExamAttempt[] }>(`/exams/${exam.id}/attempts`)
      .then(({ attempts: remote }) => {
        if (!active || !remote.length) return;
        update((current) => mergeExamHistory(current, exam, remote));
      })
      .catch((err: Error) => {
        if (active) setHistoryError(err.message);
      });
    return () => {
      active = false;
    };
  }, [exam.id, exam.version, online, user?.id, update, historyRetry]);

  function start() {
    update((current) => ({
      ...current,
      examDrafts: {
        ...current.examDrafts,
        [exam.id]: {
          id: crypto.randomUUID(),
          version: exam.version,
          startedAt: new Date().toISOString(),
          answers: {},
        },
      },
    }));
    setIndex(0);
    setReview(false);
    setError("");
  }
  function move(nextIndex: number) {
    setIndex(nextIndex);
    setReview(false);
    setError("");
    requestAnimationFrame(() => heading.current?.focus());
  }
  async function submit() {
    if (!draft || recordedAttempt || submitting.current) return;
    submitting.current = true;
    setBusy(true);
    setError("");
    try {
      const local = gradeExam(exam, draft);
      const attempt = online
        ? await post<ExamAttempt>(`/exams/${exam.id}/submit`, draft)
        : local;
      if (!mounted.current) return;
      update((current) => {
        if (current.examDrafts[exam.id]?.id !== draft.id) return current;
        const examDrafts = { ...current.examDrafts };
        if (examDrafts[exam.id]?.id === draft.id) delete examDrafts[exam.id];
        return {
          ...current,
          examDrafts,
          examAttempts: {
            ...current.examAttempts,
            [exam.id]: retainAttempts(
              current.examAttempts[exam.id] ?? [],
              attempt,
            ),
          },
        };
      });
      setSelectedAttempt(attempt.id);
      requestAnimationFrame(() => heading.current?.focus());
    } catch (err) {
      if (!mounted.current) return;
      setError((err as Error).message);
      if (user && err instanceof ApiError && err.status === 409)
        setHistoryRetry((value) => value + 1);
    } finally {
      submitting.current = false;
      setBusy(false);
    }
  }

  return (
    <div className="page exam-page">
      <Link className="text-link back-link" to={`/curriculum/${track.id}`}>
        <ArrowLeft size={15} />
        Back to {track.title}
      </Link>
      <div className="page-eyebrow">
        {trackLabel(track)}
        <span className="level-badge">
          {exam.kind === "checkpoint" ? "Checkpoint" : "Final exam"}
        </span>
      </div>
      <h1>{exam.title}</h1>
      <p className="page-subtitle">{exam.description}</p>
      <div className="exam-meta">
        <span>{exam.questions.length} questions</span>
        <span>
          {required} correct to pass ({exam.passingScore}%)
        </span>
        <span>About {exam.minutes} minutes · no timer</span>
      </div>
      {historyError ? (
        <p className="inline-notice" role="status">
          Account history could not load: {historyError}{" "}
          <button
            className="text-link"
            onClick={() => setHistoryRetry((value) => value + 1)}
          >
            Retry history
          </button>
        </p>
      ) : null}
      {storedDraft && !draft ? (
        <p className="inline-notice">
          The exam has been updated. Start a new attempt to use the current
          questions.
        </p>
      ) : null}

      {draft && recordedAttempt ? (
        <section className="tool-card" aria-label="Recovered exam submission">
          <h2>This attempt was already submitted.</h2>
          <p>
            Your account has the submitted result. Your current answers include
            later edits, which are still saved. Keep them in a new attempt, or
            discard the edits to review the submitted answers.
          </p>
          <div className="exam-actions">
            <button
              className="button primary"
              disabled={busy}
              onClick={() => {
                update((current) => {
                  const active = current.examDrafts[exam.id];
                  if (active?.id !== draft.id) return current;
                  return {
                    ...current,
                    examDrafts: {
                      ...current.examDrafts,
                      [exam.id]: {
                        ...active,
                        id: crypto.randomUUID(),
                        startedAt: new Date().toISOString(),
                      },
                    },
                  };
                });
                move(0);
              }}
            >
              Continue as a new attempt
              <ArrowRight size={16} />
            </button>
            <button
              className="button secondary"
              disabled={busy}
              onClick={() => {
                update((current) => {
                  if (current.examDrafts[exam.id]?.id !== draft.id)
                    return current;
                  const examDrafts = { ...current.examDrafts };
                  delete examDrafts[exam.id];
                  return { ...current, examDrafts };
                });
                setSelectedAttempt(recordedAttempt.id);
                setError("");
                requestAnimationFrame(() => heading.current?.focus());
              }}
            >
              Review submitted attempt
            </button>
          </div>
        </section>
      ) : null}

      {!draft && !result ? (
        <section className="exam-intro tool-card">
          <ClipboardCheck size={28} />
          <h2>Put your understanding to work.</h2>
          <p>
            Each question has one best answer. Your answers save as you go, so
            you can leave and resume later. Submit the complete exam to see your
            score, explanations, and topics to revisit.
          </p>
          <h3>Before you begin</h3>
          <ul className="exam-reading-list">
            {exam.moduleIds.map((id) => (
              <li key={id}>
                <Link to={`/learn/${id}`}>{findLesson(id)?.title}</Link>
                {state.completed.includes(id) ? (
                  <span>
                    <Check size={14} />
                    Completed
                  </span>
                ) : (
                  <span>Available to review</span>
                )}
              </li>
            ))}
          </ul>
          <p className="fine-print">
            You can take this as a readiness check at any time. Course
            completion requires the lesson practice and all course exams. You
            can revisit any course at any time.
          </p>
          <button className="button primary" onClick={start}>
            Start exam
            <ArrowRight size={16} />
          </button>
        </section>
      ) : null}

      {draft ? (
        <div className="exam-layout">
          <aside className="exam-navigation" aria-label="Exam navigation">
            <strong>
              {answered} of {exam.questions.length} answered
            </strong>
            <div
              className="progress-track"
              role="progressbar"
              aria-label="Questions answered"
              aria-valuemin={0}
              aria-valuemax={exam.questions.length}
              aria-valuenow={answered}
            >
              <span
                style={{
                  width: `${(answered / exam.questions.length) * 100}%`,
                }}
              />
            </div>
            <div className="question-grid">
              {exam.questions.map((q, i) => (
                <button
                  key={q.id}
                  disabled={busy}
                  className={`${draft.answers[q.id] !== undefined ? "answered" : ""} ${index === i && !review ? "current" : ""}`}
                  aria-label={`Question ${i + 1}${draft.answers[q.id] !== undefined ? ", answered" : ", unanswered"}`}
                  aria-current={index === i && !review ? "step" : undefined}
                  onClick={() => move(i)}
                >
                  {i + 1}
                </button>
              ))}
            </div>
            <p className="fine-print">
              Answers save automatically. You can change them before submission.
            </p>
            <button
              className="button secondary small"
              disabled={busy}
              onClick={() => {
                setReview(true);
                requestAnimationFrame(() => heading.current?.focus());
              }}
            >
              Review answers
            </button>
          </aside>
          <section className="exam-question-panel">
            {review ? (
              <>
                <h2 ref={heading} tabIndex={-1}>
                  Review your answers
                </h2>
                <p>
                  {answered === exam.questions.length
                    ? "All questions are answered. Submit when you are ready."
                    : `${exam.questions.length - answered} questions still need an answer.`}
                </p>
                <ol className="exam-answer-summary">
                  {exam.questions.map((q, i) => (
                    <li key={q.id}>
                      <div>
                        <strong>{q.question}</strong>
                        <p>
                          {q.options[draft.answers[q.id]] ?? "Not answered"}
                        </p>
                      </div>
                      <button
                        className="text-link"
                        disabled={busy}
                        aria-label={`Edit question ${i + 1}`}
                        onClick={() => move(i)}
                      >
                        Edit
                      </button>
                    </li>
                  ))}
                </ol>
                <button
                  className="button primary"
                  disabled={
                    answered !== exam.questions.length ||
                    busy ||
                    !!recordedAttempt
                  }
                  onClick={() => void submit()}
                >
                  {busy ? "Submitting…" : "Submit exam"}
                  <ClipboardCheck size={16} />
                </button>
                {!online ? (
                  <p className="fine-print">
                    Online grading is unavailable. This attempt will be graded
                    and saved on this device.
                  </p>
                ) : null}
              </>
            ) : (
              <>
                <div className="eyebrow">
                  QUESTION {index + 1} OF {exam.questions.length}
                </div>
                <h2 ref={heading} tabIndex={-1} id="exam-question">
                  {exam.questions[index].question}
                </h2>
                <fieldset
                  className="exam-options"
                  aria-labelledby="exam-question"
                  disabled={busy}
                >
                  <legend className="sr-only">Choose one answer</legend>
                  {exam.questions[index].options.map((option, answer) => (
                    <label
                      key={option}
                      className={`answer-option ${draft.answers[exam.questions[index].id] === answer ? "selected" : ""}`}
                    >
                      <input
                        type="radio"
                        name={exam.questions[index].id}
                        checked={
                          draft.answers[exam.questions[index].id] === answer
                        }
                        onChange={() =>
                          update((current) => {
                            const active = current.examDrafts[exam.id];
                            if (!active || active.id !== draft.id)
                              return current;
                            return {
                              ...current,
                              examDrafts: {
                                ...current.examDrafts,
                                [exam.id]: {
                                  ...active,
                                  answers: {
                                    ...active.answers,
                                    [exam.questions[index].id]: answer,
                                  },
                                },
                              },
                            };
                          })
                        }
                      />
                      <span className="answer-letter">
                        {String.fromCharCode(65 + answer)}
                      </span>
                      {option}
                    </label>
                  ))}
                </fieldset>
                <div className="exam-actions">
                  <button
                    className="button secondary"
                    disabled={index === 0 || busy}
                    onClick={() => move(index - 1)}
                  >
                    <ArrowLeft size={15} />
                    Previous
                  </button>
                  <button
                    className="button primary"
                    disabled={busy}
                    onClick={() =>
                      index === exam.questions.length - 1
                        ? (setReview(true),
                          requestAnimationFrame(() => heading.current?.focus()))
                        : move(index + 1)
                    }
                  >
                    {index === exam.questions.length - 1
                      ? "Review answers"
                      : "Next question"}
                    <ArrowRight size={15} />
                  </button>
                </div>
              </>
            )}
            {error ? (
              <p className="error-message" role="alert">
                {error} Your answers are saved. You can retry submission.
              </p>
            ) : null}
          </section>
        </div>
      ) : null}

      {result ? (
        <>
          <section
            className={`exam-result ${result.passed ? "passed" : ""}`}
            aria-label="Exam result"
          >
            <div className="exam-score">
              <strong>{result.score}%</strong>
              <span>
                {result.correctCount} of {result.total} correct
              </span>
            </div>
            <div>
              <div className="eyebrow">
                {result.passed
                  ? "ASSESSMENT PASSED"
                  : "KEEP BUILDING YOUR UNDERSTANDING"}
              </div>
              <h2 ref={heading} tabIndex={-1}>
                {result.passed
                  ? "You passed this exam."
                  : "Review, then try again."}
              </h2>
              <p>
                {result.passed
                  ? progress.complete
                    ? "All lessons and exams in this course are complete."
                    : "Your exam pass is saved. Complete the remaining lesson practice and assessments to finish the course."
                  : `You need ${required} correct answers to pass. Use the explanations below to revisit the concepts you missed.`}
              </p>
              <div className="exam-actions">
                <button className="button secondary" onClick={start}>
                  <RotateCcw size={15} />
                  Retake exam
                </button>
                {result.passed && afterCheckpoint ? (
                  <Link
                    className="button primary"
                    to={`/learn/${afterCheckpoint.id}`}
                  >
                    Continue to {afterCheckpoint.title}
                    <ArrowRight size={15} />
                  </Link>
                ) : result.passed && progress.complete && nextTrack ? (
                  <Link
                    className="button primary"
                    to={`/curriculum/${nextTrack.id}`}
                  >
                    Next course
                    <ArrowRight size={15} />
                  </Link>
                ) : (
                  <Link
                    className="button primary"
                    to={`/curriculum/${track.id}`}
                  >
                    Return to course
                    <ArrowRight size={15} />
                  </Link>
                )}
              </div>
              <p className="fine-print">
                Submitted {new Date(result.submittedAt).toLocaleString()} ·{" "}
                {result.grading === "server"
                  ? "Graded online"
                  : "Graded on this device"}
              </p>
            </div>
          </section>
          {!result.passed ? (
            <section className="exam-revisit">
              <h2>Topics to revisit</h2>
              <div>
                {[
                  ...new Set(
                    exam.questions
                      .filter((q) => result.answers[q.id] !== q.answer)
                      .map((q) => q.lessonId),
                  ),
                ].map((id) => (
                  <Link
                    className="button secondary small"
                    key={id}
                    to={`/learn/${id}`}
                  >
                    <BookOpen size={14} />
                    {findLesson(id)?.title}
                  </Link>
                ))}
              </div>
            </section>
          ) : null}
          <section aria-label="Answer explanations">
            <div className="section-heading">
              <div>
                <h2>Answer review</h2>
                <p>Understand the reasoning behind every answer.</p>
              </div>
            </div>
            {exam.questions.map((q, i) => (
              <article className="exam-review-card" key={q.id}>
                <span
                  className={`review-outcome ${result.answers[q.id] === q.answer ? "correct" : "incorrect"}`}
                >
                  Question {i + 1} ·{" "}
                  {result.answers[q.id] === q.answer ? "Correct" : "Incorrect"}
                </span>
                <h3>{q.question}</h3>
                <p>
                  Your answer:{" "}
                  <strong>
                    {q.options[result.answers[q.id]] ?? "No answer"}
                  </strong>
                </p>
                {result.answers[q.id] !== q.answer ? (
                  <p>
                    Correct answer: <strong>{q.options[q.answer]}</strong>
                  </p>
                ) : null}
                <p>{q.explanation}</p>
                <Link className="text-link" to={`/learn/${q.lessonId}`}>
                  Review {findLesson(q.lessonId)?.title}
                  <ArrowRight size={14} />
                </Link>
              </article>
            ))}
          </section>
          {nextExam && result.passed ? (
            <Link className="text-link" to={`/exams/${nextExam.id}`}>
              {nextExam.kind === "final"
                ? "Explore the final exam"
                : "Explore the next checkpoint"}
              <ArrowRight size={15} />
            </Link>
          ) : null}
        </>
      ) : null}

      {attempts.length ? (
        <section className="exam-history" aria-label="Attempt history">
          <h2>Attempt history</h2>
          <p className="fine-print">
            Recent attempts and your best result stay in your workspace. A
            retake does not remove a previous pass.
          </p>
          <div className="table-scroll">
            <table>
              <thead>
                <tr>
                  <th>Submitted</th>
                  <th>Score</th>
                  <th>Result</th>
                  <th>Review</th>
                </tr>
              </thead>
              <tbody>
                {attempts.map((attempt) => (
                  <tr key={attempt.id}>
                    <td>{new Date(attempt.submittedAt).toLocaleString()}</td>
                    <td>{attempt.score}%</td>
                    <td>{attempt.passed ? "Passed" : "Not yet passed"}</td>
                    <td>
                      <button
                        className="text-link"
                        disabled={!!draft}
                        onClick={() => {
                          setSelectedAttempt(attempt.id);
                          window.scrollTo({ top: 0, behavior: "smooth" });
                        }}
                      >
                        View attempt
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          {draft ? (
            <p className="fine-print">
              Finish your current attempt to review previous answers.
            </p>
          ) : null}
        </section>
      ) : null}
    </div>
  );
}
