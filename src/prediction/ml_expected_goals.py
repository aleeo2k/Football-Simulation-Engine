from pathlib import Path

import joblib
import pandas as pd


class MLExpectedGoals:

    def __init__(self):

        models_dir = Path(__file__).resolve().parents[2] / "models"

        self.home_model = joblib.load(
            models_dir / "home_xg_model.pkl"
        )

        self.away_model = joblib.load(
            models_dir / "away_xg_model.pkl"
        )

    def predict(self, features: dict):

        debug = features.pop("_debug", False)

        X = pd.DataFrame([features])

        if debug:
            print("\n========== FEATURES ==========")
            print(X)
            print()

        home_xg = float(self.home_model.predict(X)[0])
        away_xg = float(self.away_model.predict(X)[0])

        if debug:
            print(f"PREDICTED: {home_xg:.3f} : {away_xg:.3f}")
            print("==============================\n")

        return {
            "home_xg": max(home_xg, 0.05),
            "away_xg": max(away_xg, 0.05),
        }