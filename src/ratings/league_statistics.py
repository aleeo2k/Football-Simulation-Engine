from collections import defaultdict

import pandas as pd

from src.config import (
    DEFAULT_AWAY_XG,
    DEFAULT_HOME_XG,
)


class LeagueStatistics:

    def __init__(self):

        self.stats = defaultdict(
            lambda: {
                "home_xg_sum": 0.0,
                "away_xg_sum": 0.0,
                "matches": 0,
            }
        )

    def update(self, match):

        home_xg = match["home_xg"]
        away_xg = match["away_xg"]

        if (
            pd.isna(home_xg)
            or
            pd.isna(away_xg)
        ):
            return

        league = match["league_id"]

        self.stats[league]["home_xg_sum"] += home_xg
        self.stats[league]["away_xg_sum"] += away_xg
        self.stats[league]["matches"] += 1

    def get(self, league_id):

        league = self.stats[league_id]

        if league["matches"] == 0:

            return {

                "home_xg":
                    DEFAULT_HOME_XG,

                "away_xg":
                    DEFAULT_AWAY_XG,

                "total_xg":
                    DEFAULT_HOME_XG
                    +
                    DEFAULT_AWAY_XG,
            }

        home = (
            league["home_xg_sum"]
            /
            league["matches"]
        )

        away = (
            league["away_xg_sum"]
            /
            league["matches"]
        )

        if pd.isna(home):
            home = DEFAULT_HOME_XG

        if pd.isna(away):
            away = DEFAULT_AWAY_XG

        return {

            "home_xg":
                home,

            "away_xg":
                away,

            "total_xg":
                home + away,
        }