from collections import defaultdict

from src.config import (
    HOME_ADVANTAGE,
    INITIAL_ELO,
    K_FACTOR,
)


class DynamicEloTracker:

    def __init__(
        self,
        initial_elo=INITIAL_ELO,
        home_advantage=HOME_ADVANTAGE,
        k_factor=K_FACTOR,
    ):

        self.initial_elo = initial_elo
        self.home_advantage = home_advantage
        self.k_factor = k_factor

        self.home_rating = defaultdict(
            lambda: self.initial_elo
        )

        self.away_rating = defaultdict(
            lambda: self.initial_elo
        )

    @staticmethod
    def expected_score(
        rating_a,
        rating_b,
    ):

        return 1 / (
            1
            + 10 ** (
                (rating_b - rating_a) / 400
            )
        )

    def update(
        self,
        match,
    ):

        home = match["home_team"]
        away = match["away_team"]

        home_rating = self.home_rating[home]
        away_rating = self.away_rating[away]

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

        self.home_rating[home] += (
            self.k_factor
            * (
                actual_home
                - expected_home
            )
        )

        self.away_rating[away] += (
            self.k_factor
            * (
                actual_away
                - expected_away
            )
        )

    def get_home_rating(
        self,
        team,
    ):

        return self.home_rating[team]

    def get_away_rating(
        self,
        team,
    ):

        return self.away_rating[team]