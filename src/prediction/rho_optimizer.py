import numpy as np

from src.prediction.dixon_coles import DixonColes
from src.prediction.poisson import PoissonModel


class RhoOptimizer:

    def __init__(self):

        self.poisson = PoissonModel()

    def score(self, matches, rho):

        dc = DixonColes(rho)

        log_likelihood = 0.0

        for match in matches:

            matrix = self.poisson.score_matrix(
                match["home_xg"],
                match["away_xg"],
            )

            home = min(match["home_goals"], len(matrix) - 1)
            away = min(match["away_goals"], len(matrix[0]) - 1)

            probability = (
                matrix[home][away]
                * dc.correction(
                    home,
                    away,
                    match["home_xg"],
                    match["away_xg"],
                )
            )

            probability = max(probability, 1e-12)

            log_likelihood += np.log(probability)

        return log_likelihood

    def optimize(self, matches):

        best_rho = -0.10
        best_score = float("-inf")

        for rho in np.arange(-0.25, 0.051, 0.01):

            score = self.score(matches, rho)

            if score > best_score:
                best_score = score
                best_rho = float(rho)

        return best_rho