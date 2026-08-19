from pathlib import Path

import pytest

from optical_flow_experiments import load_experiment_config

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize(
    (
        "name",
        "patches_per_frame",
        "density_k",
        "expected_count",
        "overlap",
        "filament_density_k",
        "filament_count",
    ),
    [
        ("quick", 400, 300, 25_000, 1.99, 300, 30_000),
        ("paper", 4_000, 1_500, 125_000, 1.5, 50, 150_000),
    ],
)
def test_profiles(
    name,
    patches_per_frame,
    density_k,
    expected_count,
    overlap,
    filament_density_k,
    filament_count,
):
    config = load_experiment_config(ROOT / "configs" / f"{name}.toml")
    assert config.name == name
    assert config.dataset.patches_per_frame == patches_per_frame
    assert config.torus.density_k == density_k
    assert config.torus.expected_patch_count == expected_count
    assert config.torus.cover_overlap == overlap
    assert config.filaments.density_k == filament_density_k
    assert config.filaments.expected_patch_count == filament_count
