"""Quanta original offline teaching lab. Standard library only; no network or broker.

Run: python3 paper_bot_lab.py
Persistent replay: python3 paper_bot_lab.py --db harbor.sqlite
Inspect later: python3 paper_bot_lab.py --db harbor.sqlite --report
Prices and cash are integer cents; timestamps are fixture milliseconds.
References and assumptions: README.md alongside this file.
"""

import argparse
import hashlib
import json
import math
import sqlite3
import tempfile
from contextlib import contextmanager
from pathlib import Path


def positive_int(value, name):
    if type(value) is not int or value <= 0:
        raise ValueError(f"{name} must be a positive integer")
    return value


def identity(value):
    if not isinstance(value, str) or not value.strip():
        raise ValueError("identity must be nonempty text")
    return value


def digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


class PaperBot:
    """One-symbol, long-only, limit-order simulator with durable local accounting."""

    def __init__(self, database, initial_cash=1_000_000):
        positive_int(initial_cash, "initial cash")
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS account (
                id INTEGER PRIMARY KEY CHECK(id=1), initial_cash INTEGER NOT NULL,
                cash INTEGER NOT NULL, shares INTEGER NOT NULL, halt TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL, side TEXT NOT NULL,
                quantity INTEGER NOT NULL, remaining INTEGER NOT NULL,
                price_limit INTEGER NOT NULL, created INTEGER NOT NULL, status TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS fills (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL, order_id TEXT NOT NULL,
                side TEXT NOT NULL, quantity INTEGER NOT NULL, price INTEGER NOT NULL,
                fee INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS events (
                id TEXT PRIMARY KEY, payload TEXT NOT NULL, event_time INTEGER NOT NULL);
            CREATE TABLE IF NOT EXISTS transitions (
                id INTEGER PRIMARY KEY, action TEXT NOT NULL, reason TEXT NOT NULL);
        """)
        with self.db:
            self.db.execute(
                "INSERT OR IGNORE INTO account VALUES (1, ?, ?, 0, '')",
                (initial_cash, initial_cash),
            )

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def close(self):
        self.db.close()

    @staticmethod
    def fee(notional):
        # Five basis points, rounded upward to the next cent for each fill.
        return (notional * 5 + 9999) // 10000

    @staticmethod
    def clock(event_time, now, session_open):
        if type(event_time) is not int or type(now) is not int:
            raise ValueError("timestamps must be integer milliseconds")
        if event_time < 0 or now < event_time or now - event_time > 500:
            raise ValueError("stale or future quote")
        if session_open is not True:
            raise ValueError("session closed")

    def place(
        self, intent_id, side, quantity, price_limit, *, quote, event_time, now, session_open=True
    ):
        identity(intent_id)
        positive_int(quantity, "quantity")
        positive_int(price_limit, "price limit")
        if side not in ("buy", "sell"):
            raise ValueError("unsupported side")
        payload = digest([side, quantity, price_limit, event_time])
        with self.transaction():
            existing = self.db.execute("SELECT * FROM orders WHERE id=?", (intent_id,)).fetchone()
            if existing:
                if existing["payload"] != payload:
                    raise ValueError("intent identity conflict")
                return dict(existing)
            positive_int(quote, "quote")
            self.clock(event_time, now, session_open)
            latest = self.db.execute("SELECT MAX(event_time) FROM events").fetchone()[0]
            if latest is not None and now < latest:
                raise ValueError("decision predates processed market state")
            state = self.db.execute("SELECT * FROM account").fetchone()
            pending = self.db.execute("SELECT * FROM orders WHERE remaining>0").fetchall()
            if side == "buy":
                if state["halt"]:
                    raise ValueError("new risk halted")
                # Per-share fee reserve covers even one-share partial fills.
                reserved = sum(
                    o["remaining"] * (o["price_limit"] + self.fee(o["price_limit"]))
                    for o in pending
                    if o["side"] == "buy"
                )
                need = quantity * (price_limit + self.fee(price_limit))
                if need + reserved > state["cash"]:
                    raise ValueError("insufficient available cash including fees")
                committed = sum(o["remaining"] for o in pending if o["side"] == "buy")
                # $5,000 name cap and 100-share cap are fixed teaching policies.
                if state["shares"] + committed + quantity > 100:
                    raise ValueError("share cap exceeded")
                exposure = state["shares"] * quote + quantity * price_limit
                exposure += sum(
                    o["remaining"] * o["price_limit"] for o in pending if o["side"] == "buy"
                )
                if exposure > 500_000:
                    raise ValueError("name notional cap exceeded")
            else:
                committed = sum(o["remaining"] for o in pending if o["side"] == "sell")
                if quantity + committed > state["shares"]:
                    raise ValueError("insufficient unreserved shares")
            self.db.execute(
                "INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, 'open')",
                (intent_id, payload, side, quantity, quantity, price_limit, now),
            )
            return dict(self.db.execute("SELECT * FROM orders WHERE id=?", (intent_id,)).fetchone())

    def _fill(self, fill_id, order, quantity, price):
        payload = digest([order["id"], quantity, price])
        existing = self.db.execute("SELECT payload FROM fills WHERE id=?", (fill_id,)).fetchone()
        if existing:
            if existing["payload"] != payload:
                raise ValueError("fill identity conflict")
            return False
        positive_int(quantity, "fill quantity")
        positive_int(price, "fill price")
        if quantity > order["remaining"]:
            raise ValueError("overfill")
        if order["side"] == "buy" and price > order["price_limit"]:
            raise ValueError("buy limit exceeded")
        if order["side"] == "sell" and price < order["price_limit"]:
            raise ValueError("sell limit exceeded")
        notional = quantity * price
        fee = self.fee(notional)
        direction = 1 if order["side"] == "buy" else -1
        self.db.execute(
            "INSERT INTO fills VALUES (?, ?, ?, ?, ?, ?, ?)",
            (fill_id, payload, order["id"], order["side"], quantity, price, fee),
        )
        self.db.execute(
            "UPDATE account SET cash=cash-?, shares=shares+? WHERE id=1",
            (direction * notional + fee, direction * quantity),
        )
        remaining = order["remaining"] - quantity
        self.db.execute(
            "UPDATE orders SET remaining=?, status=? WHERE id=?",
            (remaining, "filled" if remaining == 0 else "partial", order["id"]),
        )
        return True

    def replay_fill(self, fill_id, order_id, quantity, price):
        """Replay an existing immutable fill message; cannot inject a new fill."""
        identity(fill_id)
        with self.transaction():
            existing = self.db.execute("SELECT * FROM fills WHERE id=?", (fill_id,)).fetchone()
            if not existing:
                raise ValueError("unknown fill; fills originate from market events")
            if existing["payload"] != digest([order_id, quantity, price]):
                raise ValueError("fill identity conflict")
            return False

    def market(self, event_id, price, volume, *, event_time, now, session_open=True):
        identity(event_id)
        positive_int(price, "market price")
        positive_int(volume, "eligible volume")
        self.clock(event_time, now, session_open)
        payload = digest([price, volume, event_time])
        with self.transaction():
            existing = self.db.execute(
                "SELECT payload FROM events WHERE id=?", (event_id,)
            ).fetchone()
            if existing:
                if existing["payload"] != payload:
                    raise ValueError("event identity conflict")
                return 0
            latest = self.db.execute("SELECT MAX(event_time) FROM events").fetchone()[0]
            if latest is not None and event_time <= latest:
                raise ValueError("out-of-order market event")
            self.db.execute("INSERT INTO events VALUES (?, ?, ?)", (event_id, payload, event_time))
            orders = self.db.execute(
                "SELECT * FROM orders WHERE remaining>0 AND created<? ORDER BY created, rowid",
                (event_time,),
            ).fetchall()
            filled = 0
            for order in orders:
                marketable = (
                    price <= order["price_limit"]
                    if order["side"] == "buy"
                    else price >= order["price_limit"]
                )
                if marketable and volume:
                    quantity = min(volume, order["remaining"])
                    self._fill(f"{event_id}/{order['id']}", order, quantity, price)
                    volume -= quantity
                    filled += quantity
            self.reconcile()
            return filled

    def cancel(self, order_id):
        with self.transaction():
            row = self.db.execute("SELECT * FROM orders WHERE id=?", (order_id,)).fetchone()
            if row is None:
                raise ValueError("unknown order")
            if row["remaining"]:
                self.db.execute(
                    "UPDATE orders SET remaining=0, status='canceled' WHERE id=?", (order_id,)
                )
                self.db.execute(
                    "INSERT INTO transitions(action,reason) VALUES ('cancel',?)", (order_id,)
                )

    def halt(self, reason):
        identity(reason)
        with self.transaction():
            self.db.execute("UPDATE account SET halt=? WHERE id=1", (reason,))
            self.db.execute("INSERT INTO transitions(action,reason) VALUES ('halt',?)", (reason,))

    def resume(self, reason):
        identity(reason)
        with self.transaction():
            self.reconcile()
            self.db.execute("UPDATE account SET halt='' WHERE id=1")
            self.db.execute("INSERT INTO transitions(action,reason) VALUES ('resume',?)", (reason,))

    def reconcile(self):
        state = self.db.execute("SELECT * FROM account").fetchone()
        cash, shares = state["initial_cash"], 0
        for fill in self.db.execute("SELECT * FROM fills ORDER BY rowid"):
            direction = 1 if fill["side"] == "buy" else -1
            cash -= direction * fill["quantity"] * fill["price"] + fill["fee"]
            shares += direction * fill["quantity"]
        if cash != state["cash"] or shares != state["shares"] or cash < 0 or shares < 0:
            raise ValueError("ledger mismatch")
        return True

    def report(self, mark=10_200):
        positive_int(mark, "mark")
        self.reconcile()
        state = self.db.execute("SELECT * FROM account").fetchone()
        return {
            "cash_cents": state["cash"],
            "shares": state["shares"],
            "equity_cents": state["cash"] + state["shares"] * mark,
            "pnl_cents": state["cash"] + state["shares"] * mark - state["initial_cash"],
            "fees_cents": self.db.execute("SELECT COALESCE(SUM(fee),0) FROM fills").fetchone()[0],
            "fills": self.db.execute("SELECT COUNT(*) FROM fills").fetchone()[0],
            "open_orders": self.db.execute(
                "SELECT COUNT(*) FROM orders WHERE remaining>0"
            ).fetchone()[0],
            "halt_reason": state["halt"],
        }


def ridge_walkforward():
    """Two expanding-window predictions on artificial y=1+2x observations.

    Training means and centered slope are refitted separately at each cutoff.
    Fixed lambda=1; no test-based tuning. Units are abstract, not stock returns.
    """
    xs, ys = [-2, -1, 0, 1, 2, 3], [-3, -1, 1, 3, 5, 7]
    rows = []
    for cutoff in (4, 5):
        xmean = sum(xs[:cutoff]) / cutoff
        ymean = sum(ys[:cutoff]) / cutoff
        cross = sum((xs[i] - xmean) * (ys[i] - ymean) for i in range(cutoff))
        variance = sum((xs[i] - xmean) ** 2 for i in range(cutoff))
        slope = cross / (variance + 1)
        prediction = ymean + slope * (xs[cutoff] - xmean)
        rows.append(
            {
                "training_rows": cutoff,
                "slope": slope,
                "prediction": prediction,
                "actual": ys[cutoff],
                "baseline": ymean,
            }
        )
    return {
        "folds": rows,
        "model_mse": sum((r["prediction"] - r["actual"]) ** 2 for r in rows) / len(rows),
        "baseline_mse": sum((r["baseline"] - r["actual"]) ** 2 for r in rows) / len(rows),
    }


EVIDENCE = {
    "HBR-2025-v1": {
        "issuer": "HBR",
        "period": "2025",
        "available": 15,
        "unit": "USD million",
        "revenue": 120,
        "prior_revenue": 100,
    }
}
CANDIDATE = {
    "source_id": "HBR-2025-v1",
    "issuer": "HBR",
    "period": "2025",
    "field": "revenue",
    "value": 120,
    "unit": "USD million",
}


def validate_fact(candidate, evidence, as_of):
    """Verify a fixture response against supplied evidence, not arbitrary documents."""
    if set(candidate) != set(CANDIDATE):
        raise ValueError("unexpected or missing fields")
    if any(not isinstance(candidate[key], str) for key in candidate if key != "value"):
        raise ValueError("invalid text field")
    if type(candidate["value"]) not in (int, float) or not math.isfinite(candidate["value"]):
        raise ValueError("invalid numeric value")
    record = evidence.get(candidate["source_id"])
    if record is None or record["available"] > as_of:
        raise ValueError("source missing or unavailable as of decision")
    for key in ("issuer", "period", "unit"):
        if candidate[key] != record[key]:
            raise ValueError(f"evidence {key} mismatch")
    if candidate["field"] != "revenue" or candidate["value"] != record["revenue"]:
        raise ValueError("unsupported fact")
    if record["prior_revenue"] <= 0:
        raise ValueError("growth denominator unavailable")
    return {
        "source_id": candidate["source_id"],
        "verified_revenue": candidate["value"],
        "growth": candidate["value"] / record["prior_revenue"] - 1,
    }


def run_demo(database):
    bot = PaperBot(database)
    try:
        if bot.db.execute("SELECT COUNT(*) FROM orders").fetchone()[0]:
            raise ValueError(
                "demo requires an unused database; use --report to inspect existing work"
            )
        # Completed closes [98, 99, 100]: fixed illustrative rule proposes ten shares.
        closes = [9800, 9900, 10000]
        target = 10 if closes[-1] > sum(closes) / len(closes) else 0
        bot.place("trend-v1/HBR/0", "buy", target, 10000, quote=10000, event_time=0, now=0)
        bot.market("E1", 10000, 4, event_time=1000, now=1000)
        bot.market("E1", 10000, 4, event_time=1000, now=1000)
        bot.close()
        bot = PaperBot(database)
        bot.market("E2", 9900, 6, event_time=2000, now=2000)
        bot.replay_fill("E1/trend-v1/HBR/0", "trend-v1/HBR/0", 4, 10000)
        bot.halt("incident rehearsal")
        bot.close()
        bot = PaperBot(database)
        rejected = False
        try:
            bot.place("blocked-entry", "buy", 1, 10000, quote=10000, event_time=2000, now=2000)
        except ValueError as error:
            rejected = str(error) == "new risk halted"
        if not rejected:
            raise AssertionError("persistent halt gate failed")
        # Reduction is permitted while new risk is halted; all other gates still apply.
        bot.place("reduce/HBR/2000", "sell", 2, 10100, quote=10100, event_time=2000, now=2000)
        bot.market("E3", 10200, 2, event_time=3000, now=3000)
        return {
            "paper": bot.report(),
            "halt_rejected_entry": rejected,
            "ml": ridge_walkforward(),
            "ai_fixture": validate_fact(CANDIDATE, EVIDENCE, 20),
        }
    finally:
        bot.close()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", help="New SQLite file for replay, or existing file with --report")
    parser.add_argument(
        "--report", action="store_true", help="Read and reconcile an existing lab database"
    )
    args = parser.parse_args()
    if args.report:
        if not args.db or not Path(args.db).is_file():
            parser.error("--report requires an existing --db file")
        bot = PaperBot(args.db)
        try:
            result = bot.report()
        finally:
            bot.close()
    elif args.db:
        result = run_demo(args.db)
    else:
        with tempfile.TemporaryDirectory(prefix="quanta-paper-") as directory:
            result = run_demo(Path(directory) / "harbor.sqlite")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
