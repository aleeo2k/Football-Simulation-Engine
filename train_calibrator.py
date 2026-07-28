import joblib
import pandas as pd

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split

from src.features import FEATURES


def main():

    df = pd.read_csv(
        "calibration_dataset.csv"
    )

    X = df[FEATURES]
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

    predictions = model.predict(
        X_test,
    )

    probabilities = model.predict_proba(
        X_test,
    )

    print("\n" + "=" * 50)
    print("CALIBRATOR")
    print("=" * 50)

    print()

    print(
        f"Accuracy : {accuracy_score(y_test, predictions):.4f}"
    )

    print(
        f"LogLoss  : {log_loss(y_test, probabilities):.4f}"
    )

    classifier = model.named_steps["classifier"]

    importance = (
        abs(classifier.coef_)
        .mean(axis=0)
    )

    feature_importance = (
        pd.DataFrame(
            {
                "Feature": FEATURES,
                "Importance": importance,
            }
        )
        .sort_values(
            "Importance",
            ascending=False,
        )
    )

    print("\nFeature importance:\n")

    print(
        feature_importance.to_string(
            index=False,
        )
    )

    joblib.dump(
        model,
        "calibrator.pkl",
    )

    print("\nSaved calibrator.pkl")


if __name__ == "__main__":
    main()