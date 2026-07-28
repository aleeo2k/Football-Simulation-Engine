from collections import defaultdict, deque

from src.config import (
    DEFAULT_HOME_XG,
    FORM_MATCHES,
    FORM_DECAY,
)


class FormTracker:

    def __init__(
        self,
        form_matches: int = FORM_MATCHES,
        default_xg: float = DEFAULT_HOME_XG,
        decay: float = FORM_DECAY,
    ):

        self.default_xg = default_xg
        self.decay = decay

        self.home_attack = defaultdict(
            lambda: deque(maxlen=form_matches)
        )

        self.home_defence = defaultdict(
            lambda: deque(maxlen=form_matches)
        )

        self.away_attack = defaultdict(
            lambda: deque(maxlen=form_matches)
        )

        self.away_defence = defaultdict(
            lambda: deque(maxlen=form_matches)
        )

    def update(self, match):

        self.home_attack[
            match["home_team"]
        ].append(
            match["home_xg"]
        )

        self.home_defence[
            match["home_team"]
        ].append(
            match["away_xg"]
        )

        self.away_attack[
            match["away_team"]
        ].append(
            match["away_xg"]
        )

        self.away_defence[
            match["away_team"]
        ].append(
            match["home_xg"]
        )

    def average(
        self,
        values,
    ):

        if len(values) == 0:
            return self.default_xg

        weighted_sum = 0.0
        total_weight = 0.0

        values = list(values)

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

    def get_team(
        self,
        team,
        long_term=None,
    ):

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

        rolling_xg = (
            form_home_attack
            + form_away_attack
        ) / 2

        rolling_xga = (
            form_home_defence
            + form_away_defence
        ) / 2

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
        }

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