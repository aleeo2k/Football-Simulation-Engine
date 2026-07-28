import importlib

import pandas as pd

import src.ratings.rating_tracker as rating_tracker
from src.database.database import Database
from src.evaluation.brier_score import BrierScore
from src.evaluation.fast_evaluator import FastEvaluator
from src.evaluation.log_loss import LogLoss


def evaluate():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches ORDER BY date",
        db.engine,
    )

    evaluator = FastEvaluator(matches)

    results = evaluator.evaluate()

    predictions = [
        r["predicted"]
        for r in results
    ]

    actual = [
        r["actual"]
        for r in results
    ]

    accuracy = sum(
        p == a
        for p, a in zip(predictions, actual)
    ) / len(results)

    return (
        accuracy,
        BrierScore.calculate(results),
        LogLoss.calculate(results),
    )


def main():

    values = [
        1,
        2,
        3,
        4,
        5,
        6,
        8,
        10,
        15,
        20,
    ]

    best = None

    print()
    print(
        f"{'Smooth':<10}"
        f"{'Accuracy':<12}"
        f"{'Brier':<12}"
        f"{'LogLoss'}"
    )
    print("-" * 46)

    for value in values:

        rating_tracker.SMOOTHING = value

        importlib.reload(rating_tracker)

        accuracy, brier, logloss = evaluate()

        print(
            f"{value:<10}"
            f"{accuracy:<12.4f}"
            f"{brier:<12.4f}"
            f"{logloss:.4f}"
        )

        if (
            best is None
            or logloss < best["logloss"]
        ):

            best = {
                "value": value,
                "accuracy": accuracy,
                "brier": brier,
                "logloss": logloss,
            }

    print("\nBest parameter")
    print("-" * 20)
    print(f"SMOOTHING : {best['value']}")
    print(f"Accuracy  : {best['accuracy']:.4f}")
    print(f"Brier     : {best['brier']:.4f}")
    print(f"Log Loss  : {best['logloss']:.4f}")


if __name__ == "__main__":
    main()