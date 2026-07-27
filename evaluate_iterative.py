import pandas as pd

from src.database.database import Database
from src.evaluation.iterative_evaluator import IterativeEvaluator
from src.evaluation.confusion_matrix import ConfusionMatrix
from src.evaluation.brier_score import BrierScore
from src.evaluation.log_loss import LogLoss


START_INDEX = 500
END_INDEX = 1500


def main():

    print("=== Iterative Model Evaluation ===\n")

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches",
        db.engine,
    )

    evaluator = IterativeEvaluator(matches)

    results = []
    predictions = []
    actual = []

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
        predictions.append(result["predicted"])
        actual.append(result["actual"])

        if result["predicted"] == result["actual"]:
            correct += 1

        total += 1

        if total % 100 == 0:
            print(f"Processed {total} matches...")

    accuracy = correct / total

    print("\n==============================")
    print("Evaluation Complete")
    print("==============================")

    print(f"Matches evaluated : {total}")
    print(f"Correct predictions : {correct}")
    print(f"Accuracy : {accuracy:.2%}")
    print(f"Brier Score : {BrierScore.calculate(results):.4f}")
    print(f"Log Loss : {LogLoss.calculate(results):.4f}")

    print("\nConfusion Matrix")
    print("----------------")

    print(
        ConfusionMatrix.build(
            predictions,
            actual,
        )
    )


if __name__ == "__main__":
    main()