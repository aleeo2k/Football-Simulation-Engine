import pandas as pd


class ConfusionMatrix:

    @staticmethod
    def build(predictions, actual):

        labels = ["H", "D", "A"]

        matrix = pd.DataFrame(
            0,
            index=labels,
            columns=labels,
        )

        for predicted, real in zip(predictions, actual):
            matrix.loc[real, predicted] += 1

        return matrix