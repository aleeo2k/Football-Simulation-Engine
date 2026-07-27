import pandas as pd

from src.evaluation.result_parser import ResultParser
from src.prediction.expected_goals import ExpectedGoalsModel
from src.prediction.match_prediction import MatchPrediction
from src.ratings.league_statistics import LeagueStatistics
from src.ratings.rating_tracker import RatingTracker


class FastEvaluator:

    def __init__(self, matches: pd.DataFrame):

        self.matches = (
            matches
            .sort_values("date")
            .reset_index(drop=True)
        )

        self.tracker = RatingTracker()
        self.leagues = LeagueStatistics()

        self.xg_model = ExpectedGoalsModel()
        self.predictor = MatchPrediction()

    def evaluate(self):

        results = []

        for _, match in self.matches.iterrows():

            home_team = match["home_team"]
            away_team = match["away_team"]

            if (
                self.tracker.has_team(home_team)
                and self.tracker.has_team(away_team)
            ):

                home = self.tracker.get_team(home_team)
                away = self.tracker.get_team(away_team)

                league = self.leagues.get(
                    match["league_id"]
                )

                prediction_xg = self.xg_model.predict(
                    home=home,
                    away=away,
                    league=league,
                    home_team=home_team,
                    away_team=away_team,
                )

                prediction = self.predictor.predict(
                    prediction_xg["home_xg"],
                    prediction_xg["away_xg"],
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

                results.append(
                    {
                        "predicted": predicted,
                        "actual": actual,
                        "home_win": prediction["home_win"],
                        "draw": prediction["draw"],
                        "away_win": prediction["away_win"],
                    }
                )

            self.tracker.update(match)
            self.leagues.update(match)

        return results