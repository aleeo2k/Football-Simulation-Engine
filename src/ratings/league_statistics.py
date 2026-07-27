from collections import defaultdict


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

        league = match["league_id"]

        self.stats[league]["home_xg_sum"] += match["home_xg"]
        self.stats[league]["away_xg_sum"] += match["away_xg"]
        self.stats[league]["matches"] += 1

    def get(self, league_id):

        league = self.stats[league_id]

        if league["matches"] == 0:
            return {
                "home_xg": 1.35,
                "away_xg": 1.15,
                "total_xg": 2.50,
            }

        home = (
            league["home_xg_sum"]
            / league["matches"]
        )

        away = (
            league["away_xg_sum"]
            / league["matches"]
        )

        return {
            "home_xg": home,
            "away_xg": away,
            "total_xg": home + away,
        }