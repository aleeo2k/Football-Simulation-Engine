import time

import pandas as pd

from src.database.database import Database
from src.evaluation.brier_score import BrierScore
from src.evaluation.confusion_matrix import ConfusionMatrix
from src.evaluation.fast_evaluator import FastEvaluator
from src.evaluation.log_loss import LogLoss


def main():

    start = time.perf_counter()

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches ORDER BY date",
        db.engine,
    )

    evaluator = FastEvaluator(matches)

    results = evaluator.evaluate()

    print("Checking for NaN values...\n")

    nan_found = False

    for i, result in enumerate(results):

        if (
            pd.isna(result["home_win"])
            or pd.isna(result["draw"])
            or pd.isna(result["away_win"])
        ):

            nan_found = True

            print("=" * 50)
            print(f"NaN FOUND IN RESULT #{i}")
            print("=" * 50)
            print(result)
            print()

            break

    if not nan_found:
        print("No NaN values found.\n")

    predictions = [
        r["predicted"]
        for r in results
    ]

    actual = [
        r["actual"]
        for r in results
    ]

    correct = sum(
        p == a
        for p, a in zip(
            predictions,
            actual,
        )
    )

    accuracy = correct / len(results)

    elapsed = time.perf_counter() - start

    print("\n========== FAST EVALUATION ==========\n")

    print(f"Matches      : {len(results)}")
    print(f"Accuracy     : {accuracy:.2%}")
    print(f"Brier Score  : {BrierScore.calculate(results):.4f}")
    print(f"Log Loss     : {LogLoss.calculate(results):.4f}")

    print("\nConfusion Matrix\n")

    print(
        ConfusionMatrix.build(
            predictions,
            actual,
        )
    )

    print(f"\nTime: {elapsed:.2f} sec")


if __name__ == "__main__":
    main()