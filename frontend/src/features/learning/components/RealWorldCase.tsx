import { caseKindLabels } from "@/features/learning/model/cases";
import type { CaseStudy, Lesson } from "@/features/learning/model/types";
import MarkdownRenderer from "@/shared/components/MarkdownRenderer";
import { ArrowUpRight, BookmarkPlus, MapPin } from "lucide-react";
import { useEffect, useRef } from "react";
import { useLocation } from "react-router-dom";
import "./real-world-cases.css";

export default function RealWorldCase({
  lesson,
  caseStudy,
  onWrite,
}: {
  lesson: Lesson;
  caseStudy: CaseStudy;
  onWrite: () => void;
}) {
  const { hash } = useLocation();
  const panel = useRef<HTMLElement>(null);
  useEffect(() => {
    if (hash !== "#real-world-case") return;
    // Wait until the route's normal scroll reset has finished, including lazy loading.
    const frame = requestAnimationFrame(() => {
      panel.current?.scrollIntoView({ block: "start" });
      panel.current?.focus({ preventScroll: true });
    });
    return () => cancelAnimationFrame(frame);
  }, [hash, lesson.id]);

  return (
    <section
      ref={panel}
      id="real-world-case"
      className="real-world-case"
      aria-labelledby="real-world-title"
      tabIndex={-1}
    >
      <div className="case-heading-meta">
        <span className="eyebrow">FROM LESSON TO REAL LIFE</span>
        <span className="case-kind">{caseKindLabels[caseStudy.kind]}</span>
      </div>
      <h2 id="real-world-title">{caseStudy.title}</h2>
      <p className="case-setting">
        <MapPin size={15} aria-hidden="true" />
        {caseStudy.setting}
      </p>
      <p className="case-period">{caseStudy.period}</p>
      <p>
        <MarkdownRenderer content={caseStudy.context} inline />
      </p>
      <div className="case-sources" aria-label="Case references">
        <h3>Source &amp; context</h3>
        {caseStudy.references.map((reference) => (
          <div key={reference.url}>
            <a href={reference.url} target="_blank" rel="noopener noreferrer">
              {reference.title}
              <ArrowUpRight size={14} aria-hidden="true" />
            </a>
            <p>{reference.scope}</p>
          </div>
        ))}
      </div>
      <p className="case-boundary">
        <MarkdownRenderer content={caseStudy.boundary} inline />
      </p>
      <div className="case-application">
        <h3>How this connects to the lesson</h3>
        <p>
          <MarkdownRenderer content={lesson.realWorld.connection} inline />
        </p>
        <h3>Your task</h3>
        <p>
          <MarkdownRenderer content={lesson.realWorld.task} inline />
        </p>
        <button className="button secondary small" onClick={onWrite}>
          <BookmarkPlus size={15} aria-hidden="true" /> Work through this case
        </button>
        <details className="case-walkthrough">
          <summary>Compare your reasoning</summary>
          <p>
            <MarkdownRenderer content={lesson.realWorld.walkthrough} inline />
          </p>
        </details>
      </div>
    </section>
  );
}
