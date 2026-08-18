from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from optical_flow_experiments import (
    load_preprocessed_npz,
    save_preprocessed_npz,
    select_dense_core,
    validate_preprocessed_table,
)


def make_table() -> pd.DataFrame:
    rows = 10
    return pd.DataFrame(
        {
            "patch": [np.full(18, value, dtype=float) for value in range(rows)],
            "row": np.arange(rows),
            "column": np.arange(rows) + 10,
            "scene": np.ones(rows, dtype=int),
            "frame": np.ones(rows, dtype=int),
            "norm": np.linspace(1, 2, rows),
            "x mean": np.zeros(rows),
            "y mean": np.zeros(rows),
            "density_3": np.arange(rows, dtype=float) + 1,
        }
    )


def test_select_dense_core_orders_by_requested_density():
    core = select_dense_core(make_table(), density_k=3, density_fraction=0.3)
    assert core.data.shape == (3, 18)
    np.testing.assert_array_equal(core.table["density_3"], [10, 9, 8])
    np.testing.assert_array_equal(core.data[:, 0], [9, 8, 7])


def test_portable_npz_round_trip(tmp_path: Path):
    original = make_table()
    artifact = save_preprocessed_npz(original, tmp_path / "patches.npz")
    restored = load_preprocessed_npz(artifact)
    assert list(restored.columns) == list(original.columns)
    np.testing.assert_allclose(np.vstack(restored["patch"]), np.vstack(original["patch"]))
    for column in original.columns[1:]:
        np.testing.assert_allclose(restored[column], original[column])


def test_validation_rejects_non_finite_density():
    table = make_table()
    table.loc[0, "density_3"] = np.nan
    with pytest.raises(ValueError, match="finite positive"):
        validate_preprocessed_table(table)
