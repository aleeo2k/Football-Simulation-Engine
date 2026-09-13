class ExpectedGoalsModel:

    # ============================================================
    # EPL BASELINES
    # ============================================================

    HOME_LEAGUE_AVG = 1.577073
    AWAY_LEAGUE_AVG = 1.245044

    def __init__(
        self,
        ratings,
    ):

        self.ratings = ratings

        self.home_league_avg = (
            self.HOME_LEAGUE_AVG
        )

        self.away_league_avg = (
            self.AWAY_LEAGUE_AVG
        )

    # ============================================================
    # PREDICT
    # ============================================================

    def predict(
        self,
        home_team,
        away_team,
    ):

        # --------------------------------------------------------
        # Check teams
        # --------------------------------------------------------

        if (
            home_team
            not in self.ratings.index
        ):

            raise ValueError(
                f"Home team not found: "
                f"{home_team}"
            )

        if (
            away_team
            not in self.ratings.index
        ):

            raise ValueError(
                f"Away team not found: "
                f"{away_team}"
            )

        home = self.ratings.loc[
            home_team
        ]

        away = self.ratings.loc[
            away_team
        ]

        # --------------------------------------------------------
        # Home team
        # --------------------------------------------------------

        home_attack = max(
            float(
                home["home_attack"]
            ),
            0.01,
        )

        home_defence = max(
            float(
                home["home_defence"]
            ),
            0.01,
        )

        # --------------------------------------------------------
        # Away team
        # --------------------------------------------------------

        away_attack = max(
            float(
                away["away_attack"]
            ),
            0.01,
        )

        away_defence = max(
            float(
                away["away_defence"]
            ),
            0.01,
        )

        # ========================================================
        # EXPECTED GOALS
        # ========================================================

        home_xg = (
            home_attack
            *
            away_defence
            /
            self.away_league_avg
        )

        away_xg = (
            away_attack
            *
            home_defence
            /
            self.home_league_avg
        )

        # --------------------------------------------------------
        # Safety
        # --------------------------------------------------------

        home_xg = max(
            float(home_xg),
            0.01,
        )

        away_xg = max(
            float(away_xg),
            0.01,
        )

        return {
            "home_team":
                home_team,

            "away_team":
                away_team,

            "home_xg":
                home_xg,

            "away_xg":
                away_xg,
        }