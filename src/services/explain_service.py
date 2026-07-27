class ExplainService:

    @staticmethod
    def print_prediction(result):

        print("\n====================================")
        print(f"{result['home_team']} vs {result['away_team']}")
        print("====================================")

        print("\nExpected Goals")
        print(f"{result['home_team']}: {result['home_xg']:.2f}")
        print(f"{result['away_team']}: {result['away_xg']:.2f}")

        print("\nMatch Odds")
        print(
            f"{result['home_team']}: "
            f"{result['home_win'] * 100:.2f}%"
        )
        print(
            f"Draw: "
            f"{result['draw'] * 100:.2f}%"
        )
        print(
            f"{result['away_team']}: "
            f"{result['away_win'] * 100:.2f}%"
        )

        print("\nMost Likely Scores")

        for score in result["top_scores"]:
            print(
                f"{score['score']:>5}   "
                f"{score['probability'] * 100:.2f}%"
            )