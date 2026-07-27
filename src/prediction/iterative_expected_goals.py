import pandas as pd


class IterativeExpectedGoalsModel:

    def __init__(self, ratings: pd.DataFrame):
        self.ratings = ratings

    def predict(
        self,
        home_team: str,
        away_team: str,
    ):

        home = self.ratings.loc[home_team]
        away = self.ratings.loc[away_team]

        league_attack = self.ratings["attack"].mean()

        home_xg = (
            home["attack"]
            / away["defence"]
            * league_attack
        )

        away_xg = (
            away["attack"]
            / home["defence"]
            * league_attack
        )

        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_xg": round(home_xg, 2),
            "away_xg": round(away_xg, 2),
        }