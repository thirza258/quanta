"""Reproduce the fictional news-course capstone. No network or trading actions."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Scenario:
    name: str
    contract_sales: float
    working_capital: float
    discount_rate: float
    efficiency_savings: float = 12


def analyze(scenario: Scenario) -> dict[str, float]:
    growth = 0.02
    if scenario.discount_rate <= growth:
        raise ValueError("Stable-growth discount rate must exceed growth.")
    ebit = 1000 - 600 - 200 - 30 + scenario.contract_sales * 0.40 + scenario.efficiency_savings
    fcff = ebit * 0.75 + 30 - 40 - scenario.working_capital
    operating_value = fcff / (scenario.discount_rate - growth)
    return {
        "EBIT": ebit,
        "FCFF": fcff,
        "Operating value": operating_value,
        "Value per share": (operating_value - 300) / 100,
    }


def main():
    print("Fictional teaching case; all figures and assumptions are supplied by the study pack.")
    for scenario in (Scenario("Base", 20, 20, 0.10), Scenario("Downside", 0, 35, 0.11)):
        result = analyze(scenario)
        print(f"\n{scenario.name}")
        for label, value in result.items():
            print(f"{label}: {value:.4f}")
        if scenario.name == "Downside":
            print(f"Conditional 25% margin threshold: {result['Value per share'] * 0.75:.4f}")
    print(
        "\nCompare with the fictional observed price of 12; document omissions and review triggers."
    )


if __name__ == "__main__":
    main()
