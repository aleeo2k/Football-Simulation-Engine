import pandas as pd

from src.database.database import Database
from src.evaluation.evaluator import Evaluator
from src.evaluation.brier_score import BrierScore
from src.evaluation.log_loss import LogLoss


START_INDEX = 500
END_INDEX = 1500

DECAYS = [
    0.995,
    0.996,
    0.997,
    0.998,
    0.999,
    0.9995,
]


def evaluate(matches, decay):

    evaluator = Evaluator(
        matches,
        recency_decay=decay,
    )

    results = []

    correct = 0
    total = 0

    end = min(
        END_INDEX,
        len(matches),
    )

    for i in range(
        START_INDEX,
        end,
    ):

        result = evaluator.evaluate_match(i)

        if result is None:
            continue

        results.append(result)

        if result["predicted"] == result["actual"]:
            correct += 1

        total += 1

    return {
        "accuracy": correct / total,
        "brier": BrierScore.calculate(results),
        "log_loss": LogLoss.calculate(results),
    }


def main():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches",
        db.engine,
    )

    print()

    print(
        f"{'Decay':<10}"
        f"{'Accuracy':<12}"
        f"{'Brier':<12}"
        f"{'LogLoss'}"
    )

    print("-" * 46)

    best = None

    for decay in DECAYS:

        metrics = evaluate(
            matches,
            decay,
        )

        print(
            f"{decay:<10}"
            f"{metrics['accuracy']:<12.4f}"
            f"{metrics['brier']:<12.4f}"
            f"{metrics['log_loss']:.4f}"
        )

        if (
            best is None
            or
            metrics["log_loss"] < best["log_loss"]
        ):

            best = {
                "decay": decay,
                **metrics,
            }

    print("\nBest parameter\n")

    print(
        f"Decay: {best['decay']}"
    )

    print(
        f"Accuracy: {best['accuracy']:.4f}"
    )

    print(
        f"Brier: {best['brier']:.4f}"
    )

    print(
        f"Log Loss: {best['log_loss']:.4f}"
    )


if __name__ == "__main__":
    main()