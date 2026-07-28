class ExpectedGoalsModel:

    def predict(
        self,
        home: dict,
        away: dict,
        league: dict,
        home_team: str,
        away_team: str,
    ):

        home_league_avg = max(
            league["home_xg"],
            0.01,
        )

        away_league_avg = max(
            league["away_xg"],
            0.01,
        )

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
            / home_league_avg
        )

        away_xg = (
            away_attack
            * home_defence
            / away_league_avg
        )

        return {
            "home_team": home_team,
            "away_team": away_team,
            "home_xg": max(home_xg, 0.01),
            "away_xg": max(away_xg, 0.01),
        }