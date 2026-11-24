# Python for the Reluctant Investor — Quick Reference Cheat Sheet

A concise reference guide for beginner investors and non-coders working with Python in Quanta and offline data environments.

---

## 1. Variables and Arithmetic

Variables store numbers and text for calculations:

```python
# Assignment
beli_saham = 10000
jual_saham = 12500

# Basic arithmetic
keuntungan = jual_saham - beli_saham
persentase = (keuntungan / beli_saham) * 100

# Output to console
print(f"Keuntungan: Rp {keuntungan:,.0f} ({persentase:.1f}%)")
```

---

## 2. Lists and Sequences

Lists hold ordered collections of values:

```python
prices = [100.0, 102.5, 101.0, 104.0, 106.0]

# Length and indexing (0-indexed)
total_bars = len(prices)      # 5
first_price = prices[0]       # 100.0
last_price = prices[-1]       # 106.0

# Slicing (start:stop)
recent_3 = prices[-3:]        # [101.0, 104.0, 106.0]
```

---

## 3. Dictionaries (Key-Value Mappings)

Dictionaries represent structured records (like a row in a table):

```python
bar = {
    "date": "2026-03-01",
    "symbol": "BBCA",
    "close": 10250,
    "volume": 450000,
}

# Access values by exact key name (case-sensitive)
print(bar["date"], bar["close"])
```

---

## 4. Built-in Guided Runtime vs Offline CPython

| Feature | Quanta Guided Sandbox | Offline CPython / Desktop |
| :--- | :--- | :--- |
| **Execution** | Server-side guided interpreter (~40–65 ms) | Local Python / Jupyter kernel |
| **Tabular Data** | Native Python lists & dictionaries | `pandas.DataFrame` (`pd.read_csv()`) |
| **Rolling SMA** | Positional `sma(data['close'], 20)` | `df['close'].rolling(20).mean()` |
| **Warm-Up** | Averages available bars without NaN | First $k-1$ rows produce `NaN` |
| **Visualization** | Text / ASCII trend summary in console | `matplotlib.pyplot` (`plt.plot()`, `plt.show()`) |

---

## 5. The Four Classic Beginner Bugs

When code breaks, read the **error class** and **line number** to diagnose:

1. **`SyntaxError`**: Typo in Python grammar (e.g. missing quote `'`, unclosed bracket `]`, or unmatched parenthesis `)`).
2. **`KeyError`**: Dictionary or column key not found. Python is strictly case-sensitive: `bar['Close']` fails if defined as `bar['close']`.
3. **`IndexError`**: Attempting to read a list position that does not exist (e.g. `prices[10]` when `len(prices)` is 5).
4. **`ZeroDivisionError`**: Dividing by zero (e.g. `profit / initial_capital` when `initial_capital == 0`).

---

## 6. Offline Analysis Template (Pandas & Matplotlib)

When running on your own computer with full scientific Python installed:

```python
import matplotlib.pyplot as plt
import pandas as pd

# 1. Load data
df = pd.read_csv("prices.csv")

# 2. Compute 20-day simple moving average
df["sma_20"] = df["close"].rolling(20).mean()

# 3. Plot trajectory
plt.figure(figsize=(10, 5))
plt.plot(df["date"], df["close"], label="Closing Price")
plt.plot(df["date"], df["sma_20"], label="20-Day SMA", linestyle="--")
plt.title("Price Trajectory and Moving Average")
plt.xlabel("Date")
plt.ylabel("Price")
plt.legend()
plt.tight_layout()
plt.savefig("price_chart.png")
```
