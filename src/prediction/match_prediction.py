from src.prediction.poisson import PoissonModel


class MatchPrediction:
    def __init__(self):
        self.poisson = PoissonModel()

    def predict(self, home_xg, away_xg):

        matrix = self.poisson.score_matrix(home_xg, away_xg)

        home_win = 0.0
        draw = 0.0
        away_win = 0.0

        for home_goals in range(len(matrix)):
            for away_goals in range(len(matrix[0])):

                p = matrix[home_goals][away_goals]

                if home_goals > away_goals:
                    home_win += p

                elif home_goals == away_goals:
                    draw += p

                else:
                    away_win += p

        return {
            "home_win": round(home_win * 100, 2),
            "draw": round(draw * 100, 2),
            "away_win": round(away_win * 100, 2),
            "matrix": matrix,
        }