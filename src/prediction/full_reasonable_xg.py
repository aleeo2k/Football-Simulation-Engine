from pathlib import Path

import joblib
import numpy as np
import pandas as pd


class FullReasonableXG:

    def __init__(self):

        models_dir = (
            Path(__file__)
            .resolve()
            .parents[2]
            / "models"
        )

        # ====================================================
        # REAL FULL REASONABLE MODELS
        # ====================================================

        home_path = (
            models_dir
            / "xg_full_reasonable_home.pkl"
        )

        away_path = (
            models_dir
            / "xg_full_reasonable_away.pkl"
        )

        if not home_path.exists():

            raise FileNotFoundError(
                f"FULL REASONABLE home model not found:\n"
                f"{home_path}"
            )

        if not away_path.exists():

            raise FileNotFoundError(
                f"FULL REASONABLE away model not found:\n"
                f"{away_path}"
            )

        self.home_model = joblib.load(
            home_path
        )

        self.away_model = joblib.load(
            away_path
        )

        # ====================================================
        # EXACT FEATURES USED BY THE SAVED MODEL
        # ====================================================

        self.home_features = list(
            self.home_model.feature_names_
        )

        self.away_features = list(
            self.away_model.feature_names_
        )

        # Both models must use the same features.
        if (
            self.home_features
            != self.away_features
        ):

            raise ValueError(
                "Home and away FULL REASONABLE "
                "models use different feature orders."
            )

    # ========================================================
    # PREDICT
    # ========================================================

    def predict(
        self,
        features,
    ):

        # ----------------------------------------------------
        # Dict
        # ----------------------------------------------------

        if isinstance(
            features,
            dict,
        ):

            features = pd.DataFrame(
                [features]
            )

        # ----------------------------------------------------
        # Series
        # ----------------------------------------------------

        elif isinstance(
            features,
            pd.Series,
        ):

            features = (
                features
                .to_frame()
                .T
            )

        # ----------------------------------------------------
        # DataFrame
        # ----------------------------------------------------

        elif isinstance(
            features,
            pd.DataFrame,
        ):

            features = features.copy()

        else:

            raise TypeError(
                "features must be "
                "dict, Series or DataFrame"
            )

        # ====================================================
        # CHECK EXACT MODEL FEATURES
        # ====================================================

        missing = [
            feature
            for feature in self.home_features
            if feature not in features.columns
        ]

        if missing:

            raise ValueError(
                "Missing FULL REASONABLE "
                "model features:\n"
                + "\n".join(missing)
            )

        # ====================================================
        # EXACT CATBOOST ORDER
        # ====================================================

        X = features[
            self.home_features
        ].copy()

        # ====================================================
        # PREDICT
        # ====================================================

        home_xg = (
            self.home_model
            .predict(X)
        )

        away_xg = (
            self.away_model
            .predict(X)
        )

        # ====================================================
        # SAFETY
        # ====================================================

        home_xg = np.maximum(
            home_xg,
            0.01,
        )

        away_xg = np.maximum(
            away_xg,
            0.01,
        )

        return {

            "home_xg":
                float(
                    home_xg[0]
                ),

            "away_xg":
                float(
                    away_xg[0]
                ),
        }