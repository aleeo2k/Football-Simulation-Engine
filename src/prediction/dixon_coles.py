class DixonColes:

    def __init__(self, rho: float = -0.10):
        self.rho = rho

    def correction(
        self,
        home_goals: int,
        away_goals: int,
        home_xg: float,
        away_xg: float,
    ):

        if home_goals == 0 and away_goals == 0:
            return 1 - home_xg * away_xg * self.rho

        if home_goals == 0 and away_goals == 1:
            return 1 + home_xg * self.rho

        if home_goals == 1 and away_goals == 0:
            return 1 + away_xg * self.rho

        if home_goals == 1 and away_goals == 1:
            return 1 - self.rho

        return 1.0