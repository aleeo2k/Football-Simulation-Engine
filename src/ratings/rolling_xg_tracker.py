from collections import defaultdict, deque


class RollingXGTracker:

    def __init__(
        self,
        window: int = 5,
        default_xg: float = 1.35,
    ):

        self.window = window
        self.default_xg = default_xg

        self.home_xg = defaultdict(
            lambda: deque(maxlen=self.window)
        )

        self.away_xg = defaultdict(
            lambda: deque(maxlen=self.window)
        )

    def update(self, match):

        self.home_xg[
            match["home_team"]
        ].append(
            match["home_xg"]
        )

        self.away_xg[
            match["away_team"]
        ].append(
            match["away_xg"]
        )

    def average(
        self,
        values,
    ):

        if len(values) == 0:
            return self.default_xg

        return sum(values) / len(values)

    def get_team(
        self,
        team,
    ):

        return {

            "home_recent_xg":
                self.average(
                    self.home_xg[team]
                ),

            "away_recent_xg":
                self.average(
                    self.away_xg[team]
                ),
        }