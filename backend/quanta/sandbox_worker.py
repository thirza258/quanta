"""Capability-free interpreter for a documented Python subset; never eval/exec.

Runs in a fresh subprocess. Unsupported syntax fails closed. User attributes are
resolved from explicit maps, never Python getattr. Desktop mode intentionally
supports a subset; full scientific Python uses the optional Docker runner.
"""

import ast
import json
import math
import operator
import sys
import time

MAX_ITEMS = 10000
MAX_OPERATIONS = 750000


class SandboxError(Exception):
    pass


class Vector:
    def __init__(self, values):
        if len(values) > MAX_ITEMS:
            raise SandboxError("Series exceeds 10,000 observations.")
        self.values = list(values)


class Namespace:
    def __init__(self, members):
        self.members = members


class Function:
    def __init__(self, node, closure):
        self.node, self.closure = node, closure


class Returned(Exception):
    def __init__(self, value):
        self.value = value


class Interpreter:
    def __init__(self):
        self.fuel, self.depth = MAX_OPERATIONS, 0
        self.deadline = time.monotonic() + 1.75
        self.output = ""
        self.math = Namespace(
            {
                name: getattr(math, name)
                for name in (
                    "sqrt",
                    "log",
                    "exp",
                    "sin",
                    "cos",
                    "fabs",
                    "floor",
                    "ceil",
                    "pi",
                    "e",
                )
            }
        )
        self.numpy = Namespace(
            {
                "array": lambda a: Vector(a),
                "mean": self.mean,
                "std": self.std,
                "sqrt": lambda a: self.vector_unary(math.sqrt, a),
                "abs": lambda a: self.vector_unary(abs, a),
                "where": self.where,
            }
        )
        self.env = {
            "print": self.print,
            "round": round,
            "abs": lambda a: self.vector_unary(abs, a),
            "min": self.minimum,
            "max": self.maximum,
            "sum": self.total,
            "len": lambda a: len(self.sequence(a)),
            "range": self.range,
            "float": float,
            "int": int,
            "bool": bool,
        }

    def tick(self, count=1):
        self.fuel -= count
        if self.fuel < 0 or time.monotonic() > self.deadline:
            raise SandboxError(
                "Execution limit reached. Simplify the strategy or use fewer observations."
            )

    def sequence(self, value):
        return value.values if isinstance(value, Vector) else value

    def total(self, a):
        return sum(self.sequence(a))

    def minimum(self, *a):
        return min(self.sequence(a[0])) if len(a) == 1 else min(a)

    def maximum(self, *a):
        return max(self.sequence(a[0])) if len(a) == 1 else max(a)

    def mean(self, a):
        a = self.sequence(a)
        return sum(a) / len(a)

    def std(self, a):
        a = self.sequence(a)
        mean = sum(a) / len(a)
        return math.sqrt(sum((x - mean) ** 2 for x in a) / len(a))

    def range(self, *args):
        result = range(*args)
        if len(result) > MAX_ITEMS:
            raise SandboxError("range() is limited to 10,000 items.")
        return list(result)

    def print(self, *args):
        value = " ".join(str(self.sequence(x)) for x in args) + "\n"
        if len(self.output) + len(value) > 20000:
            raise SandboxError("Output limit exceeded (20 KB).")
        self.output += value

    def vector_unary(self, fn, a):
        if isinstance(a, Vector):
            self.tick(len(a.values))
            return Vector([fn(x) for x in a.values])
        return fn(a)

    def where(self, condition, a, b):
        if not isinstance(condition, Vector):
            return a if condition else b
        self.tick(len(condition.values))
        return Vector(
            [self.item(a, i) if c else self.item(b, i) for i, c in enumerate(condition.values)]
        )

    def item(self, a, i):
        return a.values[i] if isinstance(a, Vector) else a

    def binary(self, op, a, b):
        self.tick()
        if isinstance(a, Vector) or isinstance(b, Vector):
            n = len(a.values) if isinstance(a, Vector) else len(b.values)
            if isinstance(a, Vector) and isinstance(b, Vector) and len(a.values) != len(b.values):
                raise SandboxError("Series lengths differ.")
            return Vector([self.binary(op, self.item(a, i), self.item(b, i)) for i in range(n)])
        if type(a) not in (int, float, bool) or type(b) not in (int, float, bool):
            if (
                op is ast.Add
                and isinstance(a, str)
                and isinstance(b, str)
                and len(a) + len(b) <= 20000
            ):
                return a + b
            raise SandboxError("Arithmetic requires finite numbers or numeric series.")
        if op is ast.Pow and (abs(b) > 32 or abs(a) > 1e12):
            raise SandboxError("Exponent exceeds the arithmetic limit.")
        operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
            ast.BitAnd: operator.and_,
            ast.BitOr: operator.or_,
        }
        if op not in operations:
            raise SandboxError("Unsupported arithmetic operator.")
        result = operations[op](a, b)
        if isinstance(result, complex) or not math.isfinite(result) or abs(result) > 1e100:
            raise SandboxError("Arithmetic result is outside the supported range.")
        return result

    def compare(self, op, a, b):
        self.tick()
        if isinstance(a, Vector) or isinstance(b, Vector):
            n = len(a.values) if isinstance(a, Vector) else len(b.values)
            return Vector([self.compare(op, self.item(a, i), self.item(b, i)) for i in range(n)])
        operations = {
            ast.Gt: operator.gt,
            ast.GtE: operator.ge,
            ast.Lt: operator.lt,
            ast.LtE: operator.le,
            ast.Eq: operator.eq,
            ast.NotEq: operator.ne,
        }
        if op not in operations:
            raise SandboxError("Unsupported comparison.")
        return operations[op](a, b)

    def expr(self, node, env):
        self.tick()
        if isinstance(node, ast.Constant):
            if type(node.value) not in (str, int, float, bool, type(None)):
                raise SandboxError("Unsupported literal.")
            if isinstance(node.value, str) and len(node.value) > 10000:
                raise SandboxError("String too long.")
            if type(node.value) in (int, float) and (
                not math.isfinite(node.value) or abs(node.value) > 1e100
            ):
                raise SandboxError("Number outside supported range.")
            return node.value
        if isinstance(node, ast.Name):
            if node.id.startswith("_") or node.id not in env:
                raise SandboxError(f"Name {node.id!r} is not available.")
            return env[node.id]
        if isinstance(node, (ast.List, ast.Tuple)):
            return [self.expr(n, env) for n in node.elts]
        if isinstance(node, ast.Dict):
            return {self.expr(k, env): self.expr(v, env) for k, v in zip(node.keys, node.values)}
        if isinstance(node, ast.Subscript):
            value = self.expr(node.value, env)
            if not isinstance(value, (dict, list, Vector)):
                raise SandboxError("Only data dictionaries and series can be indexed.")
            key = self.expr(node.slice, env)
            return self.sequence(value)[key]
        if isinstance(node, ast.Slice):
            return slice(
                self.expr(node.lower, env) if node.lower else None,
                self.expr(node.upper, env) if node.upper else None,
                self.expr(node.step, env) if node.step else None,
            )
        if isinstance(node, ast.BinOp):
            return self.binary(type(node.op), self.expr(node.left, env), self.expr(node.right, env))
        if isinstance(node, ast.UnaryOp):
            value = self.expr(node.operand, env)
            if isinstance(node.op, ast.USub):
                return self.binary(ast.Mult, -1, value)
            if isinstance(node.op, ast.UAdd):
                return self.binary(ast.Mult, 1, value)
            if isinstance(node.op, (ast.Not, ast.Invert)):
                return self.vector_unary(operator.not_, value)
        if isinstance(node, ast.Compare):
            if len(node.ops) != 1:
                raise SandboxError("Use separate comparisons joined with & for series.")
            return self.compare(
                type(node.ops[0]),
                self.expr(node.left, env),
                self.expr(node.comparators[0], env),
            )
        if isinstance(node, ast.BoolOp):
            result = self.expr(node.values[0], env)
            for nxt in node.values[1:]:
                if isinstance(result, Vector):
                    raise SandboxError("Use & and | for series comparisons.")
                if (isinstance(node.op, ast.And) and not result) or (
                    isinstance(node.op, ast.Or) and result
                ):
                    return result
                result = self.expr(nxt, env)
            return result
        if isinstance(node, ast.IfExp):
            return self.expr(node.body if self.expr(node.test, env) else node.orelse, env)
        if isinstance(node, ast.Attribute):
            obj = self.expr(node.value, env)
            if (
                not isinstance(obj, Namespace)
                or node.attr.startswith("_")
                or node.attr not in obj.members
            ):
                raise SandboxError(
                    f"Attribute {node.attr!r} is not available in the guided runtime."
                )
            return obj.members[node.attr]
        if isinstance(node, ast.Call):
            fn = self.expr(node.func, env)
            if node.keywords:
                raise SandboxError("Use positional arguments in the guided runtime.")
            args = [self.expr(arg, env) for arg in node.args]
            if isinstance(fn, Function):
                return self.call_function(fn, args)
            if not callable(fn):
                raise SandboxError("This value is not callable.")
            result = fn(*args)
            if isinstance(result, (str, list)) and len(result) > 20000:
                raise SandboxError("Result exceeds the size limit.")
            return result
        if isinstance(node, ast.JoinedStr):
            result = "".join(
                str(self.expr(v.value, env)) if isinstance(v, ast.FormattedValue) else v.value
                for v in node.values
            )
            if len(result) > 20000:
                raise SandboxError("Formatted string too long.")
            return result
        raise SandboxError(f"{type(node).__name__} is not supported by the guided Python runtime.")

    def assign(self, target, value, env):
        if not isinstance(target, ast.Name) or target.id.startswith("_"):
            raise SandboxError("Assign to a public variable name.")
        env[target.id] = value
        if len(env) > 150:
            raise SandboxError("Too many variables.")

    def block(self, nodes, env):
        for node in nodes:
            self.tick()
            if isinstance(node, ast.Assign):
                value = self.expr(node.value, env)
                for target in node.targets:
                    self.assign(target, value, env)
            elif isinstance(node, ast.AugAssign):
                self.assign(
                    node.target,
                    self.binary(
                        type(node.op),
                        self.expr(node.target, env),
                        self.expr(node.value, env),
                    ),
                    env,
                )
            elif isinstance(node, ast.Expr):
                self.expr(node.value, env)
            elif isinstance(node, ast.Return):
                raise Returned(self.expr(node.value, env) if node.value else None)
            elif isinstance(node, ast.FunctionDef):
                if (
                    node.decorator_list
                    or node.args.defaults
                    or node.args.kwarg
                    or node.args.vararg
                    or node.args.kwonlyargs
                    or node.args.posonlyargs
                    or any(a.annotation for a in node.args.args)
                    or node.returns
                ):
                    raise SandboxError("Use simple functions with positional parameters.")
                self.assign(ast.Name(id=node.name), Function(node, env.copy()), env)
            elif isinstance(node, ast.If):
                self.block(node.body if self.expr(node.test, env) else node.orelse, env)
            elif isinstance(node, ast.For):
                seq = self.sequence(self.expr(node.iter, env))
                if not isinstance(seq, list) or len(seq) > MAX_ITEMS:
                    raise SandboxError("Loop over a bounded list or range.")
                for item in seq:
                    self.assign(node.target, item, env)
                    self.block(node.body, env)
                self.block(node.orelse, env)
            elif isinstance(node, ast.ImportFrom):
                namespace = (
                    self.math
                    if node.module == "math"
                    else self.numpy
                    if node.module == "numpy"
                    else None
                )
                if namespace is None or node.level:
                    raise SandboxError(
                        "Only the documented math and numpy functions are available."
                    )
                for alias in node.names:
                    if alias.name not in namespace.members:
                        raise SandboxError(f"Import {alias.name!r} is not available.")
                    self.assign(
                        ast.Name(id=alias.asname or alias.name),
                        namespace.members[alias.name],
                        env,
                    )
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    namespace = (
                        self.math
                        if alias.name == "math"
                        else self.numpy
                        if alias.name == "numpy"
                        else None
                    )
                    if namespace is None:
                        raise SandboxError(
                            "Imports are limited to math and the guided numpy subset."
                        )
                    self.assign(ast.Name(id=alias.asname or alias.name), namespace, env)
            elif isinstance(node, ast.Pass):
                pass
            else:
                raise SandboxError(
                    f"{type(node).__name__} is not supported. Use bounded for loops and documented functions."
                )

    def call_function(self, fn, args):
        self.depth += 1
        try:
            if self.depth > 12:
                raise SandboxError("Function nesting limit exceeded.")
            if len(args) != len(fn.node.args.args):
                raise SandboxError("Function argument count does not match.")
            scope = fn.closure.copy()
            scope.update({name.arg: value for name, value in zip(fn.node.args.args, args)})
            try:
                self.block(fn.node.body, scope)
            except Returned as result:
                return result.value
            return None
        finally:
            self.depth -= 1

    def run(self, code, data):
        tree = ast.parse(code)
        if sum(1 for _ in ast.walk(tree)) > 4000:
            raise SandboxError("Code exceeds the syntax limit.")
        self.block(tree.body, self.env)
        fn = self.env.get("strategy")
        if not isinstance(fn, Function):
            raise SandboxError("Define strategy(data) and return a Boolean signal for each bar.")
        result = self.call_function(fn, [{k: Vector(v) for k, v in data.items()}])
        signals = self.sequence(result)
        if isinstance(signals, bool):
            signals = [signals] * len(data["close"])
        if not isinstance(signals, list) or len(signals) != len(data["close"]):
            raise SandboxError("strategy(data) must return one Boolean or 0/1 signal per bar.")
        if any(type(x) not in (bool, int, float) or x not in (0, 1) for x in signals):
            raise SandboxError("Only long/cash signals (True/False or 1/0) are supported.")
        return {
            "signals": [bool(x) for x in signals],
            "stdout": self.output,
            "stderr": "",
        }


def main():
    try:
        import resource

        resource.setrlimit(resource.RLIMIT_CPU, (2, 2))
        if sys.platform.startswith("linux"):
            resource.setrlimit(resource.RLIMIT_AS, (256 * 1024 * 1024, 256 * 1024 * 1024))
        resource.setrlimit(resource.RLIMIT_NOFILE, (32, 32))
        payload = json.loads(sys.stdin.read(3000000))
        vm = Interpreter()
        result = vm.run(payload["code"], payload["data"])
    except Exception as error:
        result = {"error": f"{type(error).__name__}: {str(error)[:500]}"}
    print(json.dumps(result, allow_nan=False))


if __name__ == "__main__":
    main()
