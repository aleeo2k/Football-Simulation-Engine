import pandas as pd

from src.evaluation.result_parser import ResultParser
from src.prediction.expected_goals import ExpectedGoalsModel
from src.prediction.match_prediction import MatchPrediction
from src.ratings.rating_service import RatingService


class Evaluator:

    def __init__(
        self,
        matches: pd.DataFrame,
        recency_decay: float = 0.998,
    ):

        self.matches = (
            matches
            .sort_values("date")
            .reset_index(drop=True)
        )

        self.recency_decay = recency_decay

    def evaluate_match(self, index: int):

        if index <= 0:
            raise ValueError("Index must be greater than 0.")

        history = self.matches.iloc[:index]

        match = self.matches.iloc[index]

        ratings = RatingService(
            history,
            self.recency_decay,
        ).team_statistics()

        home_team = match["home_team"]
        away_team = match["away_team"]

        if (
            home_team not in ratings.index
            or
            away_team not in ratings.index
        ):
            return None

        xg = ExpectedGoalsModel(
            ratings
        ).predict(
            home_team,
            away_team,
        )

        prediction = MatchPrediction().predict(
            xg["home_xg"],
            xg["away_xg"],
        )

        predicted = max(
            [
                ("H", prediction["home_win"]),
                ("D", prediction["draw"]),
                ("A", prediction["away_win"]),
            ],
            key=lambda x: x[1],
        )[0]

        actual = ResultParser.get_result(
            match["home_goals"],
            match["away_goals"],
        )

        return {
            "date": match["date"],
            "home_team": home_team,
            "away_team": away_team,
            "predicted": predicted,
            "actual": actual,
            "home_win": prediction["home_win"],
            "draw": prediction["draw"],
            "away_win": prediction["away_win"],
        }