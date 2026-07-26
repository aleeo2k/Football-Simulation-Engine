from src.collectors.understat_collector import UnderstatCollector
from src.database.database import Database
from src.database.repository import MatchRepository

LEAGUE = "ENG-Premier League"


def main():

    print("=== Update Database ===\n")

    db = Database()

    repository = MatchRepository(
        db.get_session()
    )

    collector = UnderstatCollector()

    print("Downloading latest matches...\n")

    matches = collector.get_matches(LEAGUE)

    repository.save_matches(matches)

    print("\nDatabase successfully updated.")


if __name__ == "__main__":
    main()