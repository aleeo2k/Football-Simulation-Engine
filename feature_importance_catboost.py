import pandas as pd

from catboost import CatBoostClassifier
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

    model = CatBoostClassifier(
        iterations=500,
        depth=6,
        learning_rate=0.05,
        loss_function="MultiClass",
        verbose=False,
        random_seed=42,
    )

    model.fit(
        X_train,
        y_train,
    )

    importance = model.get_feature_importance()

    result = (
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

    print()
    print("=" * 60)
    print("CATBOOST FEATURE IMPORTANCE")
    print("=" * 60)
    print()

    print(
        result.to_string(index=False)
    )

    result.to_csv(
        "feature_importance.csv",
        index=False,
    )

    print()
    print("Saved feature_importance.csv")


if __name__ == "__main__":
    main()