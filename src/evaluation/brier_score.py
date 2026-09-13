class BrierScore:

    @staticmethod
    def calculate(results):

        score = 0.0

        for result in results:

            actual = {
                "H": 0,
                "D": 0,
                "A": 0,
            }

            actual[result["actual"]] = 1

            score += (
                (result["home_win"] - actual["H"]) ** 2
                + (result["draw"] - actual["D"]) ** 2
                + (result["away_win"] - actual["A"]) ** 2
            )

        return score / len(results)
    