class ResultParser:

    @staticmethod
    def get_result(home_goals, away_goals):

        if home_goals > away_goals:
            return "H"

        if home_goals < away_goals:
            return "A"

        return "D"