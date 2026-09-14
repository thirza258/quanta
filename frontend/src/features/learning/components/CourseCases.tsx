import {
  caseKindLabels,
  caseLessonLinks,
} from "@/features/learning/model/cases";
import type { Track } from "@/features/learning/model/types";
import { ArrowRight } from "lucide-react";
import { Link } from "react-router-dom";
import "./real-world-cases.css";

export default function CourseCases({ track }: { track: Track }) {
  const links = caseLessonLinks(track);
  return (
    <section className="course-cases" aria-labelledby="course-cases-title">
      <span className="eyebrow">PUT THE IDEAS TO WORK</span>
      <h2 id="course-cases-title">Real-world practice in every lesson</h2>
      <p>
        {track.modules.length} lesson applications across {links.length} cases.
        Connect the ideas to everyday decisions, documented events, and
        practical systems. Each lesson includes a task, a worked explanation,
        and sources.
      </p>
      <details>
        <summary>Explore the cases in this course</summary>
        <ul className="course-case-grid">
          {links.map(({ caseStudy, lessonId }) => (
            <li key={caseStudy.id}>
              <Link to={`/learn/${lessonId}#real-world-case`}>
                <span className="case-kind">
                  {caseKindLabels[caseStudy.kind]}
                </span>
                <strong>{caseStudy.title}</strong>
                <span className="case-setting">{caseStudy.setting}</span>
                <span className="text-link">
                  Explore in module {lessonId}
                  <ArrowRight size={14} />
                </span>
              </Link>
            </li>
          ))}
        </ul>
      </details>
      <p className="case-time-note">
        Case tasks are optional extra practice beyond the listed lesson time.
      </p>
    </section>
  );
}

export function UnitCases({ track, part }: { track: Track; part: string }) {
  return (
    <div className="unit-cases">
      <strong>Cases in this unit</strong>
      <ul>
        {caseLessonLinks(track, part).map(({ caseStudy, lessonId }) => (
          <li key={caseStudy.id}>
            <Link to={`/learn/${lessonId}#real-world-case`}>
              {caseStudy.title}
              <ArrowRight size={13} aria-hidden="true" />
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
