import math


class LogLoss:

    @staticmethod
    def calculate(results):

        loss = 0.0

        epsilon = 1e-15

        for result in results:

            if result["actual"] == "H":
                p = result["home_win"]

            elif result["actual"] == "D":
                p = result["draw"]

            else:
                p = result["away_win"]

            p = max(
                epsilon,
                min(1 - epsilon, p),
            )

            loss += -math.log(p)

        return loss / len(results)