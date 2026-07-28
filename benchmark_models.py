import time

import pandas as pd

from catboost import CatBoostClassifier

from sklearn.ensemble import (
    ExtraTreesClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.model_selection import train_test_split

from src.features import FEATURES


def evaluate(model, X_train, X_test, y_train, y_test):

    start = time.perf_counter()

    model.fit(
        X_train,
        y_train,
    )

    train_time = time.perf_counter() - start

    start = time.perf_counter()

    prediction = model.predict(
        X_test,
    )

    probability = model.predict_proba(
        X_test,
    )

    predict_time = time.perf_counter() - start

    return {
        "accuracy": accuracy_score(
            y_test,
            prediction,
        ),
        "logloss": log_loss(
            y_test,
            probability,
        ),
        "train_time": train_time,
        "predict_time": predict_time,
    }


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

    models = {

        "LogisticRegression":
            LogisticRegression(
                solver="lbfgs",
                max_iter=5000,
            ),

        "HistGradientBoosting":
            HistGradientBoostingClassifier(
                random_state=42,
            ),

        "RandomForest":
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1,
            ),

        "ExtraTrees":
            ExtraTreesClassifier(
                n_estimators=300,
                random_state=42,
                n_jobs=-1,
            ),

        "CatBoost":
            CatBoostClassifier(
                iterations=500,
                depth=6,
                learning_rate=0.05,
                loss_function="MultiClass",
                verbose=False,
                random_seed=42,
            ),
    }

    print()

    print(
        f"{'Model':28}"
        f"{'Accuracy':12}"
        f"{'LogLoss':12}"
        f"{'Train(s)':12}"
        f"{'Predict(s)'}"
    )

    print("-" * 85)

    for name, model in models.items():

        result = evaluate(
            model,
            X_train,
            X_test,
            y_train,
            y_test,
        )

        print(
            f"{name:28}"
            f"{result['accuracy']:<12.4f}"
            f"{result['logloss']:<12.4f}"
            f"{result['train_time']:<12.3f}"
            f"{result['predict_time']:.3f}"
        )


if __name__ == "__main__":
    main()