"""Typed configuration loading for quick and manuscript-scale experiments."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python 3.10 compatibility
    import tomli as tomllib


@dataclass(frozen=True)
class DatasetConfig:
    patch_size: int
    patches_per_frame: int
    high_contrast_fraction: float
    preprocessed_sample_cap: int
    density_k_values: tuple[int, ...]
    raw_sample_cap: int | None = None
    expected_raw_patch_count: int | None = None


@dataclass(frozen=True)
class TorusConfig:
    density_k: int
    density_fraction: float
    expected_patch_count: int
    cover_landmarks: int
    cover_overlap: float


@dataclass(frozen=True)
class ExperimentConfig:
    name: str
    description: str
    random_seed: int
    historical_seed: str
    dataset: DatasetConfig
    torus: TorusConfig
    source_path: Path


def _positive_int(section: Mapping[str, Any], key: str) -> int:
    value = int(section[key])
    if value <= 0:
        raise ValueError(f"{key} must be positive; got {value}.")
    return value


def _fraction(section: Mapping[str, Any], key: str) -> float:
    value = float(section[key])
    if not 0 < value <= 1:
        raise ValueError(f"{key} must lie in (0, 1]; got {value}.")
    return value


def load_experiment_config(path: str | Path) -> ExperimentConfig:
    """Load and validate one experiment profile from TOML."""

    source_path = Path(path).expanduser().resolve()
    with source_path.open("rb") as stream:
        raw = tomllib.load(stream)

    profile = raw["profile"]
    dataset_raw = raw["dataset"]
    torus_raw = raw["torus"]

    density_k_values = tuple(sorted({int(k) for k in dataset_raw["density_k_values"]}))
    if not density_k_values or density_k_values[0] <= 0:
        raise ValueError("density_k_values must contain positive integers.")

    raw_sample_cap_value = dataset_raw.get("raw_sample_cap")
    expected_raw_value = dataset_raw.get("expected_raw_patch_count")
    dataset = DatasetConfig(
        patch_size=_positive_int(dataset_raw, "patch_size"),
        patches_per_frame=_positive_int(dataset_raw, "patches_per_frame"),
        raw_sample_cap=None if raw_sample_cap_value is None else int(raw_sample_cap_value),
        expected_raw_patch_count=None if expected_raw_value is None else int(expected_raw_value),
        high_contrast_fraction=_fraction(dataset_raw, "high_contrast_fraction"),
        preprocessed_sample_cap=_positive_int(dataset_raw, "preprocessed_sample_cap"),
        density_k_values=density_k_values,
    )

    torus = TorusConfig(
        density_k=_positive_int(torus_raw, "density_k"),
        density_fraction=_fraction(torus_raw, "density_fraction"),
        expected_patch_count=_positive_int(torus_raw, "expected_patch_count"),
        cover_landmarks=_positive_int(torus_raw, "cover_landmarks"),
        cover_overlap=float(torus_raw["cover_overlap"]),
    )
    if torus.density_k not in dataset.density_k_values:
        raise ValueError(f"torus density_k={torus.density_k} is absent from density_k_values.")
    if torus.cover_overlap <= 1:
        raise ValueError("cover_overlap must be greater than 1 so adjacent cover sets overlap.")

    return ExperimentConfig(
        name=str(profile["name"]),
        description=str(profile["description"]),
        random_seed=int(profile["random_seed"]),
        historical_seed=str(profile["historical_seed"]),
        dataset=dataset,
        torus=torus,
        source_path=source_path,
    )
