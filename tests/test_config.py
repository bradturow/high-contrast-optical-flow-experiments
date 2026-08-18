from pathlib import Path

import pytest

from optical_flow_experiments import load_experiment_config

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    ("name", "patches_per_frame", "density_k", "expected_count", "overlap"),
    [
        ("quick", 400, 300, 25_000, 1.99),
        ("paper", 4_000, 1_500, 125_000, 1.5),
    ],
)
def test_profiles(name, patches_per_frame, density_k, expected_count, overlap):
    config = load_experiment_config(ROOT / "configs" / f"{name}.toml")
    assert config.name == name
    assert config.dataset.patches_per_frame == patches_per_frame
    assert config.torus.density_k == density_k
    assert config.torus.expected_patch_count == expected_count
    assert config.torus.cover_overlap == overlap
