"""Full Python worker: only run inside the isolated, ephemeral sandbox image.
The container boundary is the security boundary. AST checks reduce accidental
misuse; they are not a substitute for kernel/container isolation.
"""

import ast
import builtins
import io
import json
import signal
import sys
from contextlib import redirect_stderr, redirect_stdout

import numpy as np
import pandas as pd

ALLOWED = {"math", "statistics", "numpy", "pandas", "polars", "scipy", "statsmodels"}


def limited_import(name, globals=None, locals=None, fromlist=(), level=0):
    if level or name.split(".")[0] not in ALLOWED:
        raise ValueError("This library is unavailable in the sandbox.")
    return builtins.__import__(name, globals, locals, fromlist, level)


class CappedOutput(io.StringIO):
    def write(self, value):
        if self.tell() + len(value) > 20000:
            raise ValueError("Output exceeds 20 KB.")
        return super().write(value)


def timeout(*args):
    raise TimeoutError("Python execution exceeded two seconds.")


def _series(values):
    return pd.Series(values, dtype=float)


def _window(n, minimum=1):
    if (
        isinstance(n, bool)
        or not isinstance(n, (int, float))
        or not minimum <= n <= 10000
        or not float(n).is_integer()
    ):
        raise ValueError(f"Windows must be whole numbers from {minimum} to 10,000.")
    return int(n)


def _shift(values, n):
    if n < 0:
        raise ValueError(
            "shift() only looks back: a negative lag would read bars that have not happened yet."
        )
    s = _series(values)
    return s.shift(_window(n, minimum=0)).fillna(s.iloc[0])


def _change(values, n):
    earlier = _shift(values, _window(n))
    if (earlier == 0).any():
        raise ValueError("change() divides by an earlier value of zero.")
    return _series(values) / earlier - 1


def _zscore(values, n):
    s = _series(values)
    deviation = s.rolling(_window(n), min_periods=1).std(ddof=0)
    score = (s - s.rolling(_window(n), min_periods=1).mean()) / deviation
    return score.where(deviation > 1e-12, 0.0)


# The guided runtime's trailing-window indicators, with the same warm-up rule:
# the first bars use the observations available so far.
INDICATORS = {
    "sma": lambda v, n: _series(v).rolling(_window(n), min_periods=1).mean(),
    "ema": lambda v, n: _series(v).ewm(span=_window(n), adjust=False).mean(),
    "highest": lambda v, n: _series(v).rolling(_window(n), min_periods=1).max(),
    "lowest": lambda v, n: _series(v).rolling(_window(n), min_periods=1).min(),
    "change": lambda v, n: _change(v, n),
    "shift": _shift,
    "stdev": lambda v, n: _series(v).rolling(_window(n), min_periods=1).std(ddof=0).fillna(0.0),
    "zscore": _zscore,
}


def main():
    try:
        payload = json.loads(sys.stdin.read(3000000))
        code = payload["code"]
        if len(code) > 20000:
            raise ValueError("Code too large.")
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                modules = (
                    [a.name for a in node.names]
                    if isinstance(node, ast.Import)
                    else [node.module or ""]
                )
                if any(m.split(".")[0] not in ALLOWED for m in modules):
                    raise ValueError("Import is outside the scientific library allowlist.")
            if isinstance(node, ast.Attribute) and node.attr.startswith("_"):
                raise ValueError("Private attributes are unavailable.")
            if isinstance(node, ast.Name) and node.id.startswith("_"):
                raise ValueError("Private identifiers are unavailable.")
        safe = {
            name: getattr(builtins, name)
            for name in (
                "abs",
                "all",
                "any",
                "bool",
                "dict",
                "enumerate",
                "float",
                "int",
                "len",
                "list",
                "max",
                "min",
                "print",
                "range",
                "round",
                "set",
                "sorted",
                "str",
                "sum",
                "tuple",
                "zip",
                "Exception",
                "ValueError",
            )
        }
        safe["__import__"] = limited_import
        scope = {"__builtins__": safe, "np": np, "pd": pd, **INDICATORS}
        stdout, stderr = CappedOutput(), CappedOutput()
        signal.signal(signal.SIGALRM, timeout)
        signal.setitimer(signal.ITIMER_REAL, 2)
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compile(tree, "<student>", "exec"), scope)
            data = pd.DataFrame(payload["data"])
            strategy = scope["strategy"]
            arity = strategy.__code__.co_argcount
            if arity not in (1, 2):
                raise ValueError("Define strategy(data) or strategy(data, params).")
            params = dict(payload.get("params") or {})
            raw = strategy(data) if arity == 1 else strategy(data, params)
            signals = np.asarray(raw)
            if signals.ndim == 0:
                signals = np.repeat(signals, len(data))
            if signals.shape != (len(data),) or not np.isin(signals, [0, 1]).all():
                raise ValueError("Return one Boolean long/cash signal per bar.")
        signal.setitimer(signal.ITIMER_REAL, 0)
        result = {
            "signals": signals.astype(bool).tolist(),
            "stdout": stdout.getvalue(),
            "stderr": stderr.getvalue(),
            "arity": arity,
        }
    except BaseException as error:
        signal.setitimer(signal.ITIMER_REAL, 0)
        result = {"error": f"{type(error).__name__}: {str(error)[:500]}"}
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
