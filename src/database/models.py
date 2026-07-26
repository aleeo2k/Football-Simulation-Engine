from sqlalchemy import Column, DateTime, Float, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Match(Base):
    __tablename__ = "matches"

    game_id = Column(Integer, primary_key=True)

    league_id = Column(Integer, nullable=False)
    season_id = Column(Integer, nullable=False)

    date = Column(DateTime)

    home_team_id = Column(Integer)
    away_team_id = Column(Integer)

    home_team = Column(String(100))
    away_team = Column(String(100))

    home_team_code = Column(String(10))
    away_team_code = Column(String(10))

    home_goals = Column(Integer)
    away_goals = Column(Integer)

    home_xg = Column(Float)
    away_xg = Column(Float)

    is_result = Column(Integer)
    has_data = Column(Integer)

    url = Column(String(255))   