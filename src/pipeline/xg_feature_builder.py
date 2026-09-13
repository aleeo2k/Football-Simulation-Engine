from src.xg_features import XG_FEATURES


class XGFeatureBuilder:

    def build(
        self,
        home,
        away,
        league,
        home_form,
        away_form,
        home_elo,
        away_elo,
        home_rest,
        away_rest,
        home_opponent_strength,
        away_opponent_strength,
        home_power,
        away_power,
    ):

        features = {

            # ==========================================
            # Long-term ratings
            # ==========================================

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

            # ==========================================
            # League
            # ==========================================

            "league_home_xg":
                league["home_xg"],

            "league_away_xg":
                league["away_xg"],

            "league_total_xg":
                league["total_xg"],

            # ==========================================
            # Recent form
            # ==========================================

            "home_attack_delta":
                home_form["attack_delta"],

            "home_defence_delta":
                home_form["defence_delta"],

            "away_attack_delta":
                away_form["away_attack_delta"],

            "away_defence_delta":
                away_form["away_defence_delta"],

            # ==========================================
            # Elo
            # ==========================================

            "home_elo":
                home_elo,

            "away_elo":
                away_elo,

            "elo_diff":
                home_elo
                - away_elo,

            # ==========================================
            # Rest
            # ==========================================

            "home_rest_days":
                home_rest,

            "away_rest_days":
                away_rest,

            "rest_diff":
                home_rest
                - away_rest,

            # ==========================================
            # Power Rating
            # ==========================================

            "home_power":
                home_power,

            "away_power":
                away_power,

            "power_diff":
                home_power
                - away_power,

            # ==========================================
            # Opponent Strength
            # ==========================================

            "home_opponent_strength":
                home_opponent_strength,

            "away_opponent_strength":
                away_opponent_strength,

            "opponent_strength_diff":
                home_opponent_strength
                - away_opponent_strength,

            # ==========================================
            # Rolling xG — 3
            # ==========================================

            "home_xg_form_3":
                home_form["home_xg_form_3"],

            "home_xga_form_3":
                home_form["home_xga_form_3"],

            "away_xg_form_3":
                away_form["away_xg_form_3"],

            "away_xga_form_3":
                away_form["away_xga_form_3"],

            # ==========================================
            # Rolling xG — 5
            # ==========================================

            "home_xg_form_5":
                home_form["home_xg_form_5"],

            "home_xga_form_5":
                home_form["home_xga_form_5"],

            "away_xg_form_5":
                away_form["away_xg_form_5"],

            "away_xga_form_5":
                away_form["away_xga_form_5"],

            # ==========================================
            # Rolling xG — 10
            # ==========================================

            "home_xg_form_10":
                home_form["home_xg_form_10"],

            "home_xga_form_10":
                home_form["home_xga_form_10"],

            "away_xg_form_10":
                away_form["away_xg_form_10"],

            "away_xga_form_10":
                away_form["away_xga_form_10"],
        }

        return {
            feature: features[feature]
            for feature in XG_FEATURES
        }