import pandas as pd


class ExpectedGoalsModel:
    def __init__(self, ratings: pd.DataFrame):
        self.ratings = ratings

    def predict(self, home_team: str, away_team: str):

        home = self.ratings.loc[home_team]
        away = self.ratings.loc[away_team]

        league_avg = self.ratings["attack"].mean()

        home_xg = (
            home["home_attack"]
            * away["away_defence"]
            / league_avg
        )

        away_xg = (
            away["away_attack"]
            * home["home_defence"]
            / league_avg
        )

        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_xg": round(home_xg, 2),
            "away_xg": round(away_xg, 2),
        }