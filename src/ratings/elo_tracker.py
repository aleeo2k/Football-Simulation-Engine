from collections import defaultdict, deque

from src.config import (
    HOME_ADVANTAGE,
    INITIAL_ELO,
    K_FACTOR,
)


class EloTracker:

    def __init__(
        self,
        initial_elo: float = INITIAL_ELO,
        home_advantage: float = HOME_ADVANTAGE,
        k_factor: float = K_FACTOR,
        schedule_window: int = 10,
    ):

        self.initial_elo = initial_elo
        self.home_advantage = home_advantage
        self.k_factor = k_factor

        self.ratings = defaultdict(
            lambda: self.initial_elo
        )

        self.opponents = defaultdict(
            lambda: deque(maxlen=schedule_window)
        )

    @staticmethod
    def expected_score(
        rating_a,
        rating_b,
    ):

        return 1 / (
            1 +
            10 ** (
                (rating_b - rating_a) / 400
            )
        )

    def update(self, match):

        home = match["home_team"]
        away = match["away_team"]

        home_rating = self.ratings[home]
        away_rating = self.ratings[away]

        self.opponents[home].append(
            away_rating
        )

        self.opponents[away].append(
            home_rating
        )

        expected_home = self.expected_score(
            home_rating + self.home_advantage,
            away_rating,
        )

        expected_away = 1 - expected_home

        if match["home_goals"] > match["away_goals"]:

            actual_home = 1.0
            actual_away = 0.0

        elif match["home_goals"] < match["away_goals"]:

            actual_home = 0.0
            actual_away = 1.0

        else:

            actual_home = 0.5
            actual_away = 0.5

        self.ratings[home] += (
            self.k_factor
            *
            (
                actual_home
                - expected_home
            )
        )

        self.ratings[away] += (
            self.k_factor
            *
            (
                actual_away
                - expected_away
            )
        )

    def get_team(
        self,
        team,
    ):

        return self.ratings[team]

    def get_schedule_strength(
        self,
        team,
    ):

        games = self.opponents[team]

        if len(games) == 0:
            return self.initial_elo

        return sum(games) / len(games)

    def has_team(
        self,
        team,
    ):

        return team in self.ratings