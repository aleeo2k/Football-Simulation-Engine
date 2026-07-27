import pandas as pd


class HomeAdvantage:

    @staticmethod
    def calculate(matches: pd.DataFrame) -> float:
        """
        Возвращает коэффициент домашнего преимущества
        на основе среднего xG хозяев и гостей.
        """

        home_xg = matches["home_xg"].mean()
        away_xg = matches["away_xg"].mean()

        return home_xg / away_xg