from pathlib import Path

from src.collectors.understat_collector import UnderstatCollector
from src.database.database import Database
from src.database.repository import MatchRepository


def main():
    print("Starting Football Simulation Engine...\n")

    # База данных
    db = Database()
    session = db.get_session()
    repository = MatchRepository(session)

    # Загружаем матчи
    collector = UnderstatCollector()

    print("Downloading Premier League matches...")
    matches = collector.get_epl_matches()

    print(f"Downloaded {len(matches)} matches.")

    # Сохраняем в SQLite
    print("Saving matches to database...")
    repository.save_matches(matches)

    # Пока оставляем CSV как резервную копию
    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "understat_schedule.csv"
    matches.to_csv(output_file)

    print("\nDone!")
    print(f"Database: {db.db_path}")


if __name__ == "__main__":
    main()