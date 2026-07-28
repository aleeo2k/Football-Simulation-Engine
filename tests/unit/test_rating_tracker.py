from src.ratings.rating_tracker import RatingTracker


def test_first_match():

    tracker = RatingTracker()

    tracker.update(
        {
            "home_team": "A",
            "away_team": "B",
            "home_xg": 2.0,
            "away_xg": 1.0,
        }
    )

    team = tracker.get_team("A")

    assert team["home_attack"] > 1.35