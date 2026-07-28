import optuna
import pandas as pd

from src.database.database import Database
from src.model.football_model import FootballModel


db = Database()

matches = pd.read_sql(
    "SELECT * FROM matches ORDER BY date",
    db.engine,
)


def objective(trial):

    smoothing = trial.suggest_float(
        "smoothing",
        1.0,
        8.0,
    )

    form_matches = trial.suggest_int(
        "form_matches",
        3,
        8,
    )

    home_advantage = trial.suggest_float(
        "home_advantage",
        40,
        80,
    )

    k_factor = trial.suggest_float(
        "k_factor",
        10,
        35,
    )

    model = FootballModel(
        smoothing=smoothing,
        form_matches=form_matches,
        home_advantage=home_advantage,
        k_factor=k_factor,
    )

    metrics = model.evaluate(
        matches,
    )

    trial.set_user_attr(
        "accuracy",
        metrics["accuracy"],
    )

    return metrics["logloss"]


def main():

    study = optuna.create_study(
        direction="minimize",
    )

    study.optimize(
        objective,
        n_trials=100,
        show_progress_bar=True,
    )

    print()
    print("=" * 70)
    print("BEST RESULT")
    print("=" * 70)
    print()

    print(
        f"LogLoss  : {study.best_value:.6f}"
    )

    print()

    print("Parameters:")

    for key, value in study.best_params.items():

        print(
            f"{key}: {value}"
        )

    print()

    print(
        "Accuracy:",
        study.best_trial.user_attrs[
            "accuracy"
        ],
    )


if __name__ == "__main__":
    main()