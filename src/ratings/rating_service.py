import pandas as pd


class RatingService:
    def __init__(self, matches: pd.DataFrame):
        self.matches = matches.copy()

    def team_statistics(self):

        matches = self.matches.copy()

        matches["date"] = pd.to_datetime(matches["date"])

        latest = matches["date"].max()

        matches["days_old"] = (latest - matches["date"]).dt.days
        matches["weight"] = 0.998 ** matches["days_old"]

        teams = []

        for team in sorted(
            set(matches.home_team).union(matches.away_team)
        ):

            home = matches[matches.home_team == team]
            away = matches[matches.away_team == team]

            def weighted(series, weight):
                if len(series) == 0:
                    return 0
                return (series * weight).sum() / weight.sum()

            teams.append(
                {
                    "team": team,

                    "home_attack": weighted(
                        home.home_xg,
                        home.weight
                    ),

                    "home_defence": weighted(
                        home.away_xg,
                        home.weight
                    ),

                    "away_attack": weighted(
                        away.away_xg,
                        away.weight
                    ),

                    "away_defence": weighted(
                        away.home_xg,
                        away.weight
                    ),

                    "matches": len(home) + len(away),
                }
            )

        ratings = pd.DataFrame(teams).set_index("team")

        ratings["attack"] = (
            ratings["home_attack"] +
            ratings["away_attack"]
        ) / 2

        ratings["defence"] = (
            ratings["home_defence"] +
            ratings["away_defence"]
        ) / 2

        league_attack = ratings.attack.mean()
        league_defence = ratings.defence.mean()

        ratings["attack_strength"] = (
            ratings.attack / league_attack
        )

        ratings["defence_strength"] = (
            ratings.defence / league_defence
        )

        return ratings.sort_values(
            "attack_strength",
            ascending=False
        )