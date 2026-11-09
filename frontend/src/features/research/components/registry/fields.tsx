// Small form controls shared by the experiment composer's sections.
import { tidy, type NumberRule } from "@/features/research/model/grid";
import { useState, type ReactNode } from "react";

/** An error (when present) or a hint under a field, linked by id. */
export function FieldMessage({
  id,
  error,
  hint,
}: {
  id: string;
  error?: string;
  hint?: ReactNode;
}) {
  if (error)
    return (
      <span className="registry-error" id={`${id}-message`}>
        {error}
      </span>
    );
  return hint ? (
    <span className="registry-hint" id={`${id}-message`}>
      {hint}
    </span>
  ) : null;
}

export const messageProps = (id: string, error?: string, hint?: ReactNode) => ({
  "aria-invalid": error ? true : undefined,
  "aria-describedby": error || hint ? `${id}-message` : undefined,
});

/**
 * A number input that keeps what is typed (an empty box, a lone minus sign)
 * while reporting NaN upward, so validation can explain the problem instead of
 * silently replacing it with zero. `rule.scale` shows fractions as percentages.
 */
export function NumberField({
  id,
  label,
  value,
  onChange,
  rule,
  suffix,
  hint,
  error,
  disabled,
  step,
}: {
  id: string;
  label: ReactNode;
  value: number;
  onChange: (value: number) => void;
  rule: NumberRule;
  suffix?: string;
  hint?: ReactNode;
  error?: string;
  disabled?: boolean;
  step?: number;
}) {
  const scale = rule.scale ?? 1;
  const show = (v: number) =>
    Number.isFinite(v) ? String(tidy(v * scale)) : "";
  const read = (text: string) => (text.trim() ? Number(text) / scale : NaN);
  const [text, setText] = useState(() => show(value));
  const [seen, setSeen] = useState(value);
  if (!Object.is(seen, value)) {
    // The value changed from outside (a template, a reset): show it.
    setSeen(value);
    if (!Object.is(read(text), value)) setText(show(value));
  }
  return (
    <div className={`field registry-field${error ? " has-error" : ""}`}>
      <label htmlFor={id}>{label}</label>
      <span className="registry-unit">
        <input
          id={id}
          type="number"
          min={rule.above ? undefined : rule.min * scale}
          max={rule.max * scale}
          step={step ?? (rule.integer ? 1 : "any")}
          value={text}
          disabled={disabled}
          {...messageProps(id, error, hint)}
          onChange={(event) => {
            setText(event.target.value);
            onChange(read(event.target.value));
          }}
        />
        {suffix ? <span aria-hidden="true">{suffix}</span> : null}
      </span>
      <FieldMessage id={id} error={error} hint={hint} />
    </div>
  );
}

export function SelectField({
  id,
  label,
  value,
  onChange,
  options,
  hint,
  error,
  disabled,
  placeholder,
}: {
  id: string;
  label: ReactNode;
  value: string;
  onChange: (value: string) => void;
  options: { id: string; label: string }[];
  hint?: ReactNode;
  error?: string;
  disabled?: boolean;
  placeholder?: string;
}) {
  return (
    <div className={`field registry-field${error ? " has-error" : ""}`}>
      <label htmlFor={id}>{label}</label>
      <select
        id={id}
        value={value}
        disabled={disabled}
        {...messageProps(id, error, hint)}
        onChange={(event) => onChange(event.target.value)}
      >
        {placeholder ? <option value="">{placeholder}</option> : null}
        {options.map((option) => (
          <option key={option.id} value={option.id}>
            {option.label}
          </option>
        ))}
      </select>
      <FieldMessage id={id} error={error} hint={hint} />
    </div>
  );
}

/** Radio buttons drawn as a segmented control; arrow keys move between them. */
export function Segmented<T extends string>({
  name,
  legend,
  options,
  value,
  onChange,
  hideLegend,
  disabled,
}: {
  name: string;
  legend: string;
  options: { value: T; label: ReactNode }[];
  value: T;
  onChange: (value: T) => void;
  hideLegend?: boolean;
  disabled?: boolean;
}) {
  return (
    <fieldset className="registry-segmented" disabled={disabled}>
      <legend className={hideLegend ? "sr-only" : undefined}>{legend}</legend>
      <div>
        {options.map((option) => (
          <label
            key={option.value}
            className={option.value === value ? "active" : undefined}
          >
            <input
              className="sr-only"
              type="radio"
              name={name}
              value={option.value}
              checked={option.value === value}
              onChange={() => onChange(option.value)}
            />
            {option.label}
          </label>
        ))}
      </div>
    </fieldset>
  );
}

export function Switch({
  id,
  checked,
  onChange,
  label,
  description,
}: {
  id: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
  label: string;
  description?: string;
}) {
  return (
    <label className="registry-switch" htmlFor={id}>
      <input
        id={id}
        type="checkbox"
        role="switch"
        checked={checked}
        aria-describedby={description ? `${id}-description` : undefined}
        onChange={(event) => onChange(event.target.checked)}
      />
      <span className="registry-switch-track" aria-hidden="true" />
      <span>
        <strong>{label}</strong>
        {description ? (
          <small id={`${id}-description`}>{description}</small>
        ) : null}
      </span>
    </label>
  );
}

export function ComposerSection({
  id,
  step,
  title,
  description,
  children,
}: {
  id: string;
  step: number;
  title: string;
  description: ReactNode;
  children: ReactNode;
}) {
  return (
    <section
      className="registry-section"
      id={id}
      aria-labelledby={`${id}-title`}
    >
      <header className="registry-section-head">
        <span className="registry-step mono" aria-hidden="true">
          {step}
        </span>
        <div>
          <h2 id={`${id}-title`} tabIndex={-1}>
            {title}
          </h2>
          <p>{description}</p>
        </div>
      </header>
      {children}
    </section>
  );
}
