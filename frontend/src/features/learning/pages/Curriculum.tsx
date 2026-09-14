import { tracks } from "@/features/learning/model/catalog";
import {
  exerciseKey,
  lessonExercises,
  trackProgress,
} from "@/features/learning/model/progress";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import { Search, Sparkles } from "lucide-react";
import { useState } from "react";
import TrackCard from "../components/TrackCard";
export default function Curriculum() {
  const [query, setQuery] = useState(""),
    [filter, setFilter] = useState("All tracks");
  const { state } = useWorkspace();
  const filtered = tracks.filter((track) => {
    const progress = trackProgress(track, state);
    const started =
      progress.percent > 0 ||
      track.modules.some(
        (lesson) =>
          state.drafts[lesson.id] ||
          lessonExercises(lesson).some(
            (_, index) => state.submissions[exerciseKey(lesson.id, index)],
          ),
      ) ||
      track.exams.some(
        (exam) =>
          state.examDrafts[exam.id] || state.examAttempts[exam.id]?.length,
      );
    return (
      `${track.title} ${track.description} ${track.modules.map((module) => module.title).join(" ")}`
        .toLowerCase()
        .includes(query.toLowerCase()) &&
      (filter === "All tracks" ||
        (filter === "In progress" && started && !progress.complete) ||
        (filter === "Not started" && !started) ||
        (filter === "Completed" && progress.complete))
    );
  });
  return (
    <div className="page">
      <div className="page-eyebrow">A CONNECTED CURRICULUM</div>
      <h1>Start with the basics. Build your perspective.</h1>
      <p className="page-subtitle">
        Explore {tracks.length} connected courses, from market fundamentals and
        careful investing to company analysis, strategy research, and algorithm
        evaluation.
      </p>
      <div className="catalog-toolbar">
        <div className="tabs">
          {["All tracks", "In progress", "Not started", "Completed"].map(
            (f) => (
              <button
                key={f}
                className={filter === f ? "active" : ""}
                onClick={() => setFilter(f)}
              >
                {f}
              </button>
            ),
          )}
        </div>
        <label className="search-input compact">
          <Search size={16} />
          <input
            aria-label="Search curriculum"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search curriculum…"
          />
        </label>
      </div>
      <div className="track-grid">
        {filtered.map((t) => (
          <TrackCard key={t.id} track={t} />
        ))}
      </div>
      {!filtered.length ? (
        <div className="empty-state">
          <Search size={28} />
          <h3>No matching tracks</h3>
          <p>Try another topic or switch to all tracks.</p>
        </div>
      ) : null}
      <div className="curriculum-note">
        <Sparkles size={20} />
        <p>
          <strong>Learning happens in the details.</strong> Each module includes
          original reading, a worked example, a practical code worksheet, and a
          practice check. Course exams bring the ideas together with new
          scenarios, feedback, and retakes.
        </p>
      </div>
    </div>
  );
}
