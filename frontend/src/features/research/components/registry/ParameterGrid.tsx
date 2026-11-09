import {
  NAME_PATTERN,
  newDraft,
  switchDraftMode,
  type GridDraft,
  type GridResolution,
  type GridRow,
} from "@/features/research/model/grid";
import type { ResearchOptions } from "@/features/research/model/registry";
import { Plus, Trash2, TriangleAlert } from "lucide-react";
import { FieldMessage, messageProps, Segmented } from "./fields";

type Limits = ResearchOptions["limits"];

function ConfigurationCounter({
  grid,
  limit,
}: {
  grid: GridResolution;
  limit: number;
}) {
  const over = grid.complete && grid.count > limit;
  const share = grid.complete ? Math.min(1, grid.count / limit) : 0;
  return (
    <div
      className={`registry-counter${over ? " is-over" : ""}`}
      role="status"
      aria-live="polite"
    >
      <span>
        <strong className="mono">{grid.complete ? grid.count : "—"}</strong>{" "}
        {grid.count === 1 && grid.complete ? "configuration" : "configurations"}{" "}
        <small>(limit {limit})</small>
      </span>
      <span className="registry-meter" aria-hidden="true">
        <span style={{ width: `${share * 100}%` }} />
      </span>
      <small className="mono">
        {grid.rows.length > 1 && grid.complete
          ? grid.rows.map((row) => row.values.length).join(" × ")
          : grid.complete
            ? over
              ? "Over the limit"
              : "Each one is a trial"
            : "Fix the values below"}
      </small>
    </div>
  );
}

function GridRowEditor({
  draft,
  index,
  row,
  issues,
  revealed,
  limits,
  onChange,
  onRemove,
}: {
  draft: GridDraft;
  index: number;
  row: GridRow;
  issues: Record<string, string>;
  revealed: boolean;
  limits: Limits;
  onChange: (draft: GridDraft) => void;
  onRemove: () => void;
}) {
  const prefix = `composer-${draft.id}`;
  // A freshly added blank row shows hints, not errors, until it is submitted.
  const blank = !draft.name && !draft.list && !draft.from && !draft.to;
  const show = revealed || !blank;
  const nameError = show ? issues[`grid:${draft.id}:name`] : undefined;
  const valuesError = show ? issues[`grid:${draft.id}:values`] : undefined;
  const set = (patch: Partial<GridDraft>) => onChange({ ...draft, ...patch });
  const name = draft.name.trim();
  const rangeInput = (key: "from" | "to" | "step", label: string) => (
    <div className="field registry-field">
      <label htmlFor={`${prefix}-${key}`}>{label}</label>
      <input
        id={`${prefix}-${key}`}
        className="mono"
        type="number"
        step="any"
        value={draft[key]}
        aria-invalid={valuesError ? true : undefined}
        aria-describedby={`${prefix}-values-message`}
        onChange={(event) => set({ [key]: event.target.value })}
      />
    </div>
  );
  return (
    <fieldset className="registry-grid-row">
      <legend className="sr-only">
        Parameter {index + 1}
        {name ? ` · ${name}` : ""}
      </legend>
      <div className="registry-grid-row-head">
        <span aria-hidden="true">
          Parameter {index + 1}
          {name ? <span className="mono"> · {name}</span> : null}
        </span>
        <Segmented
          name={`${prefix}-mode`}
          legend="Enter values as"
          hideLegend
          value={draft.mode}
          options={[
            { value: "list", label: "List" },
            { value: "range", label: "Range" },
          ]}
          onChange={(mode) =>
            onChange(switchDraftMode(draft, mode, limits.values))
          }
        />
        <button
          type="button"
          className="icon-button"
          aria-label={`Remove parameter ${index + 1}${name ? ` (${name})` : ""}`}
          title="Remove parameter"
          onClick={onRemove}
        >
          <Trash2 size={15} />
        </button>
      </div>
      <div className="registry-grid-fields">
        <div
          className={`field registry-field registry-grid-name${nameError ? " has-error" : ""}`}
        >
          <label htmlFor={`${prefix}-name`}>Name</label>
          <input
            id={`${prefix}-name`}
            className="mono"
            value={draft.name}
            placeholder="lookback"
            maxLength={24}
            autoCapitalize="off"
            autoCorrect="off"
            autoComplete="off"
            spellCheck={false}
            {...messageProps(`${prefix}-name`, nameError, "params[name]")}
            onChange={(event) => set({ name: event.target.value })}
          />
          <FieldMessage
            id={`${prefix}-name`}
            error={nameError}
            hint={<code>params["{name || "name"}"]</code>}
          />
        </div>
        {draft.mode === "list" ? (
          <div
            className={`field registry-field registry-grid-values${valuesError ? " has-error" : ""}`}
          >
            <label htmlFor={`${prefix}-list`}>Values</label>
            <input
              id={`${prefix}-list`}
              className="mono"
              value={draft.list}
              placeholder="20, 40, 60"
              autoComplete="off"
              spellCheck={false}
              aria-invalid={valuesError ? true : undefined}
              aria-describedby={`${prefix}-values-message`}
              onChange={(event) => set({ list: event.target.value })}
            />
          </div>
        ) : (
          <div className="registry-grid-values registry-grid-range">
            {rangeInput("from", "From")}
            {rangeInput("to", "To")}
            {rangeInput("step", "Step")}
          </div>
        )}
        <div className="field registry-field registry-grid-base">
          <label htmlFor={`${prefix}-base`}>Base value</label>
          <select
            id={`${prefix}-base`}
            className="mono"
            value={row.base === null ? "" : String(row.base)}
            disabled={!row.values.length}
            onChange={(event) => set({ base: Number(event.target.value) })}
          >
            {row.values.length ? (
              row.values.map((value) => (
                <option key={value} value={String(value)}>
                  {value}
                </option>
              ))
            ) : (
              <option value="">—</option>
            )}
          </select>
        </div>
      </div>
      <p
        className={valuesError ? "registry-error" : "registry-grid-preview"}
        id={`${prefix}-values-message`}
      >
        {valuesError ? (
          valuesError
        ) : row.values.length ? (
          <>
            <span>
              {row.values.length} {row.values.length === 1 ? "value" : "values"}
            </span>
            {row.values.map((value) => (
              <span
                key={value}
                className={`mono${value === row.base ? " is-base" : ""}`}
              >
                {value}
                {value === row.base ? (
                  <span className="sr-only"> (base)</span>
                ) : null}
              </span>
            ))}
          </>
        ) : (
          `Enter up to ${limits.values} values, or a range.`
        )}
      </p>
    </fieldset>
  );
}

export function ParameterGrid({
  drafts,
  grid,
  limits,
  issues,
  revealed,
  referenced,
  arity,
  onChange,
}: {
  drafts: GridDraft[];
  grid: GridResolution;
  limits: Limits;
  issues: Record<string, string>;
  revealed: boolean;
  referenced: string[];
  arity: number | null;
  onChange: (drafts: GridDraft[]) => void;
}) {
  const names = drafts.map((draft) => draft.name.trim());
  const twoArguments = arity !== null && arity >= 2;
  const missing = twoArguments
    ? referenced.filter((name) => !names.includes(name))
    : [];
  const unread = twoArguments
    ? names.filter(
        (name) => NAME_PATTERN.test(name) && !referenced.includes(name),
      )
    : [];
  const full = drafts.length >= limits.parameters;
  return (
    <div className="registry-grid" id="composer-grid" tabIndex={-1}>
      <div className="registry-grid-head">
        <div>
          <h3>Parameter grid</h3>
          <p>
            Every combination runs as its own configuration and counts as a
            trial. The base value is the setting you would choose without the
            grid; the red team compares it with the best and its neighbours.
          </p>
        </div>
        <ConfigurationCounter grid={grid} limit={limits.configurations} />
      </div>
      {drafts.length ? null : (
        <p className="registry-grid-empty">
          No parameters: the strategy runs once, as written. Checks that compare
          configurations, such as parameter stability and the probability of
          backtest overfitting, will be skipped.
        </p>
      )}
      {drafts.map((draft, index) => (
        <GridRowEditor
          key={draft.id}
          draft={draft}
          index={index}
          row={grid.rows[index]}
          issues={issues}
          revealed={revealed}
          limits={limits}
          onChange={(next) =>
            onChange(drafts.map((d) => (d.id === draft.id ? next : d)))
          }
          onRemove={() => onChange(drafts.filter((d) => d.id !== draft.id))}
        />
      ))}
      {issues.arity ? (
        <p
          className="registry-error registry-block-error"
          data-issue="arity"
          tabIndex={-1}
        >
          {issues.arity}{" "}
          <button
            type="button"
            className="text-link"
            onClick={() => onChange([])}
          >
            Remove the parameters
          </button>
        </p>
      ) : null}
      {issues.grid ? (
        <p
          className="registry-error registry-block-error"
          data-issue="grid"
          tabIndex={-1}
        >
          {issues.grid}
        </p>
      ) : null}
      {missing.length || unread.length ? (
        <ul className="registry-warnings">
          {missing.map((name) => (
            <li key={`missing-${name}`}>
              <TriangleAlert size={14} aria-hidden="true" />
              <span>
                The code reads <code>params["{name}"]</code>, which has no row
                in the grid.
              </span>
              {full ? null : (
                <button
                  type="button"
                  className="text-link"
                  onClick={() => onChange([...drafts, { ...newDraft(), name }])}
                >
                  Add {name}
                </button>
              )}
            </li>
          ))}
          {unread.map((name) => (
            <li key={`unread-${name}`}>
              <TriangleAlert size={14} aria-hidden="true" />
              <span>
                The code never reads <code>params["{name}"]</code>. Its values
                multiply the trials without changing the strategy.
              </span>
            </li>
          ))}
        </ul>
      ) : null}
      <div className="registry-grid-foot">
        <button
          type="button"
          className="button secondary small"
          disabled={full}
          onClick={() => onChange([...drafts, newDraft()])}
        >
          <Plus size={14} />
          Add parameter
        </button>
        <span className="registry-hint">
          {drafts.length} of {limits.parameters} parameters · up to{" "}
          {limits.values} values each
        </span>
      </div>
    </div>
  );
}
