from src.prediction.poisson import PoissonModel


def test_probability_matrix_sum():

    model = PoissonModel()

    matrix = model.score_matrix(
        1.5,
        1.2,
    )

    total = sum(
        sum(row)
        for row in matrix
    )

    assert 0.995 < total < 1.0001