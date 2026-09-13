import { useSearchParams, Link } from "react-router-dom";
import {
  BookOpen,
  ChartNoAxesCombined,
  FlaskConical,
  ArrowUpRight,
  ArrowDownUp,
  Network,
} from "lucide-react";
import Sandbox from "./Sandbox";
import { AmmLab, BrokerLab, FactorLab, ValuationLab } from "./LabTools";
import { useWorkspace } from "../lib/workspace";
const tabs = [
  ["market", "Market sandbox", FlaskConical],
  ["valuation", "Valuation", BookOpen],
  ["factors", "Factor studio", ChartNoAxesCombined],
  ["broker", "Paper trading", ArrowDownUp],
  ["amm", "AMM simulator", Network],
] as const;
export default function StrategyLab() {
  const [params, setParams] = useSearchParams(),
    { state } = useWorkspace(),
    tool = params.get("tool") || "market",
    experiment = state.experiments.find(
      (e) => e.id === params.get("experiment"),
    );
  return (
    <div className="page lab-page">
      <div className="page-eyebrow">THE INTERACTIVE RESEARCH ENVIRONMENT</div>
      <div className="page-title-row">
        <div>
          <h1>
            {experiment?.title || "Ideas become clearer when you test them."}
          </h1>
          <p className="page-subtitle">
            Change an assumption. Run the numbers. Follow the evidence.
          </p>
        </div>
        <Link className="button secondary" to="/experiments">
          Saved experiments
          <ArrowUpRight size={15} />
        </Link>
      </div>
      <div className="lab-tabs tabs">
        {tabs.map(([id, label, Icon]) => (
          <button
            key={id}
            className={tool === id ? "active" : ""}
            onClick={() => setParams({ tool: id })}
          >
            <Icon size={16} />
            {label}
          </button>
        ))}
      </div>
      {tool === "valuation" ? (
        <ValuationLab />
      ) : tool === "amm" ? (
        <AmmLab />
      ) : tool === "broker" ? (
        <BrokerLab />
      ) : tool === "factors" ? (
        <FactorLab />
      ) : (
        <div className="market-lab-layout">
          <Sandbox
            key={experiment?.id || "free-lab"}
            initialCode={experiment?.code}
            initialConfig={experiment?.config}
            experimentId={experiment?.id}
          />
          <aside className="lab-guide">
            <span className="eyebrow">THE RESEARCH LOOP</span>
            <h2>Start with a question.</h2>
            <p>
              Does your idea survive a different market? A higher transaction
              cost? A new random seed?
            </p>
            {[
              [
                "01",
                "State a hypothesis",
                "Write a claim you can disprove. “A trend rule reduces drawdown in a persistent bear regime.”",
              ],
              [
                "02",
                "Change one assumption",
                "Choose a market process, set the parameters, and keep the seed fixed while comparing rules.",
              ],
              [
                "03",
                "Read the evidence",
                "Compare returns and risk with buy & hold. Account for costs, turnover, and failed trials.",
              ],
              [
                "04",
                "Keep a research trail",
                "Save the experiment and record what you learned in your notebook.",
              ],
            ].map(([n, title, body]) => (
              <div className="research-step" key={n}>
                <span>{n}</span>
                <div>
                  <h3>{title}</h3>
                  <p>{body}</p>
                </div>
              </div>
            ))}
            <div className="guide-note">
              <BookOpen size={18} />
              <p>
                Need the theory first?
                <Link to="/learn/3.5">
                  Read about backtest traps
                  <ArrowUpRight size={13} />
                </Link>
              </p>
            </div>
            <div className="lab-guide-data">
              <span className="green-dot" />
              <span>
                Default data is synthetic.
                <small>No market-data subscription needed.</small>
              </span>
            </div>
          </aside>
        </div>
      )}
    </div>
  );
}
