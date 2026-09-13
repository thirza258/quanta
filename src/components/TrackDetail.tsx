import { Link, useParams } from "react-router-dom";
import {
  ArrowLeft,
  ArrowRight,
  BookOpen,
  Check,
  ChevronRight,
  Clock3,
  Play,
} from "lucide-react";
import { tracks } from "../lib/catalog";
import { useWorkspace } from "../lib/workspace";
import { TrackArt } from "./ui";
export default function TrackDetail() {
  const { trackId } = useParams(),
    track = tracks.find((t) => t.id === trackId),
    { state } = useWorkspace();
  if (!track)
    return (
      <div className="page">
        <h1>Track not found</h1>
        <Link className="button secondary" to="/curriculum">
          Return to curriculum
        </Link>
      </div>
    );
  const completed = track.modules.filter((m) =>
      state.completed.includes(m.id),
    ).length,
    next =
      track.modules.find((m) => !state.completed.includes(m.id)) ||
      track.modules[0];
  return (
    <div className="page track-detail">
      <Link to="/curriculum" className="text-link back-link">
        <ArrowLeft size={15} />
        All learning tracks
      </Link>
      <div className="track-detail-hero">
        <div>
          <div className="page-eyebrow">
            TRACK {String(track.number).padStart(2, "0")}
            <span className="level-badge">{track.level}</span>
          </div>
          <h1>{track.title}</h1>
          <p className="page-subtitle">{track.description}</p>
          <p className="source-line">{track.source}</p>
          <div className="inline-meta">
            <span>
              <BookOpen size={16} />
              {track.modules.length} modules
            </span>
            <span>
              <Clock3 size={16} />
              {track.modules.reduce((n, m) => n + m.minutes, 0)} minutes of
              reading
            </span>
          </div>
          <Link className="button primary" to={`/learn/${next.id}`}>
            {completed ? "Continue track" : "Start this track"}
            <ArrowRight size={16} />
          </Link>
        </div>
        <TrackArt kind={track.icon} large />
      </div>
      <div className="track-progress-row">
        <span>
          {completed} of {track.modules.length} modules completed
        </span>
        <strong>{Math.round((completed / track.modules.length) * 100)}%</strong>
      </div>
      <div className="progress-track">
        <span
          style={{ width: `${(completed / track.modules.length) * 100}%` }}
        />
      </div>
      <div className="section-heading">
        <div>
          <h2>Inside this track</h2>
          <p>A principle, an example, and an experiment in every module.</p>
        </div>
      </div>
      <div className="module-list">
        {track.modules.map((m, i) => (
          <Link to={`/learn/${m.id}`} key={m.id} className="module-row">
            <span
              className={`module-state ${state.completed.includes(m.id) ? "complete" : ""}`}
            >
              {state.completed.includes(m.id) ? (
                <Check size={19} />
              ) : (
                String(i + 1).padStart(2, "0")
              )}
            </span>
            <div>
              <span className="eyebrow">MODULE {m.id}</span>
              <h3>{m.title}</h3>
              <p>{m.subtitle}</p>
            </div>
            <span className="module-minutes">
              <Clock3 size={14} />
              {m.minutes} min
            </span>
            <span className="module-type">
              <Play size={12} />
              Interactive
            </span>
            <ChevronRight size={20} />
          </Link>
        ))}
      </div>
    </div>
  );
}
