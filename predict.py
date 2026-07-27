from src.services.explain_service import ExplainService
from src.services.prediction_service import PredictionService


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

    print("=== Football Prediction Engine ===\n")

    service = PredictionService()

    teams = service.get_teams()

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

    result = service.predict(
        home_team,
        away_team,
    )

    ExplainService.print_prediction(result)


if __name__ == "__main__":
    main()