import numpy as np

from optical_flow_experiments import make_predominant_direction_cover


def test_predominant_direction_cover_has_partition_of_unity():
    directions = np.linspace(0, np.pi, 1_000, endpoint=False)
    cover = make_predominant_direction_cover(directions, n_landmarks=16, overlap=1.5)

    assert cover.U.shape == (16, 1_000)
    assert cover.pou.shape == cover.U.shape
    assert np.all(cover.U.sum(axis=0) >= 1)
    np.testing.assert_allclose(cover.pou.sum(axis=0), 1)
