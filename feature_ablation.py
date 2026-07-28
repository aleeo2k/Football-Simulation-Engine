import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from src.features import FEATURES


def evaluate(features):

    df = pd.read_csv(
        "calibration_dataset.csv"
    )

    X = df[features]
    y = df["result"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        shuffle=False,
    )

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

    return (
        accuracy_score(
            y_test,
            prediction,
        ),
        log_loss(
            y_test,
            probability,
        ),
    )


def main():

    print()
    print("=" * 70)
    print("FEATURE ABLATION")
    print("=" * 70)
    print()

    accuracy, loss = evaluate(FEATURES)

    print(
        f"{'ALL FEATURES':30}"
        f"Accuracy={accuracy:.5f}   "
        f"LogLoss={loss:.5f}"
    )

    print()

    results = []

    for feature in FEATURES:

        subset = [
            f
            for f in FEATURES
            if f != feature
        ]

        accuracy, loss = evaluate(
            subset
        )

        results.append(
            (
                feature,
                accuracy,
                loss,
            )
        )

    results.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    print(
        f"{'Removed feature':25}"
        f"{'Accuracy':12}"
        f"{'LogLoss'}"
    )

    print("-" * 60)

    for feature, accuracy, loss in results:

        print(
            f"{feature:25}"
            f"{accuracy:.5f}     "
            f"{loss:.5f}"
        )


if __name__ == "__main__":
    main()