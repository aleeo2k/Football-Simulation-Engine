from collections import defaultdict, deque


class ScheduleStrengthTracker:

    def __init__(
        self,
        window: int = 10,
        initial_rating: float = 1500.0,
    ):

        self.window = window
        self.initial_rating = initial_rating

        self.opponents = defaultdict(
            lambda: deque(maxlen=self.window)
        )

    def update(
        self,
        home_team,
        away_team,
        home_elo,
        away_elo,
    ):

        self.opponents[home_team].append(
            away_elo
        )

        self.opponents[away_team].append(
            home_elo
        )

    def get_team(
        self,
        team,
    ):

        games = self.opponents[team]

        if len(games) == 0:
            return self.initial_rating

        return sum(games) / len(games)

    def has_team(
        self,
        team,
    ):

        return len(
            self.opponents[team]
        ) > 0