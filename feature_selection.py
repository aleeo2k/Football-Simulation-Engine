import pandas as pd

from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import TimeSeriesSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


FEATURES = [

    "home_xg",
    "away_xg",
    "xg_diff",

    "home_win",
    "draw",
    "away_win",

    "home_attack",
    "away_attack",
    "home_defence",
    "away_defence",

    "attack_diff",
    "defence_diff",

    "league_home_xg",
    "league_away_xg",
    "league_total_xg",

    "home_attack_delta",
    "home_defence_delta",
    "away_attack_delta",
    "away_defence_delta",

    "home_elo",
    "away_elo",
    "elo_diff",
]


def main():

    df = pd.read_csv(
        "calibration_dataset.csv"
    )

    X = df[FEATURES]
    y = df["result"]

    estimator = Pipeline(
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

    selector = SequentialFeatureSelector(
        estimator=estimator,
        n_features_to_select="auto",
        direction="backward",
        scoring="accuracy",
        cv=TimeSeriesSplit(
            n_splits=5,
        ),
        n_jobs=-1,
    )

    selector.fit(
        X,
        y,
    )

    selected = []

    print()
    print("=" * 70)
    print("SELECTED FEATURES")
    print("=" * 70)
    print()

    for feature, keep in zip(
        FEATURES,
        selector.get_support(),
    ):

        if keep:

            selected.append(feature)

            print(feature)

    print()
    print("=" * 70)
    print(f"Selected: {len(selected)} / {len(FEATURES)}")
    print("=" * 70)


if __name__ == "__main__":
    main()