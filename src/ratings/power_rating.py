class PowerRating:

    def __init__(
        self,
        attack_weight=0.35,
        defence_weight=0.35,
        elo_weight=0.20,
        form_weight=0.10,
    ):

        self.attack_weight = attack_weight
        self.defence_weight = defence_weight
        self.elo_weight = elo_weight
        self.form_weight = form_weight

    def calculate(
        self,
        team,
        form,
        elo,
    ):

        attack = (
            team["home_attack"]
            + team["away_attack"]
        ) / 2

        defence = (
            team["home_defence"]
            + team["away_defence"]
        ) / 2

        defence = 2.0 - defence

        form_attack = form["attack_delta"]
        form_defence = form["defence_delta"]

        form_rating = (
            form_attack
            - form_defence
        )

        elo_rating = (
            elo - 1500
        ) / 400

        power = (

            attack * self.attack_weight

            +

            defence * self.defence_weight

            +

            elo_rating * self.elo_weight

            +

            form_rating * self.form_weight

        )

        return float(power)