import io

from contextlib import redirect_stdout

import pandas as pd

from src.evaluation.result_parser import ResultParser
from src.pipeline.xg_feature_builder import XGFeatureBuilder
from src.prediction.match_prediction import MatchPrediction
from src.prediction.ml_expected_goals import MLExpectedGoals

from src.ratings.elo_tracker import EloTracker
from src.ratings.form_tracker import FormTracker
from src.ratings.league_statistics import LeagueStatistics
from src.ratings.rating_tracker import RatingTracker
from src.ratings.rest_tracker import RestTracker
from src.ratings.power_rating import PowerRating
from src.ratings.opponent_strength import OpponentStrength


class FeatureBuilder:

    def __init__(
        self,
        smoothing=5.0,
        form_matches=5,
        home_advantage=70.0,
        k_factor=20.0,
    ):

        self.smoothing = smoothing
        self.form_matches = form_matches
        self.home_advantage = home_advantage
        self.k_factor = k_factor

        self._reset()

    # ==========================================================
    # RESET STATE
    # ==========================================================

    def _reset(self):

        self.tracker = RatingTracker(
            smoothing=self.smoothing,
        )

        self.form = FormTracker(
            form_matches=self.form_matches,
        )

        self.elo = EloTracker(
            home_advantage=self.home_advantage,
            k_factor=self.k_factor,
        )

        self.rest = RestTracker()

        self.power = PowerRating()

        self.opponent_strength = OpponentStrength()

        self.leagues = LeagueStatistics()

        self.xg_builder = XGFeatureBuilder()

        # ------------------------------------------------------
        # OLD MODEL
        #
        # Kept because build() is still used for the historical
        # calibration dataset.
        # ------------------------------------------------------

        self.xg_model = MLExpectedGoals()

        self.predictor = MatchPrediction()

    # ==========================================================
    # BUILD HISTORICAL DATASET
    #
    # THIS IS THE EXISTING PIPELINE.
    # DO NOT CHANGE ITS BEHAVIOUR.
    # ==========================================================

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

            # ==================================================
            # PRE-MATCH ELO
            # ==================================================

            home_elo = self.elo.get_team(
                home_team
            )

            away_elo = self.elo.get_team(
                away_team
            )

            # ==================================================
            # BUILD FEATURES
            # ==================================================

            if (
                self.tracker.has_team(home_team)
                and
                self.tracker.has_team(away_team)
            ):

                home = self.tracker.get_team(
                    home_team
                )

                away = self.tracker.get_team(
                    away_team
                )

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

                home_opponent_strength = (
                    self.opponent_strength.get_team(
                        home_team
                    )
                )

                away_opponent_strength = (
                    self.opponent_strength.get_team(
                        away_team
                    )
                )

                home_rest = self.rest.get_team(
                    home_team,
                    match["date"],
                )

                away_rest = self.rest.get_team(
                    away_team,
                    match["date"],
                )

                home_power = self.power.calculate(
                    team=home,
                    form=home_form,
                    elo=home_elo,
                )

                away_power = self.power.calculate(
                    team=away,
                    form=away_form,
                    elo=away_elo,
                )

                features = self.xg_builder.build(
                    home=home,
                    away=away,
                    league=league,
                    home_form=home_form,
                    away_form=away_form,
                    home_elo=home_elo,
                    away_elo=away_elo,
                    home_rest=home_rest,
                    away_rest=away_rest,
                    home_opponent_strength=(
                        home_opponent_strength
                    ),
                    away_opponent_strength=(
                        away_opponent_strength
                    ),
                    home_power=home_power,
                    away_power=away_power,
                )

                features["_debug"] = (
                    home_team == "Arsenal"
                    and
                    away_team == "Liverpool"
                )

                # ----------------------------------------------
                # OLD MODEL — HISTORICAL DATASET ONLY
                # ----------------------------------------------

                # MLExpectedGoals печатает debug-информацию.
                # Для обычной работы приложения она нам не нужна.
                with redirect_stdout(io.StringIO()):

                    xg = self.xg_model.predict(
                        features
                    )

                    prediction = self.predictor.predict(
                        xg["home_xg"],
                        xg["away_xg"],
                    )

                rows.append(
                    {

                        # ======================================
                        # MATCH
                        # ======================================

                        "game_id":
                            match["game_id"],

                        "league_id":
                            match["league_id"],

                        "date":
                            match["date"],

                        "home_team":
                            home_team,

                        "away_team":
                            away_team,

                        # ======================================
                        # TARGETS
                        # ======================================

                        "home_xg":
                            match["home_xg"],

                        "away_xg":
                            match["away_xg"],

                        # ======================================
                        # POWER
                        # ======================================

                        "home_power":
                            home_power,

                        "away_power":
                            away_power,

                        "power_diff":
                            home_power
                            - away_power,

                        # ======================================
                        # OPPONENT STRENGTH
                        # ======================================

                        "home_opponent_strength":
                            home_opponent_strength,

                        "away_opponent_strength":
                            away_opponent_strength,

                        "opponent_strength_diff":
                            home_opponent_strength
                            - away_opponent_strength,

                        # ======================================
                        # MODEL PREDICTION
                        # ======================================

                        "xg_diff":
                            xg["home_xg"]
                            - xg["away_xg"],

                        "home_win":
                            prediction["home_win"],

                        "draw":
                            prediction["draw"],

                        "away_win":
                            prediction["away_win"],

                        # ======================================
                        # FORM 3
                        # ======================================

                        "home_xg_form_3":
                            home_form[
                                "home_xg_form_3"
                            ],

                        "home_xga_form_3":
                            home_form[
                                "home_xga_form_3"
                            ],

                        "away_xg_form_3":
                            away_form[
                                "away_xg_form_3"
                            ],

                        "away_xga_form_3":
                            away_form[
                                "away_xga_form_3"
                            ],

                        # ======================================
                        # FORM 5
                        # ======================================

                        "home_xg_form_5":
                            home_form[
                                "home_xg_form_5"
                            ],

                        "home_xga_form_5":
                            home_form[
                                "home_xga_form_5"
                            ],

                        "away_xg_form_5":
                            away_form[
                                "away_xg_form_5"
                            ],

                        "away_xga_form_5":
                            away_form[
                                "away_xga_form_5"
                            ],

                        # ======================================
                        # FORM 10
                        # ======================================

                        "home_xg_form_10":
                            home_form[
                                "home_xg_form_10"
                            ],

                        "home_xga_form_10":
                            home_form[
                                "home_xga_form_10"
                            ],

                        "away_xg_form_10":
                            away_form[
                                "away_xg_form_10"
                            ],

                        "away_xga_form_10":
                            away_form[
                                "away_xg_form_10"
                            ],

                        # ======================================
                        # ADJUSTED FORM
                        # ======================================

                        "home_xg_form_3_adj":
                            home_form[
                                "home_xg_form_3_adj"
                            ],

                        "home_xga_form_3_adj":
                            home_form[
                                "home_xga_form_3_adj"
                            ],

                        "away_xg_form_3_adj":
                            away_form[
                                "away_xg_form_3_adj"
                            ],

                        "away_xga_form_3_adj":
                            away_form[
                                "away_xga_form_3_adj"
                            ],

                        # ======================================
                        # OPPONENT LAST 3
                        # ======================================

                        "home_opponent_3":
                            home_form[
                                "home_opponent_3"
                            ],

                        "away_opponent_3":
                            away_form[
                                "away_opponent_3"
                            ],

                        # ======================================
                        # XG FEATURES
                        # ======================================

                        **features,

                        # ======================================
                        # RESULT
                        # ======================================

                        "result":
                            ResultParser.get_result(
                                match["home_goals"],
                                match["away_goals"],
                            ),
                    }
                )

            # ==================================================
            # POST-MATCH UPDATES
            # ==================================================

            self.tracker.update(
                match
            )

            # ==================================================
            # FORM
            # ==================================================

            self.form.update(
                match,
                home_opponent_strength=away_elo,
                away_opponent_strength=home_elo,
            )

            # ==================================================
            # LEAGUE
            # ==================================================

            self.leagues.update(
                match
            )

            # ==================================================
            # ELO
            # ==================================================

            self.elo.update(
                match
            )

            # ==================================================
            # UPDATED ELO FOR OPPONENT STRENGTH
            # ==================================================

            updated_home_elo = self.elo.get_team(
                home_team
            )

            updated_away_elo = self.elo.get_team(
                away_team
            )

            self.opponent_strength.update(
                home_team=home_team,
                away_team=away_team,
                home_elo=updated_home_elo,
                away_elo=updated_away_elo,
            )

            # ==================================================
            # REST
            # ==================================================

            self.rest.update(
                match
            )

        return pd.DataFrame(
            rows
        )

    # ==========================================================
    # BUILD FEATURES FOR ONE FUTURE MATCH
    # ==========================================================

    def build_match(
        self,
        matches: pd.DataFrame,
        home_team: str,
        away_team: str,
        match_date=None,
        league_id=None,
    ):
        """
        Build PRE-MATCH features for a future fixture.

        Important:
        - historical matches are processed chronologically;
        - the future fixture is NEVER added to the trackers;
        - all values therefore represent the state immediately
          before the requested match.
        """

        if len(matches) == 0:
            raise ValueError(
                "No historical matches supplied."
            )

        history = matches.copy()

        history["date"] = pd.to_datetime(
            history["date"]
        )

        history = (
            history
            .sort_values("date")
            .reset_index(drop=True)
        )

        # ------------------------------------------------------
        # Determine future date
        # ------------------------------------------------------

        if match_date is None:

            latest_date = history["date"].max()

            match_date = (
                latest_date
                + pd.Timedelta(days=1)
            )

        else:

            match_date = pd.to_datetime(
                match_date
            )

        # ------------------------------------------------------
        # Determine league
        # ------------------------------------------------------

        if league_id is None:

            league_id = (
                history
                .iloc[-1]["league_id"]
            )

        # ------------------------------------------------------
        # Reset all trackers
        # ------------------------------------------------------

        self._reset()

        # ------------------------------------------------------
        # Process history ONLY.
        #
        # We intentionally call build() here because its
        # post-match update order is the canonical pipeline.
        # We do not use its returned dataset.
        # ------------------------------------------------------

        self.build(
            history
        )

        # ======================================================
        # PRE-MATCH STATE
        # ======================================================

        home_elo = self.elo.get_team(
            home_team
        )

        away_elo = self.elo.get_team(
            away_team
        )

        # ------------------------------------------------------
        # Rating state
        #
        # Cold-start is allowed:
        # if a team has no historical xG data,
        # RatingTracker returns smoothed league-average values.
        # ------------------------------------------------------

        home = self.tracker.get_team(
            home_team
        )

        away = self.tracker.get_team(
            away_team
        )

        # ------------------------------------------------------
        # League
        # ------------------------------------------------------

        league = self.leagues.get(
            league_id
        )

        # ------------------------------------------------------
        # Form
        # ------------------------------------------------------

        home_form = self.form.get_team(
            home_team,
            home,
        )

        away_form = self.form.get_team(
            away_team,
            away,
        )

        # ------------------------------------------------------
        # Opponent strength
        # ------------------------------------------------------

        home_opponent_strength = (
            self.opponent_strength.get_team(
                home_team
            )
        )

        away_opponent_strength = (
            self.opponent_strength.get_team(
                away_team
            )
        )

        # ------------------------------------------------------
        # Rest
        # ------------------------------------------------------

        home_rest = self.rest.get_team(
            home_team,
            match_date,
        )

        away_rest = self.rest.get_team(
            away_team,
            match_date,
        )

        # ------------------------------------------------------
        # Power
        # ------------------------------------------------------

        home_power = self.power.calculate(
            team=home,
            form=home_form,
            elo=home_elo,
        )

        away_power = self.power.calculate(
            team=away,
            form=away_form,
            elo=away_elo,
        )

        # ======================================================
        # OLD / BASE XG FEATURES
        # ======================================================

        features = self.xg_builder.build(
            home=home,
            away=away,
            league=league,
            home_form=home_form,
            away_form=away_form,
            home_elo=home_elo,
            away_elo=away_elo,
            home_rest=home_rest,
            away_rest=away_rest,
            home_opponent_strength=(
                home_opponent_strength
            ),
            away_opponent_strength=(
                away_opponent_strength
            ),
            home_power=home_power,
            away_power=away_power,
        )

        # ======================================================
        # ADD FULL REASONABLE FEATURES
        # ======================================================

        features.update({

            # --------------------------------------------------
            # Form 3
            # --------------------------------------------------

            "home_xg_form_3":
                home_form[
                    "home_xg_form_3"
                ],

            "home_xga_form_3":
                home_form[
                    "home_xga_form_3"
                ],

            "away_xg_form_3":
                away_form[
                    "away_xg_form_3"
                ],

            "away_xga_form_3":
                away_form[
                    "away_xga_form_3"
                ],

            # --------------------------------------------------
            # Form 5
            # --------------------------------------------------

            "home_xg_form_5":
                home_form[
                    "home_xg_form_5"
                ],

            "home_xga_form_5":
                home_form[
                    "home_xga_form_5"
                ],

            "away_xg_form_5":
                away_form[
                    "away_xg_form_5"
                ],

            "away_xga_form_5":
                away_form[
                    "away_xga_form_5"
                ],

            # --------------------------------------------------
            # Form 10
            # --------------------------------------------------

            "home_xg_form_10":
                home_form[
                    "home_xg_form_10"
                ],

            "home_xga_form_10":
                home_form[
                    "home_xga_form_10"
                ],

            "away_xg_form_10":
                away_form[
                    "away_xg_form_10"
                ],

            "away_xga_form_10":
                away_form[
                    "away_xga_form_10"
                ],

            # --------------------------------------------------
            # Strength-adjusted Form 3
            # --------------------------------------------------

            "home_xg_form_3_adj":
                home_form[
                    "home_xg_form_3_adj"
                ],

            "home_xga_form_3_adj":
                home_form[
                    "home_xga_form_3_adj"
                ],

            "away_xg_form_3_adj":
                away_form[
                    "away_xg_form_3_adj"
                ],

            "away_xga_form_3_adj":
                away_form[
                    "away_xga_form_3_adj"
                ],

            # --------------------------------------------------
            # Opponent strength — last 3
            # --------------------------------------------------

            "home_opponent_3":
                home_form[
                    "home_opponent_3"
                ],

            "away_opponent_3":
                away_form[
                    "away_opponent_3"
                ],
        })

        # ======================================================
        # SAFETY CHECK
        # ======================================================

        required_features = [

            "home_attack",
            "away_attack",

            "home_defence",
            "away_defence",

            "attack_diff",
            "defence_diff",

            "league_home_xg",
            "league_away_xg",
            "league_total_xg",

            "home_attack_delta",
            "home_defence_delta",

            "away_attack_delta",
            "away_defence_delta",

            "home_elo",
            "away_elo",
            "elo_diff",

            "home_rest_days",
            "away_rest_days",
            "rest_diff",

            "home_power",
            "away_power",
            "power_diff",

            "home_xg_form_3",
            "home_xga_form_3",
            "away_xg_form_3",
            "away_xga_form_3",

            "home_opponent_3",
            "away_opponent_3",

            "home_xg_form_5",
            "home_xga_form_5",
            "away_xg_form_5",
            "away_xga_form_5",

            "home_xg_form_10",
            "home_xga_form_10",
            "away_xg_form_10",
            "away_xga_form_10",

            "home_xg_form_3_adj",
            "home_xga_form_3_adj",
            "away_xg_form_3_adj",
            "away_xga_form_3_adj",
        ]

        missing = [
            feature
            for feature in required_features
            if feature not in features
        ]

        if missing:

            raise ValueError(
                "Missing FULL REASONABLE "
                "features:\n"
                + "\n".join(missing)
            )

        # ======================================================
        # RETURN
        # ======================================================

        return {
            feature: features[feature]
            for feature in required_features
        }   