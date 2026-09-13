"""Optional smoke check after building quanta-api and quanta-sandbox images."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
os.environ["QUANTA_SANDBOX"] = "docker"
from quanta.analytics import DatasetParams, generate, strategy_data
from quanta.runner import ExecutionError, run

bars = generate(DatasetParams(years=5))
data = strategy_data(bars, 50)
started = time.perf_counter()
output = run(
    'import numpy as np\ndef strategy(data):\n    print(np.mean(data["close"]))\n    return data["close"] > data["close"].rolling(50, min_periods=1).mean()',
    data,
)
assert len(output["signals"]) == 1260
print(
    f"PASS: scientific Python, {len(output['signals'])} signals, {(time.perf_counter() - started) * 1000:.0f} ms"
)
for name, code in [
    ("forbidden import", "import os\ndef strategy(data): return True"),
    ("two-second execution limit", "while True: pass\ndef strategy(data): return True"),
    (
        "256 MiB memory limit",
        "import numpy as np\nx=np.ones(100000000)\ndef strategy(data): return True",
    ),
]:
    try:
        run(code, data)
    except ExecutionError:
        print(f"PASS: rejected {name}")
    else:
        raise AssertionError(f"Failed to reject {name}")
