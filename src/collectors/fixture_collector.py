import soccerdata as sd


class FixtureCollector:

    def __init__(self):

        self.sofascore = sd.Sofascore(
            leagues="ENG-Premier League",
            seasons=["2026"],
        )

    def get_matches(self):

        df = self.sofascore.read_schedule()

        df = df.reset_index()

        required_columns = [
            "date",
            "home_team",
            "away_team",
            "home_score",
            "away_score",
            "game_id",
            "round",
            "week",
        ]

        missing = [
            column
            for column in required_columns
            if column not in df.columns
        ]

        if missing:
            raise ValueError(
                "Missing Sofascore columns: "
                + ", ".join(missing)
            )

        return df[
            required_columns
        ].copy()