import pandas as pd

from src.database.database import Database
from src.model.football_model import FootballModel
from src.model.football_model import FEATURES


GROUPS = {

    "ALL": FEATURES,

    "NO_XG": [
        f for f in FEATURES
        if f not in {
            "home_xg",
            "away_xg",
            "xg_diff",
        }
    ],

    "NO_POISSON": [
        f for f in FEATURES
        if f not in {
            "home_win",
            "draw",
            "away_win",
        }
    ],

    "NO_ELO": [
        f for f in FEATURES
        if f not in {
            "home_elo",
            "away_elo",
            "elo_diff",
        }
    ],

    "NO_FORM": [
        f for f in FEATURES
        if f not in {
            "home_attack_delta",
            "home_defence_delta",
            "away_attack_delta",
            "away_defence_delta",
        }
    ],

    "NO_LEAGUE": [
        f for f in FEATURES
        if f not in {
            "league_home_xg",
            "league_away_xg",
            "league_total_xg",
        }
    ],

    "NO_RATINGS": [
        f for f in FEATURES
        if f not in {
            "home_attack",
            "away_attack",
            "home_defence",
            "away_defence",
            "attack_diff",
            "defence_diff",
        }
    ],
}


db = Database()

matches = pd.read_sql(
    "SELECT * FROM matches ORDER BY date",
    db.engine,
)

print()

print("=" * 65)
print("FEATURE ABLATION")
print("=" * 65)

for name, features in GROUPS.items():

    model = FootballModel()

    model.features = features

    result = model.evaluate(matches)

    print(
        f"{name:<12}"
        f" Accuracy={result['accuracy']:.5f}"
        f"  LogLoss={result['logloss']:.5f}"
    )