import pandas as pd


class ChampionshipInitializer:

    # ============================================================
    # FINAL CALIBRATED VALUE
    # ============================================================

    PROMOTED_STARTING_ELO = 1370.0

    def __init__(self):

        pass

    # ============================================================
    # PROMOTED TEAM ELO
    # ============================================================

    def get_promoted_team_ratings(
        self,
        promoted_teams,
    ):

        return {
            team:
                self.PROMOTED_STARTING_ELO
            for team in promoted_teams
        }

    # ============================================================
    # PROMOTED TEAM DATA
    #
    # Kept for compatibility with existing code.
    # Championship xG is deliberately NOT used.
    # ============================================================

    def get_promoted_team_data(
        self,
        promoted_teams,
    ):

        result = {}

        for team in promoted_teams:

            result[team] = {
                "elo":
                    self.PROMOTED_STARTING_ELO,

                "home_attack":
                    None,

                "home_defence":
                    None,

                "away_attack":
                    None,

                "away_defence":
                    None,
            }

        return result