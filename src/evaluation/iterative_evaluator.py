import pandas as pd

from src.evaluation.result_parser import ResultParser
from src.prediction.iterative_expected_goals import IterativeExpectedGoalsModel
from src.prediction.match_prediction import MatchPrediction
from src.ratings.iterative_rating import IterativeRating


class IterativeEvaluator:

    def __init__(self, matches: pd.DataFrame):

        self.matches = (
            matches
            .sort_values("date")
            .reset_index(drop=True)
        )

    def evaluate_match(self, index: int):

        if index <= 0:
            raise ValueError("Index must be greater than 0.")

        history = self.matches.iloc[:index]
        match = self.matches.iloc[index]

        ratings = IterativeRating(
            history
        ).calculate()

        home_team = match["home_team"]
        away_team = match["away_team"]

        if (
            home_team not in ratings.index
            or away_team not in ratings.index
        ):
            return None

        xg = IterativeExpectedGoalsModel(
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
            "predicted": predicted,
            "actual": actual,
            "home_win": prediction["home_win"],
            "draw": prediction["draw"],
            "away_win": prediction["away_win"],
        }