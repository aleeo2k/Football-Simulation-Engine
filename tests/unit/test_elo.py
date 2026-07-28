from src.ratings.elo_tracker import EloTracker


def test_home_team_loses_rating_after_home_draw():

    elo = EloTracker()

    before_home = elo.get_team("A")
    before_away = elo.get_team("B")

    elo.update(
        {
            "home_team": "A",
            "away_team": "B",
            "home_goals": 1,
            "away_goals": 1,
        }
    )

    after_home = elo.get_team("A")
    after_away = elo.get_team("B")

    # Домашняя команда должна немного потерять рейтинг,
    # потому что ожидалась победа.

    assert after_home < before_home

    # Гостевая должна немного приобрести.

    assert after_away > before_away

    # Общий рейтинг сохраняется.

    assert abs(
        (after_home + after_away)
        -
        (before_home + before_away)
    ) < 1e-6