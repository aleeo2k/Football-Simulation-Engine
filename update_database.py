from src.collectors.understat_collector import UnderstatCollector
from src.config import DEFAULT_LEAGUE
from src.database.database import Database
from src.database.repository import MatchRepository


def main():

    print("=== Update Database ===\n")

    db = Database()

    repository = MatchRepository(
        db.get_session()
    )

    collector = UnderstatCollector()

    print(f"Downloading {DEFAULT_LEAGUE}...\n")

    matches = collector.get_matches(
        DEFAULT_LEAGUE
    )

    repository.save_matches(matches)

    print("\nDatabase successfully updated.")


if __name__ == "__main__":
    main()