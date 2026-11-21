import {
  courseConnections,
  DOMAIN_CONFIG,
  getConnection,
  getCourseReadiness,
  getMissingPrerequisites,
  getRecommendedNextTracks,
  learningPathways,
  STAGE_CONFIG,
  type CourseDomain,
  type CourseReadiness,
  type CourseStage,
} from "@/features/learning/model/connections";
import { trackLabel, tracks } from "@/features/learning/model/catalog";
import { trackProgress } from "@/features/learning/model/progress";
import { useWorkspace } from "@/features/workspace/WorkspaceProvider";
import {
  ArrowRight,
  BookOpen,
  CheckCircle2,
  Clock,
  Compass,
  FileText,
  GitFork,
  Layers,
  Lock,
  Network,
  Route,
  Search,
  Sparkles,
  Table,
  X,
} from "lucide-react";
import { useState } from "react";
import { Link } from "react-router-dom";
import "../course-map.css";

export default function CourseMap() {
  const { state } = useWorkspace();
  const [viewMode, setViewMode] = useState<"map" | "pathways" | "matrix">(
    "map",
  );
  const [selectedTrackId, setSelectedTrackId] = useState<string | null>(
    "trading-fundamentals",
  );
  const [activePathwayId, setActivePathwayId] = useState<string>(
    learningPathways[0].id,
  );
  const [domainFilter, setDomainFilter] = useState<CourseDomain | "all">("all");
  const [searchQuery, setSearchQuery] = useState("");

  // Progress summary
  const completedCount = tracks.filter(
    (t) => trackProgress(t, state).complete,
  ).length;
  const inProgressCount = tracks.filter((t) => {
    const p = trackProgress(t, state);
    return p.percent > 0 && !p.complete;
  }).length;
  const readyCount = tracks.filter((t) => {
    const p = trackProgress(t, state);
    return p.percent === 0 && getCourseReadiness(t, state) === "ready";
  }).length;

  const recommendedTracks = getRecommendedNextTracks(state);

  const selectedTrack = selectedTrackId
    ? tracks.find((t) => t.id === selectedTrackId)
    : null;
  const selectedConnection = selectedTrackId
    ? getConnection(selectedTrackId)
    : null;

  const activePathway =
    learningPathways.find((p) => p.id === activePathwayId) ??
    learningPathways[0];

  // Filtered tracks for map and matrix
  const filteredConnections = courseConnections.filter((conn) => {
    const track = tracks.find((t) => t.id === conn.id);
    if (!track) return false;
    const matchesDomain =
      domainFilter === "all" || conn.domain === domainFilter;
    const matchesQuery =
      !searchQuery.trim() ||
      track.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      conn.focusSummary.toLowerCase().includes(searchQuery.toLowerCase()) ||
      conn.skillsGained.some((s) =>
        s.toLowerCase().includes(searchQuery.toLowerCase()),
      );
    return matchesDomain && matchesQuery;
  });

  const stages: CourseStage[] = [1, 2, 3, 4];

  const renderReadinessBadge = (readiness: CourseReadiness) => {
    switch (readiness) {
      case "completed":
        return (
          <span className="readiness-pill completed">
            <CheckCircle2 size={12} /> Completed
          </span>
        );
      case "in_progress":
        return (
          <span className="readiness-pill in_progress">
            <Clock size={12} /> In progress
          </span>
        );
      case "ready":
        return (
          <span className="readiness-pill ready">
            <Sparkles size={12} /> Ready to start
          </span>
        );
      case "locked":
        return (
          <span className="readiness-pill locked">
            <Lock size={12} /> Missing prereqs
          </span>
        );
    }
  };

  return (
    <div className="page course-map-page">
      <div className="page-eyebrow">
        <Network size={15} /> CURRICULUM ARCHITECTURE & PREREQUISITES
      </div>

      <div className="page-title-row">
        <div>
          <h1>Course Connections & Pathways</h1>
          <p className="page-subtitle">
            Understand how all {tracks.length} courses connect, what each step
            prepares you for, and follow curated sequences aligned with your
            goals.
          </p>
        </div>
        <div className="certification-heading-actions">
          <Link to="/curriculum" className="button secondary">
            <BookOpen size={16} /> Browse all courses
          </Link>
        </div>
      </div>

      {/* Progress Summary Strip */}
      <div
        className="map-summary-strip"
        aria-label="Overall curriculum progress"
      >
        <div className="map-summary-item">
          <strong>{tracks.length}</strong>
          <span>Total Courses</span>
        </div>
        <div className="map-summary-item">
          <strong style={{ color: "#16a34a" }}>{completedCount}</strong>
          <span>Courses Completed</span>
        </div>
        <div className="map-summary-item">
          <strong style={{ color: "var(--accent)" }}>{inProgressCount}</strong>
          <span>In Progress</span>
        </div>
        <div className="map-summary-item">
          <strong style={{ color: "#0284c7" }}>{readyCount}</strong>
          <span>Ready to Begin</span>
        </div>
      </div>

      {/* Next Recommended Step Banner */}
      <div className="map-recommendation-box">
        <div className="map-rec-header">
          <div className="map-rec-title">
            <Compass size={18} />
            <span>Recommended Next Courses for You</span>
          </div>
          <span style={{ fontSize: "var(--text-xs)", color: "var(--muted)" }}>
            Based on your completed prerequisites and drafts
          </span>
        </div>
        <div className="map-rec-grid">
          {recommendedTracks.map((recTrack) => {
            const conn = getConnection(recTrack.id);
            const progress = trackProgress(recTrack, state);
            return (
              <Link
                key={recTrack.id}
                to={`/curriculum/${recTrack.id}`}
                className="map-rec-card"
              >
                <div>
                  <div className="map-rec-top">
                    <span className="node-track-id">
                      {trackLabel(recTrack)}
                    </span>
                    {renderReadinessBadge(getCourseReadiness(recTrack, state))}
                  </div>
                  <h4>{recTrack.title}</h4>
                  <p className="map-rec-desc">
                    {conn?.focusSummary || recTrack.description}
                  </p>
                </div>
                <div className="map-rec-footer">
                  <span>
                    {progress.percent > 0
                      ? `${progress.percent}% complete`
                      : `${recTrack.modules.length} lessons · ${recTrack.exams.length} exams`}
                  </span>
                  <span
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "4px",
                    }}
                  >
                    {progress.percent > 0 ? "Continue" : "Start"}
                    <ArrowRight size={14} />
                  </span>
                </div>
              </Link>
            );
          })}
        </div>
      </div>

      {/* Toolbar for Views & Filters */}
      <div className="map-view-toolbar">
        <div className="map-view-tabs" role="tablist" aria-label="Map views">
          <button
            role="tab"
            aria-selected={viewMode === "map"}
            className={`map-view-tab ${viewMode === "map" ? "active" : ""}`}
            onClick={() => setViewMode("map")}
          >
            <GitFork size={16} /> Interactive Course Map
          </button>
          <button
            role="tab"
            aria-selected={viewMode === "pathways"}
            className={`map-view-tab ${viewMode === "pathways" ? "active" : ""}`}
            onClick={() => setViewMode("pathways")}
          >
            <Route size={16} /> Curated Pathways
          </button>
          <button
            role="tab"
            aria-selected={viewMode === "matrix"}
            className={`map-view-tab ${viewMode === "matrix" ? "active" : ""}`}
            onClick={() => setViewMode("matrix")}
          >
            <Table size={16} /> Prerequisites Matrix
          </button>
        </div>

        {viewMode !== "pathways" && (
          <div className="search-input compact" style={{ maxWidth: 280 }}>
            <Search size={15} />
            <input
              placeholder="Filter courses & skills…"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              aria-label="Filter courses"
            />
            {searchQuery ? (
              <button
                className="icon-button"
                aria-label="Clear course search"
                onClick={() => setSearchQuery("")}
              >
                <X size={15} />
              </button>
            ) : null}
          </div>
        )}
      </div>

      {/* Domain Filters (for Map & Matrix) */}
      {viewMode !== "pathways" && (
        <div style={{ marginBottom: 28 }}>
          <div className="domain-chips">
            <span
              style={{
                fontSize: "var(--text-xs)",
                color: "var(--muted)",
                marginRight: 4,
              }}
            >
              Domain:
            </span>
            <button
              className={`domain-chip ${domainFilter === "all" ? "active" : ""}`}
              onClick={() => setDomainFilter("all")}
            >
              All Domains ({tracks.length})
            </button>
            {(Object.keys(DOMAIN_CONFIG) as CourseDomain[]).map((dom) => (
              <button
                key={dom}
                className={`domain-chip ${domainFilter === dom ? "active" : ""}`}
                onClick={() => setDomainFilter(dom)}
              >
                {DOMAIN_CONFIG[dom].label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* VIEW 1: INTERACTIVE COURSE MAP */}
      {viewMode === "map" && (
        <div>
          {stages.map((stageNum) => {
            const stageConfig = STAGE_CONFIG[stageNum];
            const stageConns = filteredConnections.filter(
              (c) => c.stage === stageNum,
            );
            if (stageConns.length === 0) return null;

            return (
              <section
                key={stageNum}
                className="stage-section"
                aria-label={stageConfig.name}
              >
                <div className="stage-header">
                  <div className="stage-badge-row">
                    <span className="stage-pill">{stageConfig.badge}</span>
                    <span
                      style={{
                        fontSize: "var(--text-xs)",
                        color: "var(--muted)",
                      }}
                    >
                      {stageConns.length}{" "}
                      {stageConns.length === 1 ? "course" : "courses"}
                    </span>
                  </div>
                  <h3 className="stage-title">{stageConfig.name}</h3>
                  <p className="stage-desc">{stageConfig.subtitle}</p>
                </div>

                <div className="stage-cards-grid">
                  {stageConns.map((conn) => {
                    const track = tracks.find((t) => t.id === conn.id)!;
                    const readiness = getCourseReadiness(track, state);
                    const isSelected = selectedTrackId === conn.id;
                    const isPrereqOfSelected =
                      selectedConnection?.prerequisites.includes(conn.id) ??
                      false;
                    const isUnlockedBySelected =
                      selectedConnection?.unlocks.includes(conn.id) ?? false;

                    let highlightClass = "";
                    if (isSelected) highlightClass = "selected";
                    else if (isPrereqOfSelected)
                      highlightClass = "is-prerequisite-of-selected";
                    else if (isUnlockedBySelected)
                      highlightClass = "is-unlocked-by-selected";

                    return (
                      <div
                        key={conn.id}
                        className={`course-node-card ${highlightClass}`}
                        onClick={() => setSelectedTrackId(conn.id)}
                        role="button"
                        tabIndex={0}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" || e.key === " ") {
                            e.preventDefault();
                            setSelectedTrackId(conn.id);
                          }
                        }}
                        aria-pressed={isSelected}
                      >
                        <div>
                          <div className="node-top-meta">
                            <span className="node-track-id">
                              {trackLabel(track)}
                            </span>
                            {renderReadinessBadge(readiness)}
                          </div>
                          <h4 className="node-title">{track.title}</h4>
                          <p className="node-summary">{conn.focusSummary}</p>
                        </div>

                        <div>
                          <div
                            style={{
                              display: "flex",
                              gap: "4px",
                              flexWrap: "wrap",
                              marginBottom: "10px",
                            }}
                          >
                            <span
                              style={{
                                fontSize: "0.6875rem",
                                padding: "2px 6px",
                                borderRadius: "4px",
                                background: "var(--surface)",
                                border: "1px solid var(--border)",
                                color: "var(--muted)",
                              }}
                            >
                              {track.level}
                            </span>
                            <span
                              style={{
                                fontSize: "0.6875rem",
                                padding: "2px 6px",
                                borderRadius: "4px",
                                background: "var(--surface)",
                                border: "1px solid var(--border)",
                                color: "var(--muted)",
                              }}
                            >
                              {conn.domainLabel}
                            </span>
                          </div>

                          <div className="node-connections-row">
                            <span className="node-conn-item">
                              <Layers size={13} />
                              {conn.prerequisites.length === 0
                                ? "Entry point"
                                : `${conn.prerequisites.length} prereq${conn.prerequisites.length === 1 ? "" : "s"}`}
                            </span>
                            <span className="node-conn-item">
                              <Sparkles size={13} />
                              {conn.unlocks.length === 0
                                ? "Capstone"
                                : `Unlocks ${conn.unlocks.length}`}
                            </span>
                          </div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </section>
            );
          })}

          {/* Connection Inspector Panel */}
          {selectedTrack && selectedConnection && (
            <div
              className="map-inspector"
              aria-label="Selected course connection inspector"
            >
              <div className="inspector-header">
                <div className="inspector-title-area">
                  <div className="inspector-stage-tag">
                    {selectedConnection.stageName} · {trackLabel(selectedTrack)}
                  </div>
                  <h2 className="inspector-title">{selectedTrack.title}</h2>
                  <p
                    style={{
                      margin: 0,
                      fontSize: "var(--text-sm)",
                      color: "var(--secondary)",
                    }}
                  >
                    {selectedTrack.description}
                  </p>
                </div>
                <div className="inspector-actions">
                  <Link
                    to={`/curriculum/${selectedTrack.id}`}
                    className="button primary"
                  >
                    Open course <ArrowRight size={15} />
                  </Link>
                  <button
                    className="icon-button"
                    aria-label="Close inspector"
                    onClick={() => setSelectedTrackId(null)}
                  >
                    <X size={18} />
                  </button>
                </div>
              </div>

              <div className="inspector-grid">
                {/* Prerequisites Column */}
                <div className="inspector-section">
                  <h4>
                    <Lock size={15} /> Prerequisites (What to take first)
                  </h4>
                  <p>{selectedConnection.whyPrerequisites}</p>
                  {selectedConnection.prerequisites.length === 0 ? (
                    <span
                      style={{
                        fontSize: "var(--text-xs)",
                        color: "var(--muted)",
                        fontStyle: "italic",
                      }}
                    >
                      None — this is a foundational starting point.
                    </span>
                  ) : (
                    <div className="conn-chips-list">
                      {selectedConnection.prerequisites.map((prereqId) => {
                        const prereqTrack = tracks.find(
                          (t) => t.id === prereqId,
                        );
                        if (!prereqTrack) return null;
                        const isDone = trackProgress(
                          prereqTrack,
                          state,
                        ).complete;
                        return (
                          <button
                            key={prereqId}
                            className="conn-link-chip prereq-badge"
                            onClick={() => setSelectedTrackId(prereqId)}
                            title="Click to inspect this prerequisite course"
                          >
                            {isDone ? (
                              <CheckCircle2 size={13} color="#16a34a" />
                            ) : (
                              <Clock size={13} color="var(--muted)" />
                            )}
                            <span>{prereqTrack.title}</span>
                          </button>
                        );
                      })}
                    </div>
                  )}

                  {selectedConnection.recommendedBefore.length > 0 && (
                    <div style={{ marginTop: 12 }}>
                      <span
                        style={{
                          fontSize: "0.6875rem",
                          color: "var(--muted)",
                          display: "block",
                          marginBottom: 4,
                        }}
                      >
                        Helpful prior context:
                      </span>
                      <div className="conn-chips-list">
                        {selectedConnection.recommendedBefore.map((recId) => {
                          const recTrack = tracks.find((t) => t.id === recId);
                          if (!recTrack) return null;
                          return (
                            <button
                              key={recId}
                              className="conn-link-chip"
                              onClick={() => setSelectedTrackId(recId)}
                            >
                              <span>{recTrack.title}</span>
                            </button>
                          );
                        })}
                      </div>
                    </div>
                  )}
                </div>

                {/* Unlocks Column */}
                <div className="inspector-section">
                  <h4>
                    <Sparkles size={15} /> Subsequent Steps (What this unlocks)
                  </h4>
                  <p>{selectedConnection.whyUnlocks}</p>
                  {selectedConnection.unlocks.length === 0 ? (
                    <span
                      style={{
                        fontSize: "var(--text-xs)",
                        color: "var(--muted)",
                        fontStyle: "italic",
                      }}
                    >
                      Capstone destination — brings prior disciplines together.
                    </span>
                  ) : (
                    <div className="conn-chips-list">
                      {selectedConnection.unlocks.map((unlockId) => {
                        const unlockTrack = tracks.find(
                          (t) => t.id === unlockId,
                        );
                        if (!unlockTrack) return null;
                        return (
                          <button
                            key={unlockId}
                            className="conn-link-chip unlock-badge"
                            onClick={() => setSelectedTrackId(unlockId)}
                            title="Click to inspect this unlocked course"
                          >
                            <ArrowRight size={13} color="#16a34a" />
                            <span>{unlockTrack.title}</span>
                          </button>
                        );
                      })}
                    </div>
                  )}
                </div>

                {/* Skills Column */}
                <div className="inspector-section">
                  <h4>
                    <FileText size={15} /> Key Skills & Methodologies
                  </h4>
                  <p>
                    Practical competencies developed throughout this course:
                  </p>
                  <div>
                    {selectedConnection.skillsGained.map((skill) => (
                      <span key={skill} className="skill-tag-pill">
                        {skill}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* VIEW 2: CURATED PATHWAYS */}
      {viewMode === "pathways" && (
        <div>
          {/* Pathway Tab Selector */}
          <div
            className="pathway-selector-row"
            role="tablist"
            aria-label="Curated learning pathways"
          >
            {learningPathways.map((pathway) => (
              <button
                key={pathway.id}
                role="tab"
                aria-selected={activePathwayId === pathway.id}
                className={`pathway-tab-btn ${activePathwayId === pathway.id ? "active" : ""}`}
                onClick={() => setActivePathwayId(pathway.id)}
              >
                <span className="pathway-tab-title">{pathway.title}</span>
                <span className="pathway-tab-role">
                  {pathway.steps.length} steps · {pathway.badge}
                </span>
              </button>
            ))}
          </div>

          {/* Active Pathway Header Banner */}
          <div className="pathway-banner">
            <div className="pathway-banner-top">
              <span className="pathway-banner-badge">
                {activePathway.badge}
              </span>
              <span
                style={{ fontSize: "var(--text-xs)", color: "var(--muted)" }}
              >
                Target Profile: {activePathway.targetRole}
              </span>
            </div>
            <h2
              style={{
                margin: "0 0 8px",
                fontSize: "var(--text-xl)",
                color: "var(--text)",
              }}
            >
              {activePathway.title}
            </h2>
            <p
              style={{
                margin: 0,
                fontSize: "var(--text-sm)",
                color: "var(--secondary)",
                lineHeight: 1.6,
              }}
            >
              {activePathway.description}
            </p>
          </div>

          {/* Step-by-Step Timeline */}
          <div className="pathway-steps-timeline">
            {activePathway.steps.map((step) => {
              const track = tracks.find((t) => t.id === step.trackId);
              if (!track) return null;
              const conn = getConnection(track.id);
              const progress = trackProgress(track, state);
              const readiness = getCourseReadiness(track, state);

              return (
                <div key={step.step} className="pathway-step-card">
                  <div className="pathway-step-marker">{step.step}</div>

                  <div className="pathway-step-info">
                    <div className="pathway-step-meta">
                      <span>STEP {step.step}</span>
                      <span>·</span>
                      <span>{conn?.stageName}</span>
                      <span>·</span>
                      <span>{track.level}</span>
                    </div>
                    <h3 className="pathway-step-title">{track.title}</h3>
                    <p className="pathway-step-why">
                      <strong>Why take this now:</strong> {step.whyThisStep}
                    </p>
                    <p className="pathway-step-deliverable">
                      <strong>Key deliverable:</strong> {step.keyDeliverable}
                    </p>
                  </div>

                  <div className="pathway-step-action">
                    {renderReadinessBadge(readiness)}
                    <Link
                      to={`/curriculum/${track.id}`}
                      className="button secondary"
                      style={{ fontSize: "var(--text-xs)", width: "100%" }}
                    >
                      {progress.percent > 0 ? "Continue" : "View course"}
                      <ArrowRight size={13} />
                    </Link>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* VIEW 3: PREREQUISITES MATRIX */}
      {viewMode === "matrix" && (
        <div className="matrix-container">
          <table
            className="matrix-table"
            aria-label="Full course prerequisites matrix"
          >
            <thead>
              <tr>
                <th style={{ width: "22%" }}>Course</th>
                <th style={{ width: "12%" }}>Stage</th>
                <th style={{ width: "14%" }}>Domain</th>
                <th style={{ width: "24%" }}>Direct Prerequisites</th>
                <th style={{ width: "18%" }}>Unlocks</th>
                <th style={{ width: "10%" }}>Status</th>
              </tr>
            </thead>
            <tbody>
              {filteredConnections.map((conn) => {
                const track = tracks.find((t) => t.id === conn.id)!;
                const readiness = getCourseReadiness(track, state);
                const missing = getMissingPrerequisites(conn.id, state);

                return (
                  <tr key={conn.id}>
                    <td>
                      <div className="matrix-course-col">
                        <Link
                          to={`/curriculum/${track.id}`}
                          className="text-link"
                          style={{ fontWeight: 600 }}
                        >
                          {track.title}
                        </Link>
                        <span
                          style={{
                            fontSize: "0.6875rem",
                            color: "var(--muted)",
                          }}
                        >
                          {trackLabel(track)} · {track.level}
                        </span>
                      </div>
                    </td>
                    <td>
                      <span className="stage-pill">Stage {conn.stage}</span>
                    </td>
                    <td>
                      <span
                        style={{
                          fontSize: "var(--text-xs)",
                          color: "var(--secondary)",
                        }}
                      >
                        {conn.domainLabel}
                      </span>
                    </td>
                    <td>
                      {conn.prerequisites.length === 0 ? (
                        <span style={{ color: "var(--muted)" }}>
                          None (Entry point)
                        </span>
                      ) : (
                        <div
                          style={{
                            display: "flex",
                            flexDirection: "column",
                            gap: "4px",
                          }}
                        >
                          {conn.prerequisites.map((pId) => {
                            const pTrack = tracks.find((t) => t.id === pId);
                            if (!pTrack) return null;
                            const isDone = trackProgress(
                              pTrack,
                              state,
                            ).complete;
                            return (
                              <span
                                key={pId}
                                style={{
                                  display: "inline-flex",
                                  alignItems: "center",
                                  gap: "4px",
                                  color: isDone
                                    ? "#16a34a"
                                    : "var(--secondary)",
                                }}
                              >
                                {isDone ? (
                                  <CheckCircle2 size={12} />
                                ) : (
                                  <Clock size={12} color="var(--muted)" />
                                )}
                                {pTrack.title}
                              </span>
                            );
                          })}
                          {missing.length > 0 && readiness === "locked" && (
                            <span
                              style={{
                                fontSize: "0.6875rem",
                                color: "var(--negative)",
                              }}
                            >
                              Needs {missing.length} prerequisite
                              {missing.length === 1 ? "" : "s"}
                            </span>
                          )}
                        </div>
                      )}
                    </td>
                    <td>
                      {conn.unlocks.length === 0 ? (
                        <span style={{ color: "var(--muted)" }}>
                          Capstone track
                        </span>
                      ) : (
                        <span style={{ color: "var(--secondary)" }}>
                          {conn.unlocks.length} course
                          {conn.unlocks.length === 1 ? "" : "s"}
                        </span>
                      )}
                    </td>
                    <td>{renderReadinessBadge(readiness)}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}

      {/* Educational Note at bottom */}
      <div className="curriculum-note" style={{ marginTop: 40 }}>
        <Sparkles size={20} />
        <p>
          <strong>Progression is flexible.</strong> Quanta courses are designed
          modularly. While prerequisites highlight the foundational concepts
          assumed in later lessons, you are free to explore any course at any
          time to match your current research question or project need.
        </p>
      </div>
    </div>
  );
}
