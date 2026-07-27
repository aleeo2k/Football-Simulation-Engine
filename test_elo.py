import pandas as pd

from src.database.database import Database
from src.elo.elo_rating import EloRating


def main():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches ORDER BY date",
        db.engine,
    )

    elo = EloRating()

    for _, match in matches.iterrows():

        if match["home_goals"] > match["away_goals"]:
            result = 1.0

        elif match["home_goals"] < match["away_goals"]:
            result = 0.0

        else:
            result = 0.5

        elo.update(
            match["home_team"],
            match["away_team"],
            result,
        )

    ratings = sorted(
        elo.ratings.items(),
        key=lambda x: x[1],
        reverse=True,
    )

    print("\nTop 20 Elo Ratings\n")

    for team, rating in ratings[:20]:
        print(
            f"{team:<30} {rating:.1f}"
        )


if __name__ == "__main__":
    main()