import pandas as pd

from src.database.database import Database
from src.prediction.expected_goals import ExpectedGoalsModel
from src.prediction.match_prediction import MatchPrediction
from src.ratings.league_statistics import LeagueStatistics
from src.ratings.rating_tracker import RatingTracker


def main():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches ORDER BY date",
        db.engine,
    )

    tracker = RatingTracker()
    leagues = LeagueStatistics()

    predictor = MatchPrediction()
    xg_model = ExpectedGoalsModel()

    total = 0

    diff_01 = 0
    diff_02 = 0
    diff_03 = 0
    diff_05 = 0
    diff_10 = 0

    draw_probs = []

    draw_best = 0

    close_matches = 0
    close_draw_prob = 0

    highest_draws = []

    for _, match in matches.iterrows():

        if (
            tracker.has_team(match["home_team"])
            and
            tracker.has_team(match["away_team"])
        ):

            home = tracker.get_team(match["home_team"])
            away = tracker.get_team(match["away_team"])
            league = leagues.get(match["league_id"])

            xg = xg_model.predict(
                home=home,
                away=away,
                league=league,
                home_team=match["home_team"],
                away_team=match["away_team"],
            )

            prediction = predictor.predict(
                xg["home_xg"],
                xg["away_xg"],
            )

            diff = abs(
                xg["home_xg"]
                - xg["away_xg"]
            )

            total += 1

            if diff < 0.1:
                diff_01 += 1

            if diff < 0.2:
                diff_02 += 1

            if diff < 0.3:
                diff_03 += 1

            if diff < 0.5:
                diff_05 += 1

            if diff > 1.0:
                diff_10 += 1

            draw_probs.append(
                prediction["draw"]
            )

            if (
                prediction["draw"]
                >= prediction["home_win"]
                and
                prediction["draw"]
                >= prediction["away_win"]
            ):
                draw_best += 1

            if diff < 0.1:

                close_matches += 1
                close_draw_prob += prediction["draw"]

            highest_draws.append(
                {
                    "match": (
                        f"{match['home_team']} vs "
                        f"{match['away_team']}"
                    ),
                    "xg": (
                        f"{xg['home_xg']:.2f} : "
                        f"{xg['away_xg']:.2f}"
                    ),
                    "draw": prediction["draw"],
                }
            )

        tracker.update(match)
        leagues.update(match)

    highest_draws.sort(
        key=lambda x: x["draw"],
        reverse=True,
    )

    print("\n========== ANALYSIS ==========\n")

    print(f"Matches analysed: {total}")

    print("\nXG difference")

    print(f"<0.1 : {diff_01}")
    print(f"<0.2 : {diff_02}")
    print(f"<0.3 : {diff_03}")
    print(f"<0.5 : {diff_05}")
    print(f">1.0 : {diff_10}")

    print()

    print(
        f"Average draw probability: "
        f"{sum(draw_probs)/len(draw_probs):.3f}"
    )

    print(
        f"Maximum draw probability: "
        f"{max(draw_probs):.3f}"
    )

    print(
        f"Draw was most likely: "
        f"{draw_best} matches"
    )

    if close_matches:

        print()

        print(
            f"Average draw probability "
            f"when |ΔxG|<0.1 : "
            f"{close_draw_prob/close_matches:.3f}"
        )

    print("\nTop 20 draw matches\n")

    for row in highest_draws[:20]:

        print(
            f"{row['match']:<45}"
            f"{row['xg']:<15}"
            f"{row['draw']:.3f}"
        )


if __name__ == "__main__":
    main()