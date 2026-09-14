import { LockKeyhole, Trash2 } from "lucide-react";
import type { Candle, Drawing, DrawingKind } from "../../lib/simulator";
import { price } from "../../lib/simulator";
export default function DrawingsPanel({
  drawings,
  onChange,
  selected,
  onSelect,
  bars,
  disabled,
}: {
  drawings: Drawing[];
  onChange: (d: Drawing[]) => void;
  selected: string | null;
  onSelect: (id: string | null) => void;
  bars: Candle[];
  disabled: boolean;
}) {
  const item = drawings.find((d) => d.id === selected);
  const edit = (change: Partial<Drawing>) => {
    if (item)
      onChange(
        drawings.map((d) => (d.id === item.id ? { ...d, ...change } : d)),
      );
  };
  const add = (kind: DrawingKind) => {
    const first = bars.at(-30) ?? bars[0],
      last = bars.at(-1);
    if (!first || !last) return;
    const d: Drawing = {
      id: crypto.randomUUID(),
      kind,
      t1: first.time,
      t2: last.time,
      p1: first.close,
      p2: last.close,
      text: kind === "text" ? "Chart note" : "",
      color: "#668de8",
      locked: false,
    };
    onChange([...drawings, d]);
    onSelect(d.id);
  };
  return (
    <section className="sim-drawings-panel" aria-label="Drawing manager">
      <div className="sim-section-title">
        <strong>Drawing objects</strong>
        <span>{drawings.length}</span>
      </div>
      <label className="sim-field">
        Add drawing with form
        <select
          value=""
          disabled={disabled}
          onChange={(e) => add(e.target.value as DrawingKind)}
        >
          <option value="" disabled>
            Choose a drawing…
          </option>
          <option value="trend">Trend line</option>
          <option value="horizontal">Horizontal line</option>
          <option value="rectangle">Rectangle</option>
          <option value="text">Text annotation</option>
          <option value="measure">Price measurement</option>
        </select>
      </label>
      <div className="sim-object-list">
        {drawings.map((d) => (
          <button
            key={d.id}
            className={selected === d.id ? "selected" : ""}
            onClick={() => onSelect(d.id)}
          >
            {d.locked ? <LockKeyhole size={12} /> : null}
            {d.text || d.kind.replace("_", " ")}
            <span>{price(d.p1)}</span>
          </button>
        ))}
      </div>
      {item ? (
        <fieldset disabled={disabled} className="sim-drawing-form">
          <label className="sim-field">
            Drawing label
            <input
              value={item.text}
              maxLength={100}
              onChange={(e) => edit({ text: e.target.value })}
              disabled={item.locked}
            />
          </label>
          <div className="sim-field-pair">
            <label className="sim-field">
              First price
              <input
                type="number"
                step="0.01"
                min="0.01"
                value={item.p1}
                onChange={(e) => {
                  if (Number(e.target.value) > 0)
                    edit({ p1: Number(e.target.value) });
                }}
                disabled={item.locked}
              />
            </label>
            {item.kind !== "horizontal" && item.kind !== "text" ? (
              <label className="sim-field">
                Second price
                <input
                  type="number"
                  step="0.01"
                  min="0.01"
                  value={item.p2}
                  onChange={(e) => {
                    if (Number(e.target.value) > 0)
                      edit({ p2: Number(e.target.value) });
                  }}
                  disabled={item.locked}
                />
              </label>
            ) : null}
          </div>
          <label className="sim-field">
            First time
            <select
              value={item.t1}
              onChange={(e) => edit({ t1: Number(e.target.value) })}
              disabled={item.locked}
            >
              {bars.map((b) => (
                <option key={b.time} value={b.time}>
                  {new Date(b.time * 1000)
                    .toISOString()
                    .slice(0, 16)
                    .replace("T", " ")}{" "}
                  UTC
                </option>
              ))}
            </select>
          </label>
          {item.kind !== "horizontal" && item.kind !== "text" ? (
            <label className="sim-field">
              Second time
              <select
                value={item.t2}
                onChange={(e) => edit({ t2: Number(e.target.value) })}
                disabled={item.locked}
              >
                {bars.map((b) => (
                  <option key={b.time} value={b.time}>
                    {new Date(b.time * 1000)
                      .toISOString()
                      .slice(0, 16)
                      .replace("T", " ")}{" "}
                    UTC
                  </option>
                ))}
              </select>
            </label>
          ) : null}
          <label className="sim-field">
            Drawing color
            <input
              type="color"
              value={item.color}
              onChange={(e) => edit({ color: e.target.value })}
              disabled={item.locked}
            />
          </label>
          <label className="sim-checkbox">
            <input
              type="checkbox"
              checked={item.locked}
              onChange={(e) => edit({ locked: e.target.checked })}
            />{" "}
            Lock drawing
          </label>
          <button
            className="sim-outline"
            disabled={item.locked}
            onClick={() => {
              onChange(drawings.filter((d) => d.id !== item.id));
              onSelect(null);
            }}
          >
            <Trash2 size={14} /> Delete drawing
          </button>
        </fieldset>
      ) : (
        <p className="sim-small">
          Select a drawing to edit its prices, dates, label, and lock. Drag
          unlocked objects directly on the chart.
        </p>
      )}
    </section>
  );
}
