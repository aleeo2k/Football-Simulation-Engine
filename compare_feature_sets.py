import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.features import FEATURES


def evaluate(features):

    df = pd.read_csv(
        "calibration_dataset.csv"
    )

    X = df[features]
    y = df["result"]

    n = len(df)

    train_end = int(n * 0.40)
    test_size = int(n * 0.10)

    accuracies = []
    loglosses = []

    while train_end + test_size <= n:

        X_train = X.iloc[:train_end]
        y_train = y.iloc[:train_end]

        X_test = X.iloc[
            train_end:
            train_end + test_size
        ]

        y_test = y.iloc[
            train_end:
            train_end + test_size
        ]

        model = Pipeline(
            [
                (
                    "scaler",
                    StandardScaler(),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        solver="lbfgs",
                        max_iter=5000,
                    ),
                ),
            ]
        )

        model.fit(
            X_train,
            y_train,
        )

        prediction = model.predict(
            X_test,
        )

        probability = model.predict_proba(
            X_test,
        )

        accuracies.append(
            accuracy_score(
                y_test,
                prediction,
            )
        )

        loglosses.append(
            log_loss(
                y_test,
                probability,
            )
        )

        train_end += test_size

    return (
        sum(accuracies) / len(accuracies),
        sum(loglosses) / len(loglosses),
    )


def main():

    print()
    print("=" * 70)
    print("CURRENT FEATURE SET")
    print("=" * 70)
    print()

    acc, loss = evaluate(
        FEATURES
    )

    print(
        f"Features : {len(FEATURES)}"
    )

    print(
        f"Accuracy : {acc:.5f}"
    )

    print(
        f"LogLoss  : {loss:.5f}"
    )


if __name__ == "__main__":
    main()