import pandas as pd


class IncrementalRating:

    def __init__(self):

        self.matches = pd.DataFrame()

        self.ratings = None

    def update(self, match: pd.Series):

        self.matches = pd.concat(
            [
                self.matches,
                match.to_frame().T,
            ],
            ignore_index=True,
        )

    def build(self):

        from src.ratings.rating_service import RatingService

        self.ratings = RatingService(
            self.matches
        ).team_statistics()

        return self.ratings