import type { Exam } from "@/features/assessments/model/types";
import { examPassed } from "@/features/learning/model/progress";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { ArrowRight, ClipboardCheck } from "lucide-react";
import { Link } from "react-router-dom";

export default function ExamCard({ exam }: { exam: Exam }) {
  const { state } = useWorkspace();
  const attempts = (state.examAttempts[exam.id] ?? []).filter(
    (attempt) => attempt.version === exam.version,
  );
  const draft = state.examDrafts[exam.id];
  const inProgress = draft?.version === exam.version;
  const passed = examPassed(exam, state);
  const best = attempts.length
    ? Math.max(...attempts.map((attempt) => attempt.score))
    : null;
  return (
    <article className={`exam-card ${passed ? "passed" : ""}`}>
      <span className="exam-card-icon">
        <ClipboardCheck size={23} />
      </span>
      <div>
        <div className="eyebrow">
          {exam.kind === "checkpoint" ? "CHECKPOINT EXAM" : "FINAL EXAM"}
          {passed ? " · PASSED" : inProgress ? " · IN PROGRESS" : ""}
        </div>
        <h3>{exam.title}</h3>
        <p>
          {exam.questions.length} questions ·{" "}
          {Math.ceil((exam.questions.length * exam.passingScore) / 100)} correct
          to pass · Open-book
        </p>
        {best !== null ? (
          <span className="fine-print">
            Best score: {best}% · {attempts.length} saved{" "}
            {attempts.length === 1 ? "attempt" : "attempts"}
          </span>
        ) : null}
      </div>
      <Link className="button secondary small" to={`/exams/${exam.id}`}>
        {inProgress
          ? "Resume exam"
          : attempts.length
            ? "View results"
            : "View exam"}
        <ArrowRight size={15} />
      </Link>
    </article>
  );
}
