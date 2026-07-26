import math


class PoissonModel:

    @staticmethod
    def probability(expected_goals: float, goals: int) -> float:
        """
        Вероятность забить goals голов
        при ожидаемых голах expected_goals.
        """

        return (
            math.exp(-expected_goals)
            * expected_goals ** goals
            / math.factorial(goals)
        )

    def score_matrix(
        self,
        home_xg: float,
        away_xg: float,
        max_goals: int = 7,
    ):

        matrix = []

        for home_goals in range(max_goals + 1):

            row = []

            for away_goals in range(max_goals + 1):

                p = (
                    self.probability(home_xg, home_goals)
                    * self.probability(away_xg, away_goals)
                )

                row.append(p)

            matrix.append(row)

        return matrix