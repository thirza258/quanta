import {
  exerciseKey,
  lessonExercises,
} from "@/features/learning/model/progress";
import type { Exercise, Lesson } from "@/features/learning/model/types";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { post } from "@/shared/api/client";
import { ArrowRight, CheckCircle2 } from "lucide-react";
import { useEffect, useRef, useState } from "react";

export default function PracticeQuestions({ lesson }: { lesson: Lesson }) {
  const questions = lessonExercises(lesson);
  return (
    <section aria-label="Practice questions">
      {questions.map((exercise, index) => (
        <PracticeQuestion
          key={exerciseKey(lesson.id, index)}
          exercise={exercise}
          lessonId={lesson.id}
          index={index}
          total={questions.length}
        />
      ))}
    </section>
  );
}

function PracticeQuestion({
  exercise,
  lessonId,
  index,
  total,
}: {
  exercise: Exercise;
  lessonId: string;
  index: number;
  total: number;
}) {
  const { state, update, online } = useWorkspace();
  const key = exerciseKey(lessonId, index);
  const saved = state.submissions[key];
  const [answer, setAnswer] = useState<number | null>(saved?.answer ?? null);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");
  const mounted = useRef(true);
  useEffect(() => {
    mounted.current = true;
    return () => {
      mounted.current = false;
    };
  }, []);
  const feedback = saved?.answer === answer ? saved : null;
  async function submit() {
    if (answer === null || submitting) return;
    setSubmitting(true);
    setError("");
    try {
      const result = online
        ? await post<{ correct: boolean }>(`/exercises/${lessonId}/submit`, {
            answer,
            question: index,
          })
        : { correct: answer === exercise.answer };
      if (!mounted.current) return;
      update((current) => ({
        ...current,
        submissions: {
          ...current.submissions,
          [key]: { answer, correct: result.correct },
        },
      }));
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSubmitting(false);
    }
  }
  return (
    <div className="exercise-card">
      <div className="eyebrow">
        <CheckCircle2 size={15} />
        {total > 1
          ? `PRACTICE ${index + 1} OF ${total}`
          : "CHECK YOUR UNDERSTANDING"}
      </div>
      <h3 id={`prompt-${key}`}>{exercise.question}</h3>
      <fieldset disabled={submitting} aria-labelledby={`prompt-${key}`}>
        <legend className="sr-only">Choose your answer</legend>
        {exercise.options.map((option, i) => (
          <label
            key={option}
            className={`answer-option ${answer === i ? "selected" : ""}`}
          >
            <input
              type="radio"
              name={`answer-${key}`}
              checked={answer === i}
              onChange={() => {
                setAnswer(i);
                setError("");
              }}
            />
            <span className="answer-letter">{String.fromCharCode(65 + i)}</span>
            {option}
          </label>
        ))}
      </fieldset>
      <button
        className="button secondary small"
        disabled={answer === null || submitting}
        onClick={() => void submit()}
      >
        {submitting ? "Checking…" : "Check answer"}
        <ArrowRight size={14} />
      </button>
      {feedback ? (
        <div
          className={`quiz-feedback ${feedback.correct ? "correct" : "incorrect"}`}
          role="status"
        >
          <strong>
            {feedback.correct ? "That’s right." : "Take another look."}
          </strong>{" "}
          {exercise.explanation}
        </div>
      ) : null}
      {error ? (
        <p className="error-message" role="alert">
          {error}
        </p>
      ) : null}
    </div>
  );
}
