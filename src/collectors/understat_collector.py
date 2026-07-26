import soccerdata as sd


class UnderstatCollector:
    def __init__(self):
        self.understat = sd.Understat()

    def get_matches(self, league: str):
        """
        Загружает расписание и статистику матчей выбранной лиги.

        Примеры:
        ENG-Premier League
        ESP-La Liga
        ITA-Serie A
        GER-Bundesliga
        FRA-Ligue 1
        """

        return self.understat.read_schedule(league)