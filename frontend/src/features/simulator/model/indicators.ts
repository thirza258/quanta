export function sma(values: number[], period: number): (number | null)[] {
  let sum = 0;
  return values.map((value, i) => {
    sum += value;
    if (i >= period) sum -= values[i - period];
    return i >= period - 1 ? sum / period : null;
  });
}

export function ema(values: number[], period: number): (number | null)[] {
  let previous: number | null = null;
  let sum = 0;
  const alpha = 2 / (period + 1);
  return values.map((v, i) => {
    sum += v;
    if (i < period - 1) return null;
    previous =
      previous === null ? sum / period : alpha * v + (1 - alpha) * previous;
    return previous;
  });
}

export function rsi(values: number[], period: number): (number | null)[] {
  let gain = 0,
    loss = 0;
  return values.map((v, i) => {
    if (i === 0) return null;
    const diff = v - values[i - 1];
    if (i <= period) {
      gain += Math.max(diff, 0) / period;
      loss += Math.max(-diff, 0) / period;
    } else {
      gain = (gain * (period - 1) + Math.max(diff, 0)) / period;
      loss = (loss * (period - 1) + Math.max(-diff, 0)) / period;
    }
    return i < period
      ? null
      : loss === 0
        ? gain === 0
          ? 50
          : 100
        : 100 - 100 / (1 + gain / loss);
  });
}

export function macd(
  values: number[],
  fast: number,
  slow: number,
  signal: number,
) {
  const a = ema(values, fast),
    b = ema(values, slow),
    line = a.map((v, i) => (v !== null && b[i] !== null ? v - b[i]! : null));
  const valid = line.filter((v): v is number => v !== null);
  const offset = line.length - valid.length;
  const sig = [
    ...Array<number | null>(offset).fill(null),
    ...ema(valid, signal),
  ];
  return {
    line,
    signal: sig,
    histogram: line.map((v, i) =>
      v !== null && sig[i] !== null ? v - sig[i]! : null,
    ),
  };
}
