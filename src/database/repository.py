import pandas as pd

from src.database.models import Match


class MatchRepository:
    def __init__(self, session):
        self.session = session

    def save_matches(self, matches: pd.DataFrame):
        added = 0
        skipped = 0

        for _, row in matches.iterrows():

            exists = (
                self.session.query(Match)
                .filter_by(game_id=int(row["game_id"]))
                .first()
            )

            if exists:
                skipped += 1
                continue

            match = Match(
                game_id=int(row["game_id"]),
                league_id=int(row["league_id"]),
                season_id=int(row["season_id"]),

                date=row["date"],

                home_team_id=int(row["home_team_id"]),
                away_team_id=int(row["away_team_id"]),

                home_team=row["home_team"],
                away_team=row["away_team"],

                home_team_code=row["home_team_code"],
                away_team_code=row["away_team_code"],

                home_goals=int(row["home_goals"]) if pd.notna(row["home_goals"]) else None,
                away_goals=int(row["away_goals"]) if pd.notna(row["away_goals"]) else None,

                home_xg=float(row["home_xg"]) if pd.notna(row["home_xg"]) else None,
                away_xg=float(row["away_xg"]) if pd.notna(row["away_xg"]) else None,

                is_result=bool(row["is_result"]),
                has_data=bool(row["has_data"]),

                url=row["url"],
            )

            self.session.add(match)
            added += 1

        self.session.commit()

        print(f"Added: {added}")
        print(f"Skipped: {skipped}")