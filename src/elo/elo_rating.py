class EloRating:

    def __init__(
        self,
        initial_rating: float = 1500,
        k_factor: float = 20,
    ):
        self.initial_rating = initial_rating
        self.k_factor = k_factor
        self.ratings = {}

    def get_rating(self, team: str):

        if team not in self.ratings:
            self.ratings[team] = self.initial_rating

        return self.ratings[team]

    def expected_score(
        self,
        home_rating: float,
        away_rating: float,
    ):

        return 1 / (
            1 + 10 ** (
                (away_rating - home_rating) / 400
            )
        )

    def update(
        self,
        home_team: str,
        away_team: str,
        result: float,
    ):

        home = self.get_rating(home_team)
        away = self.get_rating(away_team)

        expected = self.expected_score(
            home,
            away,
        )

        self.ratings[home_team] = (
            home
            + self.k_factor
            * (result - expected)
        )

        self.ratings[away_team] = (
            away
            + self.k_factor
            * (
                (1 - result)
                - (1 - expected)
            )
        )