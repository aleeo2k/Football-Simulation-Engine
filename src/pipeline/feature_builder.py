import pandas as pd

from src.evaluation.result_parser import ResultParser
from src.prediction.expected_goals import ExpectedGoalsModel
from src.prediction.match_prediction import MatchPrediction
from src.ratings.elo_tracker import EloTracker
from src.ratings.form_tracker import FormTracker
from src.ratings.league_statistics import LeagueStatistics
from src.ratings.rating_tracker import RatingTracker
from src.ratings.rest_tracker import RestTracker


class FeatureBuilder:

    def __init__(
        self,
        smoothing=5.0,
        form_matches=5,
        home_advantage=70.0,
        k_factor=20.0,
    ):

        self.tracker = RatingTracker(
            smoothing=smoothing,
        )

        self.form = FormTracker(
            form_matches=form_matches,
        )

        self.elo = EloTracker(
            home_advantage=home_advantage,
            k_factor=k_factor,
        )

        self.rest = RestTracker()

        self.leagues = LeagueStatistics()

        self.xg_model = ExpectedGoalsModel()
        self.predictor = MatchPrediction()

    def build(
        self,
        matches: pd.DataFrame,
    ):

        rows = []

        matches = (
            matches
            .sort_values("date")
            .reset_index(drop=True)
        )

        for _, match in matches.iterrows():

            home_team = match["home_team"]
            away_team = match["away_team"]

            if (
                self.tracker.has_team(home_team)
                and
                self.tracker.has_team(away_team)
            ):

                home = self.tracker.get_team(home_team)
                away = self.tracker.get_team(away_team)

                league = self.leagues.get(
                    match["league_id"]
                )

                home_form = self.form.get_team(
                    home_team,
                    home,
                )

                away_form = self.form.get_team(
                    away_team,
                    away,
                )

                xg = self.xg_model.predict(
                    home=home,
                    away=away,
                    league=league,
                    home_team=home_team,
                    away_team=away_team,
                )

                prediction = self.predictor.predict(
                    xg["home_xg"],
                    xg["away_xg"],
                )

                home_elo = self.elo.get_team(
                    home_team
                )

                away_elo = self.elo.get_team(
                    away_team
                )

                home_rest = self.rest.get_team(
                    home_team,
                    match["date"],
                )

                away_rest = self.rest.get_team(
                    away_team,
                    match["date"],
                )

                rows.append(
                    {

                        "home_xg": xg["home_xg"],
                        "away_xg": xg["away_xg"],
                        "xg_diff":
                            xg["home_xg"]
                            - xg["away_xg"],

                        "home_win":
                            prediction["home_win"],

                        "draw":
                            prediction["draw"],

                        "away_win":
                            prediction["away_win"],

                        "home_attack":
                            home["home_attack"],

                        "away_attack":
                            away["away_attack"],

                        "home_defence":
                            home["home_defence"],

                        "away_defence":
                            away["away_defence"],

                        "attack_diff":
                            home["home_attack"]
                            - away["away_attack"],

                        "defence_diff":
                            away["away_defence"]
                            - home["home_defence"],

                        "league_home_xg":
                            league["home_xg"],

                        "league_away_xg":
                            league["away_xg"],

                        "league_total_xg":
                            league["total_xg"],

                        "home_attack_delta":
                            home_form["attack_delta"],

                        "home_defence_delta":
                            home_form["defence_delta"],

                        "away_attack_delta":
                            away_form["away_attack_delta"],

                        "away_defence_delta":
                            away_form["away_defence_delta"],

                        "home_elo":
                            home_elo,

                        "away_elo":
                            away_elo,

                        "elo_diff":
                            home_elo
                            - away_elo,

                        "home_rest_days":
                            home_rest,

                        "away_rest_days":
                            away_rest,

                        "rest_diff":
                            home_rest
                            - away_rest,

                        "result":
                            ResultParser.get_result(
                                match["home_goals"],
                                match["away_goals"],
                            ),
                    }
                )

            self.tracker.update(match)
            self.form.update(match)
            self.leagues.update(match)
            self.elo.update(match)
            self.rest.update(match)

        return pd.DataFrame(rows)