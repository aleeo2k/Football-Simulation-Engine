from collections import defaultdict, deque


class OpponentStrength:

    def __init__(self, matches=5):

        self.matches = matches

        self.history = defaultdict(
            lambda: deque(maxlen=matches)
        )

    def update(
        self,
        home_team,
        away_team,
        home_elo,
        away_elo,
    ):

        self.history[home_team].append(
            away_elo
        )

        self.history[away_team].append(
            home_elo
        )

    def average(
        self,
        team,
    ):

        values = self.history[team]

        if len(values) == 0:
            return 1500.0

        return sum(values) / len(values)

    def get_team(
        self,
        team,
    ):

        return self.average(team)