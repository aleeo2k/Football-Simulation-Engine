import soccerdata as sd


class UnderstatCollector:
    def __init__(self):
        self.understat = sd.Understat()

    def get_epl_matches(self):
        """
        Возвращает расписание матчей.
        """
        return self.understat.read_schedule()
    