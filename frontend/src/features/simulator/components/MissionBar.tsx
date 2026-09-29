import type { MissionProgress } from "@/features/simulator/model/types";
import "@/features/simulator/simulator.css";
import { Check, Target } from "lucide-react";

export default function MissionBar({
  mission,
}: {
  mission: MissionProgress | null;
}) {
  if (!mission) return null;
  return (
    <details
      className={`sim-mission ${mission.complete ? "complete" : ""}`}
      aria-label="Practice mission"
    >
      <summary>
        <Target size={15} />
        <strong>{mission.title}</strong>
        <span className="sim-mission-sub">{mission.subtitle}</span>
        <span className="sim-mission-score">
          {mission.complete
            ? "All objectives met"
            : `${mission.met} of ${mission.total} objectives`}
        </span>
        <span className="sim-mission-chips" aria-hidden="true">
          {mission.objectives.map((objective) => (
            <span
              key={objective.id}
              className={objective.met ? "met" : ""}
              title={objective.title}
            />
          ))}
        </span>
      </summary>
      <div className="sim-mission-body">
        <p className="sim-mission-brief">{mission.brief}</p>
        <ol className="sim-mission-list">
          {mission.objectives.map((objective) => (
            <li key={objective.id} className={objective.met ? "met" : ""}>
              <span className="sim-mission-mark" aria-hidden="true">
                {objective.met ? <Check size={13} /> : null}
              </span>
              <div>
                <strong>{objective.title}</strong>
                <span className="sim-mission-detail">{objective.detail}</span>
                <span className="sim-mission-progress">
                  {objective.progress}
                </span>
              </div>
            </li>
          ))}
        </ol>
        <p className="sim-small">
          Objectives describe what you did and recorded, not what the trade
          returned. A profitable breach of a rule is still a breach, and a loss
          taken while following the rules is not evidence the rules were wrong.
        </p>
      </div>
    </details>
  );
}
