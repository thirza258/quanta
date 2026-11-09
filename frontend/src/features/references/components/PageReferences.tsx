import {
  examTrack,
  findLesson,
  lessonTrack,
  tracks,
} from "@/features/learning/model/catalog";
import { Link, useLocation } from "react-router-dom";

const chartReference = {
  title: "TradingView · Lightweight Charts™",
  url: "https://www.tradingview.com/lightweight-charts/",
};

export default function PageReferences() {
  const { pathname } = useLocation();
  const [, section, id] = pathname.split("/");
  const lesson = section === "learn" ? findLesson(id) : undefined;
  const track =
    section === "learn"
      ? lessonTrack(id)
      : section === "exams"
        ? examTrack(id)
        : section === "curriculum"
          ? tracks.find((item) => item.id === id)
          : section === "lab" ||
              section === "experiments" ||
              section === "research"
            ? tracks.find((item) => item.id === "strategy-lab")
            : undefined;
  const references =
    section === "simulator"
      ? [chartReference, ...(tracks[0].references ?? [])]
      : (lesson?.references ?? track?.references ?? tracks[0].references ?? []);
  return (
    <footer className="page-references" aria-label="Sources and attribution">
      <div className="page-references-heading">
        <strong>
          {lesson ? "Lesson references" : "Sources & attribution"}
        </strong>
        <Link className="text-link" to="/library">
          Full reference library
        </Link>
      </div>
      {lesson?.reading ? <p>{lesson.reading}</p> : null}
      <ul>
        {references.map((reference) => (
          <li key={reference.url}>
            <a href={reference.url} target="_blank" rel="noopener noreferrer">
              {reference.title}
            </a>
          </li>
        ))}
      </ul>
      <p>
        Quanta’s course explanations and exercises are original teaching
        material. Documented events cite their sources; fictional scenarios and
        exercise data are labeled. Books, research, and documentation are
        credited to their respective authors. Quanta is an independent learning
        project; references do not imply affiliation or endorsement.
      </p>
      {section === "simulator" ? (
        <p>
          Charts use TradingView’s Lightweight Charts™ library. Market and
          execution assumptions are described in{" "}
          <Link to="/methodology">How Quanta works</Link>.
        </p>
      ) : null}
      <Link className="text-link" to="/library#source-use">
        Source use and permissions
      </Link>
    </footer>
  );
}
