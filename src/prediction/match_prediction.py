import math
from pathlib import Path

import joblib
import numpy as np

from src.prediction.dixon_coles import DixonColes
from src.prediction.poisson import PoissonModel


class MatchPrediction:

    def __init__(
        self,
        use_dixon_coles: bool = True,
        rho: float = -0.10,
        use_calibration: bool = True,
    ):

        self.poisson = PoissonModel()

        self.use_dixon_coles = (
            use_dixon_coles
        )

        self.dixon_coles = DixonColes(
            rho
        )

        self.use_calibration = (
            use_calibration
        )

        self.calibrator = None

        if self.use_calibration:

            models_dir = (
                Path(__file__)
                .resolve()
                .parents[2]
                / "models"
            )

            calibrator_path = (
                models_dir
                / "probability_calibrator.pkl"
            )

            if calibrator_path.exists():

                self.calibrator = (
                    joblib.load(
                        calibrator_path
                    )
                )

    # =====================================================
    # CALIBRATION
    # =====================================================

    def _calibrate(
        self,
        home_win,
        draw,
        away_win,
    ):

        if self.calibrator is None:

            return (
                home_win,
                draw,
                away_win,
            )

        probabilities = np.array([[
            home_win,
            draw,
            away_win,
        ]])

        probabilities = np.clip(
            probabilities,
            1e-8,
            1.0 - 1e-8,
        )

        log_features = np.log(
            probabilities[:, :2]
            / probabilities[:, [2]]
        )

        calibrated = (
            self.calibrator
            .predict_proba(
                log_features
            )[0]
        )

        calibrated = np.clip(
            calibrated,
            0.0,
            1.0,
        )

        total = calibrated.sum()

        if (
            total <= 0
            or math.isnan(total)
            or math.isinf(total)
        ):

            return (
                home_win,
                draw,
                away_win,
            )

        calibrated /= total

        return (
            float(calibrated[0]),
            float(calibrated[1]),
            float(calibrated[2]),
        )

    # =====================================================
    # PREDICT
    # =====================================================

    def predict(
        self,
        home_xg,
        away_xg,
    ):

        matrix = (
            self.poisson.score_matrix(
                home_xg,
                away_xg,
            )
        )

        home_win = 0.0
        draw = 0.0
        away_win = 0.0

        scores = []

        for home_goals in range(
            len(matrix)
        ):

            for away_goals in range(
                len(matrix[0])
            ):

                p = matrix[
                    home_goals
                ][
                    away_goals
                ]

                if self.use_dixon_coles:

                    p *= (
                        self.dixon_coles
                        .correction(
                            home_goals,
                            away_goals,
                            home_xg,
                            away_xg,
                        )
                    )

                if (
                    math.isnan(p)
                    or math.isinf(p)
                    or p < 0
                ):

                    p = 0.0

                scores.append({
                    "score":
                        f"{home_goals}:{away_goals}",

                    "probability":
                        p,
                })

                if (
                    home_goals
                    > away_goals
                ):

                    home_win += p

                elif (
                    home_goals
                    == away_goals
                ):

                    draw += p

                else:

                    away_win += p

        total = (
            home_win
            + draw
            + away_win
        )

        if (
            total <= 0
            or math.isnan(total)
            or math.isinf(total)
        ):

            return {
                "home_win": 1 / 3,
                "draw": 1 / 3,
                "away_win": 1 / 3,
                "top_scores": [],
            }

        # -------------------------------------------------
        # RAW PROBABILITIES
        # -------------------------------------------------

        home_win /= total
        draw /= total
        away_win /= total

        # -------------------------------------------------
        # CALIBRATION
        # -------------------------------------------------

        (
            home_win,
            draw,
            away_win,
        ) = self._calibrate(
            home_win,
            draw,
            away_win,
        )

        # -------------------------------------------------
        # SCORE PROBABILITIES
        #
        # These remain RAW Dixon-Coles score probabilities.
        # Calibration is applied only to H/D/A.
        # -------------------------------------------------

        for score in scores:

            score["probability"] /= total

        scores.sort(
            key=lambda x:
                x["probability"],
            reverse=True,
        )

        return {
            "home_win": home_win,
            "draw": draw,
            "away_win": away_win,
            "top_scores": scores[:5],
        }