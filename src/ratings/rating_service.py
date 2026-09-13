import pandas as pd


# ============================================================
# EPL BASELINES
# ============================================================

EPL_HOME_XG = 1.577073
EPL_AWAY_XG = 1.245044


# ============================================================
# PROMOTED TEAMS
#
# Championship data is NOT used.
# These teams only need to exist in the ratings table
# before they have played their first EPL match.
# ============================================================

PROMOTED_TEAMS = {
    "Coventry",
    "Hull",
    "Ipswich",
}


class RatingService:

    def __init__(
        self,
        matches: pd.DataFrame,
        recency_decay: float = 0.998,
    ):

        self.matches = matches.copy()
        self.recency_decay = recency_decay

    # ============================================================
    # CURRENT EPL SEASON
    # ============================================================

    def _current_season_matches(self):

        matches = self.matches.copy()

        if matches.empty:
            return matches

        matches["date"] = pd.to_datetime(
            matches["date"],
            errors="coerce",
        )

        latest = matches["date"].max()

        if pd.isna(latest):
            return matches.iloc[0:0].copy()

        if latest.month >= 8:
            season_start_year = latest.year
        else:
            season_start_year = latest.year - 1

        season_start = pd.Timestamp(
            year=season_start_year,
            month=8,
            day=1,
        )

        season_end = pd.Timestamp(
            year=season_start_year + 1,
            month=7,
            day=31,
        )

        return matches[
            (
                matches["date"]
                >= season_start
            )
            &
            (
                matches["date"]
                <= season_end
            )
        ].copy()

    # ============================================================
    # TEAM STATISTICS
    # ============================================================

    def team_statistics(self):

        matches = self.matches.copy()

        if matches.empty:

            return pd.DataFrame(
                columns=[
                    "home_attack",
                    "home_defence",
                    "away_attack",
                    "away_defence",
                    "matches",
                    "attack",
                    "defence",
                    "attack_strength",
                    "defence_strength",
                ]
            )

        matches["date"] = pd.to_datetime(
            matches["date"],
            errors="coerce",
        )

        matches = matches.dropna(
            subset=["date"]
        ).copy()

        if matches.empty:
            return pd.DataFrame()

        latest = matches["date"].max()

        # --------------------------------------------------------
        # Recency weighting
        # --------------------------------------------------------

        matches["days_old"] = (
            latest
            - matches["date"]
        ).dt.days

        matches["weight"] = (
            self.recency_decay
            **
            matches["days_old"]
        )

        # --------------------------------------------------------
        # Current EPL season
        # --------------------------------------------------------

        current_season = (
            self._current_season_matches()
        )

        # --------------------------------------------------------
        # All teams
        #
        # Promoted teams are explicitly included so that they
        # receive a rating even before playing their first EPL
        # match.
        # --------------------------------------------------------

        all_teams = sorted(
            set(matches["home_team"])
            |
            set(matches["away_team"])
            |
            PROMOTED_TEAMS
        )

        teams = []

        for team in all_teams:

            # ----------------------------------------------------
            # Promoted teams:
            #
            # ONLY current EPL season is allowed.
            #
            # No Championship prior.
            # No old EPL data.
            # ----------------------------------------------------

            if team in PROMOTED_TEAMS:

                home = current_season[
                    current_season[
                        "home_team"
                    ]
                    == team
                ]

                away = current_season[
                    current_season[
                        "away_team"
                    ]
                    == team
                ]

            else:

                home = matches[
                    matches["home_team"]
                    == team
                ]

                away = matches[
                    matches["away_team"]
                    == team
                ]

            # ----------------------------------------------------
            # Weighted average
            # ----------------------------------------------------

            def weighted(
                series,
                weight,
            ):

                if len(series) == 0:
                    return None

                weight_sum = weight.sum()

                if (
                    weight_sum <= 0
                    or pd.isna(weight_sum)
                ):
                    return None

                return (
                    (
                        series
                        * weight
                    ).sum()
                    /
                    weight_sum
                )

            # ----------------------------------------------------
            # Attack
            #
            # home_attack:
            # goals/xG scored by team at home
            #
            # away_attack:
            # goals/xG scored by team away
            # ----------------------------------------------------

            home_attack = weighted(
                home["home_xg"],
                home["weight"],
            )

            away_attack = weighted(
                away["away_xg"],
                away["weight"],
            )

            # ----------------------------------------------------
            # Defence
            #
            # home_defence:
            # opponent xG at this team's home
            #
            # away_defence:
            # opponent xG at this team's away matches
            # ----------------------------------------------------

            home_defence = weighted(
                home["away_xg"],
                home["weight"],
            )

            away_defence = weighted(
                away["home_xg"],
                away["weight"],
            )

            # ----------------------------------------------------
            # NEW PROMOTED TEAM
            #
            # No EPL matches yet.
            #
            # We use neutral EPL league baselines.
            # Championship is completely ignored.
            # ----------------------------------------------------

            if (
                team in PROMOTED_TEAMS
                and
                len(home) + len(away) == 0
            ):

                home_attack = (
                    EPL_HOME_XG
                )

                home_defence = (
                    EPL_AWAY_XG
                )

                away_attack = (
                    EPL_AWAY_XG
                )

                away_defence = (
                    EPL_HOME_XG
                )

            # ----------------------------------------------------
            # Missing home/away split
            #
            # This can happen for normal EPL teams when there
            # is not enough data for one side.
            # ----------------------------------------------------

            if home_attack is None:

                home_attack = (
                    EPL_HOME_XG
                )

            if away_attack is None:

                away_attack = (
                    EPL_AWAY_XG
                )

            if home_defence is None:

                home_defence = (
                    EPL_AWAY_XG
                )

            if away_defence is None:

                away_defence = (
                    EPL_HOME_XG
                )

            # ----------------------------------------------------
            # Save
            # ----------------------------------------------------

            teams.append(
                {
                    "team": team,

                    "home_attack":
                        home_attack,

                    "home_defence":
                        home_defence,

                    "away_attack":
                        away_attack,

                    "away_defence":
                        away_defence,

                    "matches":
                        len(home)
                        + len(away),
                }
            )

        ratings = (
            pd.DataFrame(teams)
            .set_index("team")
        )

        # ========================================================
        # OVERALL ATTACK / DEFENCE
        # ========================================================

        ratings["attack"] = (
            ratings["home_attack"]
            +
            ratings["away_attack"]
        ) / 2.0

        ratings["defence"] = (
            ratings["home_defence"]
            +
            ratings["away_defence"]
        ) / 2.0

        league_attack = (
            ratings["attack"]
            .mean()
        )

        league_defence = (
            ratings["defence"]
            .mean()
        )

        # ========================================================
        # STRENGTH
        # ========================================================

        if league_attack > 0:

            ratings["attack_strength"] = (
                ratings["attack"]
                /
                league_attack
            )

        else:

            ratings["attack_strength"] = 1.0

        if league_defence > 0:

            ratings["defence_strength"] = (
                ratings["defence"]
                /
                league_defence
            )

        else:

            ratings["defence_strength"] = 1.0

        return ratings.sort_values(
            "attack_strength",
            ascending=False,
        )