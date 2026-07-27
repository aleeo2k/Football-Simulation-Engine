import pandas as pd

from src.database.database import Database
from src.ratings.iterative_rating import IterativeRating


def main():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches",
        db.engine,
    )

    ratings = IterativeRating(matches).calculate()

    print("\nTop 20 Attack\n")

    print(
        ratings
        .sort_values("attack", ascending=False)
        .head(20)
    )

    print("\nTop 20 Defence\n")

    print(
        ratings
        .sort_values("defence")
        .head(20)
    )


if __name__ == "__main__":
    main()
    