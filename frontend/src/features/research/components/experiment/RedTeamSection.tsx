import type { RandomTiming, Results } from "@/features/research/model/registry";
import {
  CHECK_STATUS,
  formatCount,
  formatDay,
  formatNumber,
  formatPValue,
  isSkipped,
  niceScale,
  position,
  riskTone,
} from "@/features/research/model/experiment";
import { decimal, percent } from "@/shared/lib/format";
import { BookOpen } from "lucide-react";
import { memo } from "react";
import { Link } from "react-router-dom";
import {
  ChartLegend,
  SectionHeading,
  SkippedNote,
  Stat,
  StatusBadge,
  ToneIcon,
} from "./ui";

type Timing = Exclude<RandomTiming, { status: "skipped" | "undefined" }>;

/** The actual Sharpe against the random-timing null distribution's 5–95% band. */
function NullBand({ timing }: { timing: Timing }) {
  const { domain } = niceScale(
    [
      timing.null_p05,
      timing.null_p95,
      timing.null_median,
      timing.actual_sharpe,
    ],
    4,
  );
  const at = (value: number) => `${position(value, domain)}%`;
  const low = timing.null_p05,
    high = timing.null_p95;
  return (
    <figure className="xd-figure" aria-labelledby="timing-caption">
      <ChartLegend
        items={[
          { label: "Random timing, 5–95%", tone: "context", mark: "bar" },
          { label: "Random-timing median", tone: "context", mark: "tick" },
          { label: "Actual Sharpe", tone: "strategy", mark: "dot" },
        ]}
      />
      <div className="xd-band" aria-hidden="true">
        <span className="xd-track-zero" style={{ left: at(0) }} />
        {low != null && high != null ? (
          <span
            className="xd-band-range"
            style={{
              left: at(low),
              width: `${position(high, domain) - position(low, domain)}%`,
            }}
          />
        ) : null}
        {timing.null_median != null ? (
          <span
            className="xd-band-median"
            style={{ left: at(timing.null_median) }}
          />
        ) : null}
        <span
          className="xd-dot is-strategy"
          style={{ left: at(timing.actual_sharpe) }}
        />
      </div>
      <div className="xd-band-axis" aria-hidden="true">
        <span style={{ left: 0 }}>{formatNumber(domain[0])}</span>
        {position(0, domain) > 12 && position(0, domain) < 88 ? (
          <span className="is-zero" style={{ left: at(0) }}>
            0
          </span>
        ) : null}
        <span className="is-end" style={{ right: 0 }}>
          {formatNumber(domain[1])}
        </span>
      </div>
      <figcaption id="timing-caption" className="xd-figcaption">
        Actual Sharpe {decimal(timing.actual_sharpe)} is above{" "}
        {percent(timing.percentile, 0)} of {formatCount(timing.permutations)}{" "}
        runs with the same number of trades at random times. The null band runs
        from {decimal(low)} to {decimal(high)} (median{" "}
        {decimal(timing.null_median)}).
      </figcaption>
    </figure>
  );
}

export const RedTeamSection = memo(function RedTeamSection({
  results,
}: {
  results: Results;
}) {
  const { checks, risk } = results.redteam;
  const {
    trials,
    deflated_sharpe: dsr,
    pbo,
    random_timing: timing,
    concentration,
  } = results.diagnostics;
  const quality = results.dataset.quality;
  return (
    <section
      id="red-team"
      className="xd-section"
      aria-labelledby="red-team-title"
    >
      <SectionHeading
        id="red-team"
        eyebrow="RESEARCH RED TEAM"
        title="We tried to break it"
        description="Each check attacks one way a backtest can mislead. Research risk summarises what survived; it is not a forecast and not investment advice."
      />
      <div className="xd-card xd-risk">
        <StatusBadge
          tone={riskTone(risk.level)}
          size="large"
          label={`Research risk: ${risk.level}`}
        />
        <ul className="xd-risk-counts" aria-label="Check results">
          <li>
            <ToneIcon tone="pass" />
            <strong>{risk.passed}</strong> passed
          </li>
          <li>
            <ToneIcon tone="warn" />
            <strong>{risk.warnings}</strong>{" "}
            {risk.warnings === 1 ? "warning" : "warnings"}
            {risk.high ? ` (${risk.high} high)` : ""}
          </li>
          <li>
            <ToneIcon tone="fail" />
            <strong>{risk.failed}</strong> failed
          </li>
          <li>
            <ToneIcon tone="neutral" />
            <strong>{risk.skipped}</strong> not applicable
          </li>
        </ul>
      </div>
      <ul className="xd-checks">
        {checks.map((check) => {
          const meta = CHECK_STATUS[check.status];
          return (
            <li key={check.id} className={`xd-check is-${meta.tone}`}>
              <ToneIcon tone={meta.tone} size={18} />
              <div>
                <div className="xd-check-head">
                  <h3>{check.title}</h3>
                  <span className={`xd-check-status is-${meta.tone}`}>
                    {meta.label}
                  </span>
                  {check.status === "warn" && check.severity ? (
                    <span className={`xd-severity is-${check.severity}`}>
                      {check.severity} severity
                    </span>
                  ) : null}
                </div>
                <p>{check.finding}</p>
                {check.lesson ? (
                  <Link
                    className="text-link xd-learn"
                    to={`/learn/${check.lesson}`}
                  >
                    <BookOpen size={14} aria-hidden="true" />
                    Learn why · lesson {check.lesson}
                    <span className="sr-only">: {check.title}</span>
                  </Link>
                ) : null}
              </div>
            </li>
          );
        })}
      </ul>
      <div className="xd-grid-2">
        <div className="xd-card">
          <div className="xd-card-head">
            <h3>Deflated Sharpe ratio</h3>
          </div>
          {isSkipped(dsr) ? (
            <SkippedNote value={dsr} />
          ) : (
            <>
              <div className="xd-kpis xd-kpis-compact">
                <Stat
                  label="Deflated Sharpe"
                  value={percent(dsr.dsr, 0)}
                  sub={`Edge beats the luck of ${formatCount(dsr.trials)} trials`}
                />
                <Stat
                  label="Probabilistic Sharpe"
                  value={percent(dsr.psr, 0)}
                  sub="True Sharpe above zero, before trials"
                />
                <Stat
                  label="Best Sharpe from luck"
                  value={decimal(dsr.expected_max_sharpe)}
                  sub={`Observed ${decimal(dsr.sharpe)}`}
                />
              </div>
              <dl className="xd-pairs">
                <div>
                  <dt>Trials counted</dt>
                  <dd>{formatCount(dsr.trials)}</dd>
                </div>
                <div>
                  <dt>This run</dt>
                  <dd>{formatCount(trials.run)} configurations</dd>
                </div>
                <div>
                  <dt>All runs of this strategy</dt>
                  <dd>
                    {formatCount(trials.strategy_configurations)} configurations
                  </dd>
                </div>
              </dl>
              <p className="fine-print">
                Every configuration ever tried counts, across reruns and edits:
                the more you search, the higher the best Sharpe you should
                expect from luck alone. {formatCount(dsr.observations)}{" "}
                observations · skew {decimal(dsr.skewness)} · kurtosis{" "}
                {decimal(dsr.kurtosis)}.
              </p>
            </>
          )}
        </div>
        <div className="xd-card">
          <div className="xd-card-head">
            <h3>Probability of backtest overfitting</h3>
          </div>
          {isSkipped(pbo) ? (
            <SkippedNote value={pbo} />
          ) : (
            <>
              <div className="xd-kpis xd-kpis-compact">
                <Stat
                  label="PBO"
                  value={percent(pbo.pbo, 0)}
                  sub="In-sample winner below the median out of sample"
                />
                <Stat
                  label="Below risk-free"
                  value={percent(pbo.oos_below_risk_free, 0)}
                  sub="Splits where the in-sample winner lost to cash"
                />
                <Stat
                  label="Median Sharpe"
                  value={`${decimal(pbo.in_sample_sharpe_median)} → ${decimal(pbo.out_of_sample_sharpe_median)}`}
                  sub="In sample → out of sample"
                />
              </div>
              <p className="fine-print">
                Combinatorially symmetric cross-validation:{" "}
                {formatCount(pbo.blocks)} blocks give{" "}
                {formatCount(pbo.combinations)} train/test splits over{" "}
                {formatCount(pbo.configurations)} configurations. Median logit{" "}
                {decimal(pbo.median_logit)}.
              </p>
            </>
          )}
        </div>
        <div className="xd-card">
          <div className="xd-card-head">
            <h3>Random-timing test</h3>
            {!isSkipped(timing) ? (
              <p className="xd-hint">
                p = {formatPValue(timing.p_value)} · seed {timing.seed}
              </p>
            ) : null}
          </div>
          {isSkipped(timing) ? (
            <SkippedNote value={timing} />
          ) : (
            <>
              <div className="xd-kpis xd-kpis-compact">
                <Stat label="p-value" value={formatPValue(timing.p_value)} />
                <Stat
                  label="Percentile"
                  value={percent(timing.percentile, 0)}
                  sub="of random-timing runs beaten"
                />
              </div>
              <NullBand timing={timing} />
            </>
          )}
        </div>
        <div className="xd-card">
          <div className="xd-card-head">
            <h3>Concentration</h3>
          </div>
          {isSkipped(concentration) ? (
            <SkippedNote value={concentration} />
          ) : (
            <>
              <div className="xd-kpis xd-kpis-compact">
                <Stat
                  label="Best year share"
                  value={percent(concentration.share, 0)}
                  sub={`${concentration.best_year} of total profit`}
                />
                <Stat
                  label="Losing years"
                  value={`${concentration.losing_years} / ${concentration.years}`}
                />
              </div>
              <p className="fine-print">
                If one year makes most of the profit, the result may be one
                event rather than a repeatable edge.
              </p>
            </>
          )}
        </div>
        <div className="xd-card">
          <div className="xd-card-head">
            <h3>Look-ahead test</h3>
            <StatusBadge
              tone={results.lookahead.status === "pass" ? "pass" : "fail"}
              label={
                results.lookahead.status === "pass"
                  ? "No look-ahead"
                  : "Look-ahead detected"
              }
            />
          </div>
          <p className="xd-hint">
            The strategy is rerun on data truncated at each cut. Signals up to
            the cut must not change when the future is removed.
          </p>
          <div className="table-scroll xd-table xd-table-full">
            <table>
              <caption className="sr-only">Look-ahead truncation cuts</caption>
              <thead>
                <tr>
                  <th scope="col">Cut</th>
                  <th scope="col">Date</th>
                  <th scope="col">Result</th>
                </tr>
              </thead>
              <tbody>
                {results.lookahead.checks.map((cut) => (
                  <tr key={`${cut.bars}-${cut.time}`}>
                    <th scope="row">{formatCount(cut.bars)} bars</th>
                    <td>{formatDay(cut.time)}</td>
                    <td className="xd-wrap">
                      {cut.error ? (
                        <StatusBadge
                          tone="fail"
                          label={`Error: ${cut.error}`}
                        />
                      ) : cut.match ? (
                        <StatusBadge tone="pass" label="Signals match" />
                      ) : (
                        <StatusBadge
                          tone="fail"
                          label={`Differs${cut.first_difference ? ` from ${formatDay(cut.first_difference)}` : ""}`}
                        />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
        <div className="xd-card">
          <div className="xd-card-head">
            <h3>Data integrity</h3>
            <StatusBadge
              tone={quality.issues ? "warn" : "pass"}
              label={
                quality.issues
                  ? `${quality.issues} ${quality.issues === 1 ? "issue" : "issues"}`
                  : "No issues"
              }
            />
          </div>
          <ul className="xd-quality-checks">
            {quality.checks.map((check) => {
              const tone =
                check.status === "pass"
                  ? "pass"
                  : check.status === "warn"
                    ? "warn"
                    : "neutral";
              return (
                <li key={check.id}>
                  <ToneIcon tone={tone} />
                  <div>
                    <strong>{check.label}</strong>
                    <span className="sr-only">
                      {" "}
                      (
                      {check.status === "info"
                        ? "information"
                        : check.status === "pass"
                          ? "passed"
                          : "warning"}
                      )
                    </span>
                    {check.detail ? <p>{check.detail}</p> : null}
                  </div>
                </li>
              );
            })}
          </ul>
        </div>
      </div>
    </section>
  );
});
