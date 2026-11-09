import {
  newDraft,
  referencedParams,
  STRATEGY_NAME_MAX,
  strategyParams,
  type ComposerForm,
  type GridResolution,
} from "@/features/research/model/grid";
import type {
  ResearchOptions,
  StrategyTemplate,
} from "@/features/research/model/registry";
import { Loading, Modal } from "@/shared/components/ui";
import { Code2 } from "lucide-react";
import { lazy, Suspense, useState } from "react";
import { FieldMessage, messageProps } from "./fields";
import { IndicatorReference } from "./IndicatorReference";
import { ParameterGrid } from "./ParameterGrid";

const CodeEditor = lazy(() => import("@/shared/components/CodeEditor"));

type StrategyPatch = Partial<Pick<ComposerForm, "name" | "code" | "grid">>;

export function StrategyFields({
  form,
  grid,
  options,
  issues,
  revealed,
  onChange,
  onTouch,
}: {
  form: ComposerForm;
  grid: GridResolution;
  options: ResearchOptions;
  issues: Record<string, string>;
  revealed: boolean;
  onChange: (patch: StrategyPatch) => void;
  onTouch: (field: string) => void;
}) {
  const [pending, setPending] = useState<StrategyTemplate | null>(null);
  const { templates } = options;
  const declared = strategyParams(form.code);
  const referenced = referencedParams(form.code);
  const active = templates.find((template) => template.code === form.code);
  const name = form.name.trim();
  // Follow the template's name unless the user has chosen one.
  const namedByUser =
    !!name &&
    name !== options.defaults.strategy.name &&
    !templates.some((template) => template.label === name);
  const apply = (template: StrategyTemplate) => {
    onChange({
      code: template.code,
      grid: template.parameters.map((parameter) =>
        newDraft(parameter, template.base[parameter.name]),
      ),
      ...(namedByUser ? {} : { name: template.label }),
    });
    setPending(null);
  };
  const edited =
    !!form.code.trim() &&
    !templates.some((template) => template.code === form.code);
  const nameError = issues.name;
  const nameHint =
    "Code is versioned per name: new code under the same name becomes its next version.";
  const codeError = issues.code;
  return (
    <>
      <div
        className="registry-templates"
        role="group"
        aria-labelledby="composer-templates-label"
      >
        <span id="composer-templates-label" className="registry-label">
          Start from a template
        </span>
        <div>
          {templates.map((template) => (
            <button
              key={template.id}
              type="button"
              className={`registry-template${active?.id === template.id ? " active" : ""}`}
              aria-pressed={active?.id === template.id}
              onClick={() => (edited ? setPending(template) : apply(template))}
            >
              <strong>{template.label}</strong>
              <small>{template.description}</small>
              <span className="mono">
                {template.parameters.length
                  ? template.parameters
                      .map((p) => `${p.name} ×${p.values.length}`)
                      .join("  ")
                  : "no grid"}
              </span>
            </button>
          ))}
        </div>
      </div>
      <div className={`field registry-field${nameError ? " has-error" : ""}`}>
        <label htmlFor="composer-name">Strategy name</label>
        <input
          id="composer-name"
          value={form.name}
          maxLength={STRATEGY_NAME_MAX}
          autoComplete="off"
          {...messageProps("composer-name", nameError, nameHint)}
          onChange={(event) => onChange({ name: event.target.value })}
          onBlur={() => onTouch("name")}
        />
        <FieldMessage id="composer-name" error={nameError} hint={nameHint} />
      </div>
      <div
        className={`registry-editor${codeError ? " has-error" : ""}`}
        id="composer-code"
      >
        <div className="registry-editor-bar">
          <span className="mono">
            <Code2 size={14} aria-hidden="true" />
            strategy.py
          </span>
          <span
            className={`mono registry-signature${declared ? "" : " is-missing"}`}
          >
            {declared
              ? `strategy(${declared.join(", ")})${
                  declared.length > 1 && referenced.length
                    ? ` · reads ${referenced.join(", ")}`
                    : ""
                }`
              : "No def strategy(…) found"}
          </span>
        </div>
        <Suspense fallback={<Loading label="Loading Python editor…" />}>
          <CodeEditor
            code={form.code}
            onChange={(code) => onChange({ code })}
          />
        </Suspense>
      </div>
      {codeError ? (
        <p className="registry-error" data-issue="code" tabIndex={-1}>
          {codeError}
        </p>
      ) : (
        <p className="registry-hint registry-editor-note">
          Guided Python: <code>def strategy(data, params):</code> returns a
          true/false series of positions. With an empty grid,{" "}
          <code>strategy(data)</code> is enough.
        </p>
      )}
      <IndicatorReference indicators={options.indicators} />
      <ParameterGrid
        drafts={form.grid}
        grid={grid}
        limits={options.limits}
        issues={issues}
        revealed={revealed}
        referenced={referenced}
        arity={declared?.length ?? null}
        onChange={(drafts) => onChange({ grid: drafts })}
      />
      <Modal
        open={!!pending}
        onOpenChange={(open) => {
          if (!open) setPending(null);
        }}
        title="Replace your strategy code?"
        description={`“${pending?.label ?? "This template"}” replaces the code, the parameter grid and the base values. Your edits will be lost.`}
      >
        <div className="dialog-actions">
          <button
            type="button"
            className="button secondary"
            onClick={() => setPending(null)}
          >
            Keep my code
          </button>
          <button
            type="button"
            className="button primary"
            onClick={() => pending && apply(pending)}
          >
            Replace code
          </button>
        </div>
      </Modal>
    </>
  );
}
