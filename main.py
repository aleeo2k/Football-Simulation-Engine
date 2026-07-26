from src.collectors.understat_collector import UnderstatCollector
from src.prediction.expected_goals import ExpectedGoalsModel
from src.prediction.match_prediction import MatchPrediction
from src.ratings.rating_service import RatingService

LEAGUE = "ENG-Premier League"


def find_team(query, teams):

    query = query.strip().lower()

    matches = [
        team
        for team in teams
        if query in team.lower()
    ]

    if len(matches) == 0:
        print(f'\nNo team found for "{query}".')
        return None

    if len(matches) == 1:
        return matches[0]

    print(f'\nSeveral teams match "{query}":\n')

    for i, team in enumerate(matches, start=1):
        print(f"{i}. {team}")

    while True:

        choice = input("\nChoose number: ")

        if choice.isdigit():

            choice = int(choice)

            if 1 <= choice <= len(matches):
                return matches[choice - 1]

        print("Invalid choice.")


def main():

    print("=== Football Simulation Engine ===\n")

    collector = UnderstatCollector()

    print(f"Downloading {LEAGUE}...\n")

    matches = collector.get_matches(LEAGUE)

    ratings = RatingService(matches).team_statistics()

    teams = sorted(ratings.index.tolist())

    match_input = input(
        "Match (example: Arsenal vs Liverpool): "
    ).strip()

    if " vs " not in match_input.lower():

        print("\nUse format:")
        print("Team A vs Team B")
        return

    home_query, away_query = match_input.lower().split(" vs ", 1)

    home_team = find_team(home_query, teams)

    if home_team is None:
        return

    away_team = find_team(away_query, teams)

    if away_team is None:
        return

    xg_model = ExpectedGoalsModel(ratings)

    xg = xg_model.predict(
        home_team,
        away_team,
    )

    predictor = MatchPrediction()

    result = predictor.predict(
        xg["home_xg"],
        xg["away_xg"],
    )

    print("\n====================================")
    print(f"{home_team} vs {away_team}")
    print("====================================")

    print("\nExpected Goals")

    print(f"{home_team}: {xg['home_xg']}")
    print(f"{away_team}: {xg['away_xg']}")

    print("\nMatch Odds")

    print(f"{home_team}: {result['home_win']}%")
    print(f"Draw: {result['draw']}%")
    print(f"{away_team}: {result['away_win']}%")


if __name__ == "__main__":
    main()