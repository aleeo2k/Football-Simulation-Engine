import pandas as pd


class IterativeRating:

    def __init__(
        self,
        matches: pd.DataFrame,
        iterations: int = 10,
    ):
        self.matches = matches.copy()
        self.iterations = iterations

    def calculate(self):

        teams = sorted(
            set(self.matches.home_team)
            .union(self.matches.away_team)
        )

        ratings = pd.DataFrame(
            index=teams,
            data={
                "attack": 1.0,
                "defence": 1.0,
            },
        )

        for _ in range(self.iterations):

            new_attack = {}
            new_defence = {}

            for team in teams:

                home = self.matches[
                    self.matches.home_team == team
                ]

                away = self.matches[
                    self.matches.away_team == team
                ]

                attack_values = []
                defence_values = []

                for _, match in home.iterrows():

                    opponent = match["away_team"]

                    attack_values.append(
                        match["home_xg"]
                        / ratings.loc[opponent, "defence"]
                    )

                    defence_values.append(
                        match["away_xg"]
                        / ratings.loc[opponent, "attack"]
                    )

                for _, match in away.iterrows():

                    opponent = match["home_team"]

                    attack_values.append(
                        match["away_xg"]
                        / ratings.loc[opponent, "defence"]
                    )

                    defence_values.append(
                        match["home_xg"]
                        / ratings.loc[opponent, "attack"]
                    )

                new_attack[team] = (
                    sum(attack_values)
                    / len(attack_values)
                )

                new_defence[team] = (
                    sum(defence_values)
                    / len(defence_values)
                )

            ratings["attack"] = pd.Series(
                new_attack
            )

            ratings["defence"] = pd.Series(
                new_defence
            )

            ratings["attack"] /= ratings[
                "attack"
            ].mean()

            ratings["defence"] /= ratings[
                "defence"
            ].mean()

        return ratings