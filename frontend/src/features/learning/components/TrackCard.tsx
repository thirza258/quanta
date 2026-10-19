import {
  TrackArt,
  TrackIcon,
} from "@/features/learning/components/TrackVisuals";
import { trackLabel } from "@/features/learning/model/catalog";
import { trackProgress } from "@/features/learning/model/progress";
import type { Track } from "@/features/learning/model/types";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import MarkdownRenderer from "@/shared/components/MarkdownRenderer";
import { ArrowUpRight, BookOpen } from "lucide-react";
import { Link } from "react-router-dom";
export default function TrackCard({ track }: { track: Track }) {
  const { state } = useWorkspace(),
    progress = trackProgress(track, state);
  return (
    <Link className="track-card" to={`/curriculum/${track.id}`}>
      <div className="track-card-top">
        <span className="track-number">{trackLabel(track)}</span>
        <span className={`level-badge ${track.level.toLowerCase()}`}>
          {track.level}
        </span>
      </div>
      <div className="track-art-wrap">
        <TrackArt kind={track.icon} />
        <span className="track-icon">
          <TrackIcon kind={track.icon} />
        </span>
      </div>
      <h3>{track.title}</h3>
      <p>
        <MarkdownRenderer content={track.description} inline />
      </p>
      <div className="track-card-footer">
        <span>
          <BookOpen size={13} />
          {track.modules.length} modules<span className="dot-separator">·</span>
          {Math.round(
            (track.modules.reduce((n, l) => n + l.minutes, 0) / 60) * 10,
          ) / 10}{" "}
          hrs
        </span>
        <ArrowUpRight size={17} />
      </div>
      <div className="track-assessment-meta">
        <span>
          {track.exams.length} {track.exams.length === 1 ? "exam" : "exams"}
        </span>
        <span>
          {progress.complete
            ? "Course complete"
            : `${progress.percent}% complete`}
        </span>
      </div>
      {progress.percent > 0 ? (
        <div
          className="card-progress"
          style={{ width: `${progress.percent}%` }}
        />
      ) : null}
    </Link>
  );
}
