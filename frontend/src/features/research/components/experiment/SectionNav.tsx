import type { SectionId } from "@/features/research/model/experiment";
import { SECTIONS } from "@/features/research/model/experiment";
import { useEffect, useRef, useState } from "react";

/** How far below the viewport top a section must start to count as read. */
const OFFSET = 120;

function currentSection(): SectionId {
  const atBottom =
    window.innerHeight + window.scrollY >=
    document.documentElement.scrollHeight - 2;
  if (atBottom) return SECTIONS[SECTIONS.length - 1].id;
  let active: SectionId = SECTIONS[0].id;
  for (const section of SECTIONS) {
    const element = document.getElementById(section.id);
    if (element && element.getBoundingClientRect().top <= OFFSET)
      active = section.id;
  }
  return active;
}

/** Sticky in-page navigation; highlights the section being read. */
export function SectionNav() {
  const [active, setActive] = useState<SectionId>("overview");
  const list = useRef<HTMLUListElement>(null);
  // Keep the active link visible when the nav scrolls sideways (narrow screens).
  useEffect(() => {
    const ul = list.current;
    const link = ul?.querySelector<HTMLElement>("a.is-active");
    if (!ul || !link) return;
    const left = link.offsetLeft - ul.offsetLeft;
    if (
      left < ul.scrollLeft ||
      left + link.offsetWidth > ul.scrollLeft + ul.clientWidth
    )
      ul.scrollTo({ left: Math.max(0, left - 16) });
  }, [active]);
  useEffect(() => {
    let frame = 0;
    const update = () => {
      cancelAnimationFrame(frame);
      frame = requestAnimationFrame(() => setActive(currentSection()));
    };
    update();
    window.addEventListener("scroll", update, { passive: true });
    window.addEventListener("resize", update);
    return () => {
      cancelAnimationFrame(frame);
      window.removeEventListener("scroll", update);
      window.removeEventListener("resize", update);
    };
  }, []);
  return (
    <nav className="xd-nav" aria-label="Experiment sections">
      <ul ref={list}>
        {SECTIONS.map((section) => (
          <li key={section.id}>
            <a
              href={`#${section.id}`}
              className={active === section.id ? "is-active" : undefined}
              aria-current={active === section.id ? "location" : undefined}
              onClick={(event) => {
                const target = document.getElementById(section.id);
                if (!target) return;
                event.preventDefault();
                const reduce = window.matchMedia?.(
                  "(prefers-reduced-motion: reduce)",
                ).matches;
                target.scrollIntoView({
                  behavior: reduce ? "auto" : "smooth",
                  block: "start",
                });
                document
                  .getElementById(`${section.id}-title`)
                  ?.focus({ preventScroll: true });
              }}
            >
              {section.label}
            </a>
          </li>
        ))}
      </ul>
    </nav>
  );
}
