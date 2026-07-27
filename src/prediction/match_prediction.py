import math

from src.prediction.dixon_coles import DixonColes
from src.prediction.poisson import PoissonModel


class MatchPrediction:

    def __init__(
        self,
        use_dixon_coles: bool = True,
        rho: float = -0.10,
    ):
        self.poisson = PoissonModel()
        self.use_dixon_coles = use_dixon_coles
        self.dixon_coles = DixonColes(rho)

    def predict(self, home_xg, away_xg):

        matrix = self.poisson.score_matrix(
            home_xg,
            away_xg,
        )

        home_win = 0.0
        draw = 0.0
        away_win = 0.0

        scores = []

        for home_goals in range(len(matrix)):

            for away_goals in range(len(matrix[0])):

                p = matrix[home_goals][away_goals]

                if self.use_dixon_coles:
                    p *= self.dixon_coles.correction(
                        home_goals,
                        away_goals,
                        home_xg,
                        away_xg,
                    )

                if (
                    math.isnan(p)
                    or math.isinf(p)
                    or p < 0
                ):
                    p = 0.0

                scores.append(
                    {
                        "score": f"{home_goals}:{away_goals}",
                        "probability": p,
                    }
                )

                if home_goals > away_goals:
                    home_win += p

                elif home_goals == away_goals:
                    draw += p

                else:
                    away_win += p

        total = home_win + draw + away_win

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

        home_win /= total
        draw /= total
        away_win /= total

        for score in scores:
            score["probability"] /= total

        scores.sort(
            key=lambda x: x["probability"],
            reverse=True,
        )

        return {
            "home_win": home_win,
            "draw": draw,
            "away_win": away_win,
            "top_scores": scores[:5],
        }