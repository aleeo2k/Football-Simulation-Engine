from pathlib import Path

import pandas as pd

from config import LEAGUES, SEASONS


def main():

    root = Path(__file__).resolve().parents[2]

    raw_dir = root / "data" / "raw"
    output_dir = root / "data" / "processed"

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    dfs = []

    for season in SEASONS:

        for league in LEAGUES:

            file = raw_dir / season / f"{league}.csv"

            if not file.exists():
                continue

            df = pd.read_csv(file)

            df["league_code"] = league
            df["season"] = season

            dfs.append(df)

    if not dfs:
        print("No files found.")
        return

    matches = pd.concat(
        dfs,
        ignore_index=True,
    )

    matches = matches.drop_duplicates()

    if "Date" in matches.columns:
        matches["Date"] = pd.to_datetime(
            matches["Date"],
            dayfirst=True,
            errors="coerce",
        )

        matches = matches.sort_values(
            "Date"
        )

    output = output_dir / "matches.csv"

    matches.to_csv(
        output,
        index=False,
    )

    print()
    print("=" * 50)
    print("MATCHES MERGED")
    print("=" * 50)
    print(f"Rows   : {len(matches):,}")
    print(f"Leagues: {matches['league_code'].nunique()}")
    print(f"Seasons: {matches['season'].nunique()}")
    print(f"Saved  : {output}")
    print("=" * 50)


if __name__ == "__main__":
    main()