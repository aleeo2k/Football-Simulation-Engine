import itertools
import pandas as pd

from src.database.database import Database
from src.model.football_model import FootballModel


SMOOTHING = [3, 5, 7, 10]
FORM_MATCHES = [3, 5, 7]
HOME_ADVANTAGE = [40, 55, 70, 85]
K_FACTOR = [10, 20, 30]


def main():

    db = Database()

    matches = pd.read_sql(
        "SELECT * FROM matches ORDER BY date",
        db.engine,
    )

    results = []

    total = (
        len(SMOOTHING)
        * len(FORM_MATCHES)
        * len(HOME_ADVANTAGE)
        * len(K_FACTOR)
    )

    current = 1

    for smoothing, form, home_advantage, k in itertools.product(
        SMOOTHING,
        FORM_MATCHES,
        HOME_ADVANTAGE,
        K_FACTOR,
    ):

        print(
            f"[{current}/{total}] "
            f"s={smoothing} "
            f"form={form} "
            f"home={home_advantage} "
            f"k={k}"
        )

        model = FootballModel(
            smoothing=smoothing,
            form_matches=form,
            home_advantage=home_advantage,
            k_factor=k,
        )

        metrics = model.evaluate(matches)

        results.append(
            {
                "smoothing": smoothing,
                "form_matches": form,
                "home_advantage": home_advantage,
                "k_factor": k,
                "accuracy": metrics["accuracy"],
                "logloss": metrics["logloss"],
            }
        )

        current += 1

    results = (
        pd.DataFrame(results)
        .sort_values(
            ["accuracy", "logloss"],
            ascending=[False, True],
        )
    )

    print()
    print("=" * 70)
    print("TOP 20")
    print("=" * 70)
    print()

    print(results.head(20).to_string(index=False))

    results.to_csv(
        "parameter_search.csv",
        index=False,
    )

    print()
    print("Saved parameter_search.csv")


if __name__ == "__main__":
    main()