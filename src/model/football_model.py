import joblib
import numpy as np
import pandas as pd

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from src.features import FEATURES
from src.pipeline.feature_builder import FeatureBuilder


class FootballModel:

    def __init__(
        self,
        smoothing=5.0,
        form_matches=5,
        home_advantage=70,
        k_factor=20,
    ):

        self.builder = FeatureBuilder(
            smoothing=smoothing,
            form_matches=form_matches,
            home_advantage=home_advantage,
            k_factor=k_factor,
        )

        self.features = FEATURES

        self.pipeline = Pipeline(
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
                        random_state=42,
                    ),
                ),
            ]
        )

    def build_dataset(
        self,
        matches: pd.DataFrame,
    ):

        return self.builder.build(matches)

    def fit(
        self,
        matches: pd.DataFrame,
    ):

        dataset = self.build_dataset(matches)

        X = dataset[self.features]
        y = dataset["result"]

        self.pipeline.fit(
            X,
            y,
        )

        return self

    def evaluate(
        self,
        matches: pd.DataFrame,
    ):

        dataset = self.build_dataset(matches)

        X = dataset[self.features].reset_index(drop=True)
        y = dataset["result"].reset_index(drop=True)

        n = len(dataset)

        train_start = int(n * 0.40)
        test_size = int(n * 0.10)

        accuracies = []
        loglosses = []

        while train_start + test_size <= n:

            X_train = X.iloc[:train_start]
            y_train = y.iloc[:train_start]

            X_test = X.iloc[
                train_start:
                train_start + test_size
            ]

            y_test = y.iloc[
                train_start:
                train_start + test_size
            ]

            self.pipeline.fit(
                X_train,
                y_train,
            )

            prediction = self.pipeline.predict(
                X_test,
            )

            probability = self.pipeline.predict_proba(
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

            train_start += test_size

        return {
            "accuracy": float(
                np.mean(accuracies)
            ),
            "logloss": float(
                np.mean(loglosses)
            ),
            "folds": len(accuracies),
        }

    def save(
        self,
        path="football_model.pkl",
    ):

        joblib.dump(
            self.pipeline,
            path,
        )

    def load(
        self,
        path="football_model.pkl",
    ):

        self.pipeline = joblib.load(path)

        return self