from collections import defaultdict, deque

from src.config import (
    DEFAULT_HOME_XG,
    FORM_DECAY,
)


class FormTracker:

    def __init__(
        self,
        form_matches: int = 5,
        default_xg: float = DEFAULT_HOME_XG,
        decay: float = FORM_DECAY,
        default_elo: float = 1500.0,
    ):

        self.default_xg = default_xg
        self.default_elo = default_elo
        self.decay = decay

        # -------------------------------------------------
        # Последние 10 матчей
        # -------------------------------------------------

        self.home_attack = defaultdict(
            lambda: deque(maxlen=10)
        )

        self.home_defence = defaultdict(
            lambda: deque(maxlen=10)
        )

        self.away_attack = defaultdict(
            lambda: deque(maxlen=10)
        )

        self.away_defence = defaultdict(
            lambda: deque(maxlen=10)
        )

        # -------------------------------------------------
        # Сила соперников в момент матча
        # -------------------------------------------------

        self.home_opponent_strength = defaultdict(
            lambda: deque(maxlen=10)
        )

        self.away_opponent_strength = defaultdict(
            lambda: deque(maxlen=10)
        )

    # =====================================================
    # UPDATE
    # =====================================================

    def update(
        self,
        match,
        home_opponent_strength=None,
        away_opponent_strength=None,
    ):

        home_xg = match["home_xg"]
        away_xg = match["away_xg"]

        # Если xG отсутствует,
        # матч не используется для формы.

        if home_xg is None or away_xg is None:
            return

        home_team = match["home_team"]
        away_team = match["away_team"]

        home_xg = float(home_xg)
        away_xg = float(away_xg)

        # -------------------------------------------------
        # Домашняя команда
        # -------------------------------------------------

        self.home_attack[
            home_team
        ].append(
            home_xg
        )

        self.home_defence[
            home_team
        ].append(
            away_xg
        )

        if home_opponent_strength is not None:

            self.home_opponent_strength[
                home_team
            ].append(
                float(home_opponent_strength)
            )

        # -------------------------------------------------
        # Гостевая команда
        # -------------------------------------------------

        self.away_attack[
            away_team
        ].append(
            away_xg
        )

        self.away_defence[
            away_team
        ].append(
            home_xg
        )

        if away_opponent_strength is not None:

            self.away_opponent_strength[
                away_team
            ].append(
                float(away_opponent_strength)
            )

    # =====================================================
    # XG AVERAGE
    # =====================================================

    def average(
        self,
        values,
        window=None,
    ):

        if len(values) == 0:
            return self.default_xg

        values = list(values)

        if window is not None:
            values = values[-window:]

        weighted_sum = 0.0
        total_weight = 0.0

        for i, value in enumerate(
            reversed(values)
        ):

            weight = self.decay ** i

            weighted_sum += (
                value * weight
            )

            total_weight += weight

        return (
            weighted_sum
            / total_weight
        )

    # =====================================================
    # ELO AVERAGE
    # =====================================================

    def average_elo(
        self,
        values,
        window=None,
    ):

        if len(values) == 0:
            return self.default_elo

        values = list(values)

        if window is not None:
            values = values[-window:]

        weighted_sum = 0.0
        total_weight = 0.0

        for i, value in enumerate(
            reversed(values)
        ):

            weight = self.decay ** i

            weighted_sum += (
                value * weight
            )

            total_weight += weight

        return (
            weighted_sum
            / total_weight
        )

    # =====================================================
    # GET TEAM
    # =====================================================

    def get_team(
        self,
        team,
        long_term=None,
    ):

        # -------------------------------------------------
        # Текущая сглаженная форма
        # -------------------------------------------------

        form_home_attack = self.average(
            self.home_attack[team]
        )

        form_home_defence = self.average(
            self.home_defence[team]
        )

        form_away_attack = self.average(
            self.away_attack[team]
        )

        form_away_defence = self.average(
            self.away_defence[team]
        )

        # -------------------------------------------------
        # Rolling 3
        # -------------------------------------------------

        home_xg_3 = self.average(
            self.home_attack[team],
            window=3,
        )

        home_xga_3 = self.average(
            self.home_defence[team],
            window=3,
        )

        away_xg_3 = self.average(
            self.away_attack[team],
            window=3,
        )

        away_xga_3 = self.average(
            self.away_defence[team],
            window=3,
        )

        # -------------------------------------------------
        # Rolling 5
        # -------------------------------------------------

        home_xg_5 = self.average(
            self.home_attack[team],
            window=5,
        )

        home_xga_5 = self.average(
            self.home_defence[team],
            window=5,
        )

        away_xg_5 = self.average(
            self.away_attack[team],
            window=5,
        )

        away_xga_5 = self.average(
            self.away_defence[team],
            window=5,
        )

        # -------------------------------------------------
        # Rolling 10
        # -------------------------------------------------

        home_xg_10 = self.average(
            self.home_attack[team],
            window=10,
        )

        home_xga_10 = self.average(
            self.home_defence[team],
            window=10,
        )

        away_xg_10 = self.average(
            self.away_attack[team],
            window=10,
        )

        away_xga_10 = self.average(
            self.away_defence[team],
            window=10,
        )

        # -------------------------------------------------
        # Rolling opponent strength
        # -------------------------------------------------

        home_opponent_3 = self.average_elo(
            self.home_opponent_strength[team],
            window=3,
        )

        away_opponent_3 = self.average_elo(
            self.away_opponent_strength[team],
            window=3,
        )

        # -------------------------------------------------
        # Strength-adjusted Rolling 3
        # -------------------------------------------------

        home_strength_factor = (
            home_opponent_3 / self.default_elo
        )

        away_strength_factor = (
            away_opponent_3 / self.default_elo
        )

        home_xg_form_3_adj = (
            home_xg_3
            * home_strength_factor
        )

        home_xga_form_3_adj = ( 
            home_xga_3
            * home_strength_factor
        )

        away_xg_form_3_adj = (
            away_xg_3
            * away_strength_factor
        )

        away_xga_form_3_adj = (
            away_xga_3
            * away_strength_factor
        )

        # -------------------------------------------------
        # Общая форма
        # -------------------------------------------------

        rolling_xg = (
            form_home_attack
            + form_away_attack
        ) / 2

        rolling_xga = (
            form_home_defence
            + form_away_defence
        ) / 2

        # -------------------------------------------------
        # Result
        # -------------------------------------------------

        result = {

            "form_home_attack":
                form_home_attack,

            "form_home_defence":
                form_home_defence,

            "form_away_attack":
                form_away_attack,

            "form_away_defence":
                form_away_defence,

            "rolling_xg":
                rolling_xg,

            "rolling_xga":
                rolling_xga,

            "rolling_xg_diff":
                rolling_xg
                - rolling_xga,

            # =============================================
            # Rolling 3
            # =============================================

            "home_xg_form_3":
                home_xg_3,

            "home_xga_form_3":
                home_xga_3,

            "away_xg_form_3":
                away_xg_3,

            "away_xga_form_3":
                away_xga_3,

            # =============================================
            # Rolling 5
            # =============================================

            "home_xg_form_5":
                home_xg_5,

            "home_xga_form_5":
                home_xga_5,

            "away_xg_form_5":
                away_xg_5,

            "away_xga_form_5":
                away_xga_5,

            # =============================================
            # Rolling 10
            # =============================================

            "home_xg_form_10":
                home_xg_10,

            "home_xga_form_10":
                home_xga_10,

            "away_xg_form_10":
                away_xg_10,

            "away_xga_form_10":
                away_xga_10,

            # =============================================
            # Strength-adjusted Rolling 3
            # =============================================

            "home_xg_form_3_adj":
                home_xg_form_3_adj,

            "home_xga_form_3_adj":
                home_xga_form_3_adj,

            "away_xg_form_3_adj":
                away_xg_form_3_adj,

            "away_xga_form_3_adj":
                away_xga_form_3_adj,

            # =============================================
            # Opponent strength
            # =============================================

            "home_opponent_3":
                home_opponent_3,

            "away_opponent_3":
                away_opponent_3,
        }

        # -------------------------------------------------
        # Delta относительно долгосрочного рейтинга
        # -------------------------------------------------

        if long_term is not None:

            result.update(
                {

                    "attack_delta":
                        form_home_attack
                        - long_term["home_attack"],

                    "defence_delta":
                        form_home_defence
                        - long_term["home_defence"],

                    "away_attack_delta":
                        form_away_attack
                        - long_term["away_attack"],

                    "away_defence_delta":
                        form_away_defence
                        - long_term["away_defence"],
                }
            )

        return result