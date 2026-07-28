import pandas as pd

from src.database.database import Database
from src.model.football_model import FootballModel


def test_model_quality():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches ORDER BY date",
        db.engine,
    )

    model = FootballModel()

    metrics = model.evaluate(matches)

    assert metrics["accuracy"] > 0.51
    assert metrics["logloss"] < 1.0