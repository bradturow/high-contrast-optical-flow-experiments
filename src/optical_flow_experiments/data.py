"""Deterministic sampling, preprocessing, and portable artifact utilities."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import circle_bundles as cb
import numpy as np
import pandas as pd

from .config import ExperimentConfig

BASE_METADATA_COLUMNS = ("row", "column", "scene", "frame", "norm", "x mean", "y mean")
FORMAT_VERSION = 1


@dataclass(frozen=True)
class DenseCore:
    """A density-selected point cloud and the corresponding table rows."""

    data: np.ndarray
    table: pd.DataFrame
    density_k: int
    density_fraction: float


def validate_preprocessed_table(table: pd.DataFrame) -> None:
    """Validate the schema and numerical health of a preprocessed patch table."""

    required = {"patch", *BASE_METADATA_COLUMNS}
    missing = sorted(required.difference(table.columns))
    if missing:
        raise ValueError(f"Preprocessed table is missing columns: {missing}")
    if len(table) == 0:
        raise ValueError("Preprocessed table is empty.")

    patches = np.vstack(table["patch"].to_numpy())
    if patches.ndim != 2 or patches.shape[1] != 18:
        raise ValueError(f"Expected an (N, 18) patch matrix; got {patches.shape}.")
    if not np.isfinite(patches).all():
        raise ValueError("Patch matrix contains non-finite values.")

    density_columns = [column for column in table.columns if column.startswith("density_")]
    if not density_columns:
        raise ValueError("Preprocessed table contains no density columns.")
    for column in density_columns:
        values = table[column].to_numpy(dtype=float)
        if not np.isfinite(values).all() or np.any(values <= 0):
            raise ValueError(f"{column} must contain finite positive values.")


def sample_and_preprocess(flow_root: str | Path, config: ExperimentConfig) -> pd.DataFrame:
    """Sample Sintel flow frames and reproduce the configured preprocessing pipeline."""

    dataset = config.dataset
    patch_table, _ = cb.get_patch_sample(
        Path(flow_root).expanduser(),
        patches_per_frame=dataset.patches_per_frame,
        d=dataset.patch_size,
        random_state=config.random_seed,
    )

    if dataset.expected_raw_patch_count is not None:
        observed = len(patch_table)
        if observed != dataset.expected_raw_patch_count:
            raise ValueError(
                "Raw patch count does not match the configured Sintel inventory: "
                f"expected {dataset.expected_raw_patch_count}, observed {observed}."
            )

    if dataset.raw_sample_cap is not None and len(patch_table) > dataset.raw_sample_cap:
        patch_table = patch_table.sample(
            n=dataset.raw_sample_cap,
            random_state=config.random_seed,
        ).reset_index(drop=True)

    processed = cb.preprocess_flow_patches(
        patch_table,
        hc_frac=dataset.high_contrast_fraction,
        max_samples=dataset.preprocessed_sample_cap,
        k_list=dataset.density_k_values,
        random_state=config.random_seed,
    )
    validate_preprocessed_table(processed)
    return processed


def select_dense_core(
    table: pd.DataFrame,
    *,
    density_k: int,
    density_fraction: float,
) -> DenseCore:
    """Select the top fraction by a named k-nearest-neighbor density estimate."""

    validate_preprocessed_table(table)
    if not 0 < float(density_fraction) <= 1:
        raise ValueError("density_fraction must lie in (0, 1].")

    density_column = f"density_{int(density_k)}"
    if density_column not in table.columns:
        available = sorted(column for column in table.columns if column.startswith("density_"))
        raise ValueError(f"Missing {density_column}; available density columns: {available}")

    ordered = table.sort_values(
        density_column,
        ascending=False,
        kind="mergesort",
    ).reset_index(drop=True)
    count = int(float(density_fraction) * len(ordered))
    if count == 0:
        raise ValueError("density_fraction selected zero points.")
    selected = ordered.iloc[:count].copy().reset_index(drop=True)
    data = np.vstack(selected["patch"].to_numpy()).astype(np.float64, copy=False)
    return DenseCore(
        data=data,
        table=selected,
        density_k=int(density_k),
        density_fraction=float(density_fraction),
    )


def save_preprocessed_npz(table: pd.DataFrame, path: str | Path) -> Path:
    """Save a preprocessed table as compressed, non-object NumPy arrays."""

    validate_preprocessed_table(table)
    output = Path(path).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)

    scalar_columns = [column for column in table.columns if column != "patch"]
    key_map = {column: f"column_{index}" for index, column in enumerate(scalar_columns)}
    metadata = {
        "format": "high-contrast-optical-flow-preprocessed",
        "format_version": FORMAT_VERSION,
        "scalar_columns": scalar_columns,
        "key_map": key_map,
    }
    payload: dict[str, np.ndarray] = {
        "patches": np.vstack(table["patch"].to_numpy()),
        "metadata_json": np.asarray(json.dumps(metadata, sort_keys=True)),
    }
    for column, key in key_map.items():
        payload[key] = table[column].to_numpy()

    np.savez_compressed(output, **payload)
    return output


def load_preprocessed_npz(path: str | Path) -> pd.DataFrame:
    """Load a portable artifact without enabling NumPy pickle support."""

    source = Path(path).expanduser()
    with np.load(source, allow_pickle=False) as archive:
        metadata = json.loads(str(archive["metadata_json"].item()))
        if metadata.get("format_version") != FORMAT_VERSION:
            raise ValueError(
                f"Unsupported artifact format version: {metadata.get('format_version')}."
            )
        patches = np.asarray(archive["patches"])
        columns = {
            column: np.asarray(archive[metadata["key_map"][column]])
            for column in metadata["scalar_columns"]
        }

    table = pd.DataFrame(columns)
    table.insert(0, "patch", list(patches))
    validate_preprocessed_table(table)
    return table
