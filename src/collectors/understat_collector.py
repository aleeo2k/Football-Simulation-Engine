import soccerdata as sd


SEASONS = [
    "2015",
    "2016",
    "2017",
    "2018",
    "2019",
    "2020",
    "2021",
    "2022",
    "2023",
    "2024",
    "2025",
    "2026",
]


class UnderstatCollector:

    def __init__(self):

        self.seasons = SEASONS

    def get_matches(
        self,
        league: str,
    ):

        understat = sd.Understat(
            leagues=league,
            seasons=self.seasons,
        )

        return understat.read_schedule(
            include_matches_without_data=True
        )