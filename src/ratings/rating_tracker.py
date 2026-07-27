from collections import defaultdict


SMOOTHING = 5.0
LEAGUE_AVERAGE = 1.35


class RatingTracker:

    def __init__(self):

        self.stats = defaultdict(
            lambda: {
                "home_attack_sum": 0.0,
                "home_attack_weight": 0.0,

                "home_defence_sum": 0.0,
                "home_defence_weight": 0.0,

                "away_attack_sum": 0.0,
                "away_attack_weight": 0.0,

                "away_defence_sum": 0.0,
                "away_defence_weight": 0.0,
            }
        )

    def update(self, match):

        home = self.stats[match["home_team"]]
        away = self.stats[match["away_team"]]

        home["home_attack_sum"] += match["home_xg"]
        home["home_attack_weight"] += 1

        home["home_defence_sum"] += match["away_xg"]
        home["home_defence_weight"] += 1

        away["away_attack_sum"] += match["away_xg"]
        away["away_attack_weight"] += 1

        away["away_defence_sum"] += match["home_xg"]
        away["away_defence_weight"] += 1

    def smoothed_average(
        self,
        total,
        games,
    ):

        return (
            total
            + SMOOTHING * LEAGUE_AVERAGE
        ) / (
            games
            + SMOOTHING
        )

    def get_team(self, team):

        s = self.stats[team]

        home_attack = self.smoothed_average(
            s["home_attack_sum"],
            s["home_attack_weight"],
        )

        away_attack = self.smoothed_average(
            s["away_attack_sum"],
            s["away_attack_weight"],
        )

        home_defence = self.smoothed_average(
            s["home_defence_sum"],
            s["home_defence_weight"],
        )

        away_defence = self.smoothed_average(
            s["away_defence_sum"],
            s["away_defence_weight"],
        )

        attack = (
            home_attack
            + away_attack
        ) / 2

        defence = (
            home_defence
            + away_defence
        ) / 2

        return {
            "home_attack": home_attack,
            "away_attack": away_attack,
            "home_defence": home_defence,
            "away_defence": away_defence,
            "attack": attack,
            "defence": defence,
            "league_attack": self.league_attack(),
        }

    def league_attack(self):

        attacks = []

        for team in self.stats.values():

            values = []

            if team["home_attack_weight"] > 0:

                values.append(
                    self.smoothed_average(
                        team["home_attack_sum"],
                        team["home_attack_weight"],
                    )
                )

            if team["away_attack_weight"] > 0:

                values.append(
                    self.smoothed_average(
                        team["away_attack_sum"],
                        team["away_attack_weight"],
                    )
                )

            if values:
                attacks.append(
                    sum(values) / len(values)
                )

        if not attacks:
            return LEAGUE_AVERAGE

        return sum(attacks) / len(attacks)

    def has_team(self, team):

        return (
            team in self.stats
            and (
                self.stats[team]["home_attack_weight"] > 0
                or self.stats[team]["away_attack_weight"] > 0
            )
        )