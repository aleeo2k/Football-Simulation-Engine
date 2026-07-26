from src.database.models import Match


class TeamRepository:
    def __init__(self, session):
        self.session = session

    def get_all_teams(self):
        home_teams = (
            self.session.query(Match.home_team)
            .distinct()
            .all()
        )

        away_teams = (
            self.session.query(Match.away_team)
            .distinct()
            .all()
        )

        teams = {
            team[0]
            for team in home_teams + away_teams
            if team[0] is not None
        }

        return sorted(teams)