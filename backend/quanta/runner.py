import json
import os
import subprocess
import sys
import uuid
from pathlib import Path


class ExecutionError(ValueError):
    pass


def run(code: str, data: dict) -> dict:
    mode = os.getenv("QUANTA_SANDBOX", "guided")
    container = None
    if mode == "docker":
        container = f"quanta-run-{uuid.uuid4().hex}"
        command = [
            "docker",
            "run",
            "--rm",
            "--name",
            container,
            "--network",
            "none",
            "--memory",
            "256m",
            "--memory-swap",
            "256m",
            "--cpus",
            "1",
            "--pids-limit",
            "32",
            "--read-only",
            "--cap-drop",
            "ALL",
            "--security-opt",
            "no-new-privileges",
            "--user",
            "65534:65534",
            "--tmpfs",
            "/tmp:rw,noexec,nosuid,size=16m",
            "-i",
            "quanta-sandbox:local",
        ]
    elif mode == "guided":
        command = [
            sys.executable,
            "-I",
            str(Path(__file__).with_name("sandbox_worker.py")),
        ]
    else:
        raise ExecutionError("Unknown sandbox mode. Use guided or docker.")
    try:
        # Docker startup/import time is separate from the worker's two-second
        # student-code timer. The guided process has a two-second total timeout.
        result = subprocess.run(
            command,
            input=json.dumps({"code": code, "data": data}),
            text=True,
            capture_output=True,
            timeout=15 if container else 2,
            env={
                "PATH": os.environ.get("PATH", ""),
                "OPENBLAS_NUM_THREADS": "1",
                "OMP_NUM_THREADS": "1",
            },
        )
        if result.returncode:
            raise ExecutionError(
                "Sandbox process stopped. Check resource limits or start the configured Docker runtime."
            )
        output = json.loads(result.stdout)
        if "error" in output:
            raise ExecutionError(output["error"])
        signals = output.get("signals")
        if (
            not isinstance(signals, list)
            or len(signals) != len(data["close"])
            or any(type(v) not in (bool, int, float) or v not in (0, 1) for v in signals)
        ):
            raise ExecutionError("Return one Boolean long/cash signal for every bar.")
        return output
    except subprocess.TimeoutExpired:
        raise ExecutionError("Execution exceeded the 2-second limit.") from None
    except OSError, json.JSONDecodeError:
        raise ExecutionError("Sandbox runtime unavailable or returned invalid output.") from None
    finally:
        if container:
            try:
                subprocess.run(["docker", "rm", "-f", container], capture_output=True, timeout=3)
            except OSError, subprocess.TimeoutExpired:
                pass
