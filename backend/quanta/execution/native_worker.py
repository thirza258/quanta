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
        scope = {"__builtins__": safe, "np": np, "pd": pd}
        stdout, stderr = CappedOutput(), CappedOutput()
        signal.signal(signal.SIGALRM, timeout)
        signal.setitimer(signal.ITIMER_REAL, 2)
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compile(tree, "<student>", "exec"), scope)
            data = pd.DataFrame(payload["data"])
            raw = scope["strategy"](data)
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
        }
    except BaseException as error:
        signal.setitimer(signal.ITIMER_REAL, 0)
        result = {"error": f"{type(error).__name__}: {str(error)[:500]}"}
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
