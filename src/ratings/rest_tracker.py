from collections import defaultdict

import pandas as pd


class RestTracker:

    def __init__(self):

        self.last_match = defaultdict(
            lambda: None
        )

    def update(self, match):

        date = pd.to_datetime(
            match["date"]
        )

        self.last_match[
            match["home_team"]
        ] = date

        self.last_match[
            match["away_team"]
        ] = date

    def get_team(
        self,
        team,
        current_date,
    ):

        current_date = pd.to_datetime(
            current_date
        )

        last = self.last_match[team]

        if last is None:

            return 7

        days = (
            current_date
            - last
        ).days

        if days < 0:
            days = 0

        return days

    def has_team(
        self,
        team,
    ):

        return (
            self.last_match[team]
            is not None
        )