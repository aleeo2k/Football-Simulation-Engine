import pandas as pd

from src.database.database import Database
from src.evaluation.evaluator import Evaluator
from src.evaluation.confusion_matrix import ConfusionMatrix
from src.evaluation.brier_score import BrierScore
from src.evaluation.log_loss import LogLoss


START_INDEX = 500
END_INDEX = 1500


def main():

    print("=== Evaluation Engine ===\n")

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches",
        db.engine,
    )

    evaluator = Evaluator(matches)

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

        predictions.append(
            result["predicted"]
        )

        actual.append(
            result["actual"]
        )

        if (
            result["predicted"]
            ==
            result["actual"]
        ):
            correct += 1

        total += 1

        if total % 100 == 0:
            print(
                f"Processed {total} matches..."
            )

    accuracy = correct / total

    matrix = ConfusionMatrix.build(
        predictions,
        actual,
    )

    brier = BrierScore.calculate(
        results,
    )

    log_loss = LogLoss.calculate(
        results,
    )

    print("\n==============================")
    print("Evaluation Complete")
    print("==============================")

    print(
        f"Matches evaluated : {total}"
    )

    print(
        f"Correct predictions : {correct}"
    )

    print(
        f"Accuracy : {accuracy:.2%}"
    )

    print(
        f"Brier Score : {brier:.4f}"
    )

    print(
        f"Log Loss : {log_loss:.4f}"
    )

    print("\nConfusion Matrix")
    print("----------------")

    print(matrix)


if __name__ == "__main__":
    main()