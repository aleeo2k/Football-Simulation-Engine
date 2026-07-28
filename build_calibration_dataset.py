import pandas as pd

from src.database.database import Database
from src.pipeline.feature_builder import FeatureBuilder


def main():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches ORDER BY date",
        db.engine,
    )

    builder = FeatureBuilder()

    dataset = builder.build(
        matches
    )

    dataset.to_csv(
        "calibration_dataset.csv",
        index=False,
    )

    print(dataset.head())

    print()

    print(
        f"Rows: {len(dataset)}"
    )


if __name__ == "__main__":
    main()