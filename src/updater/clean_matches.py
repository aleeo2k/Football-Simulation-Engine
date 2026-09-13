from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "Date": "date",
    "HomeTeam": "home_team",
    "AwayTeam": "away_team",
    "FTHG": "home_goals",
    "FTAG": "away_goals",
    "league_code": "league_code",
    "season": "season",
}


def main():

    root = Path(__file__).resolve().parents[2]

    source = root / "data" / "processed" / "matches.csv"
    output = root / "data" / "processed" / "matches_clean.csv"

    df = pd.read_csv(source)

    df = df.rename(columns=REQUIRED_COLUMNS)

    df = df[list(REQUIRED_COLUMNS.values())]

    # Даты уже находятся в ISO-формате.
    df["date"] = pd.to_datetime(
        df["date"],
        errors="coerce",
    )

    df = df.dropna(
        subset=[
            "date",
            "home_team",
            "away_team",
            "home_goals",
            "away_goals",
        ]
    )

    df["home_goals"] = df["home_goals"].astype(int)
    df["away_goals"] = df["away_goals"].astype(int)

    df = (
        df.sort_values("date")
          .reset_index(drop=True)
    )

    df.to_csv(
        output,
        index=False,
    )

    print()
    print("=" * 60)
    print("CLEAN DATASET CREATED")
    print("=" * 60)
    print(f"Rows    : {len(df):,}")
    print(f"Columns : {len(df.columns)}")
    print(f"First   : {df['date'].min().date()}")
    print(f"Last    : {df['date'].max().date()}")
    print(f"Saved   : {output}")
    print("=" * 60)


if __name__ == "__main__":
    main()