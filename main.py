from pathlib import Path

from src.collectors.understat_collector import UnderstatCollector


def main():
    collector = UnderstatCollector()

    print("Loading Premier League matches...")

    matches = collector.get_epl_matches()

    output_dir = Path("data/raw")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "understat_schedule.csv"

    matches.to_csv(output_file, index=True)

    print(f"Saved {len(matches)} matches to {output_file}")


if __name__ == "__main__":
    main()