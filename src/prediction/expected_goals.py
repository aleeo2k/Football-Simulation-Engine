class ExpectedGoalsModel:

    def predict(
        self,
        home: dict,
        away: dict,
        league: dict,
        home_team: str,
        away_team: str,
    ):

        league_avg = (
            league["home_xg"]
            + league["away_xg"]
        ) / 2

        if league_avg <= 0:
            league_avg = 1.35

        home_attack = max(
            home["home_attack"],
            0.01,
        )

        away_attack = max(
            away["away_attack"],
            0.01,
        )

        home_defence = max(
            home["home_defence"],
            0.01,
        )

        away_defence = max(
            away["away_defence"],
            0.01,
        )

        home_xg = (
            home_attack
            * away_defence
            / league_avg
        )

        away_xg = (
            away_attack
            * home_defence
            / league_avg
        )

        home_xg = max(home_xg, 0.01)
        away_xg = max(away_xg, 0.01)

        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_xg": round(home_xg, 2),
            "away_xg": round(away_xg, 2),
        }