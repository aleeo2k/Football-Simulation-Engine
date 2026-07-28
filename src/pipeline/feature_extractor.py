from src.evaluation.result_parser import ResultParser


class FeatureExtractor:

    def extract(
        self,
        match,
        home,
        away,
        league,
        home_form,
        away_form,
        prediction,
        xg,
        home_elo,
        away_elo,
    ):

        return {

            # xG
            "home_xg": xg["home_xg"],
            "away_xg": xg["away_xg"],
            "xg_diff":
                xg["home_xg"]
                - xg["away_xg"],

            # Poisson
            "home_win":
                prediction["home_win"],

            "draw":
                prediction["draw"],

            "away_win":
                prediction["away_win"],

            # Ratings
            "home_attack":
                home["home_attack"],

            "away_attack":
                away["away_attack"],

            "home_defence":
                home["home_defence"],

            "away_defence":
                away["away_defence"],

            "attack_diff":
                home["home_attack"]
                - away["away_attack"],

            "defence_diff":
                away["away_defence"]
                - home["home_defence"],

            # League
            "league_home_xg":
                league["home_xg"],

            "league_away_xg":
                league["away_xg"],

            "league_total_xg":
                league["total_xg"],

            # Form
            "home_attack_delta":
                home_form["attack_delta"],

            "home_defence_delta":
                home_form["defence_delta"],

            "away_attack_delta":
                away_form["away_attack_delta"],

            "away_defence_delta":
                away_form["away_defence_delta"],

            # Elo
            "home_elo":
                home_elo,

            "away_elo":
                away_elo,

            "elo_diff":
                home_elo
                - away_elo,

            # Target
            "result":
                ResultParser.get_result(
                    match["home_goals"],
                    match["away_goals"],
                ),
        }