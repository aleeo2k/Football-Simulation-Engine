import pandas as pd

from src.database.database import Database
from src.prediction.expected_goals import ExpectedGoalsModel
from src.prediction.match_prediction import MatchPrediction
from src.ratings.rating_service import RatingService


class PredictionService:

    def __init__(self):

        db = Database()

        self.matches = pd.read_sql(
            "SELECT * FROM matches",
            db.engine,
        )

        self.ratings = RatingService(
            self.matches
        ).team_statistics()

        self.xg_model = ExpectedGoalsModel(
            self.ratings
        )

        self.predictor = MatchPrediction()

    def get_teams(self):

        return sorted(
            self.ratings.index.tolist()
        )

    def predict(
        self,
        home_team,
        away_team,
    ):

        xg = self.xg_model.predict(
            home_team,
            away_team,
        )

        prediction = self.predictor.predict(
            xg["home_xg"],
            xg["away_xg"],
        )

        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_xg": xg["home_xg"],
            "away_xg": xg["away_xg"],
            **prediction,
        }