"""Reusable code for the high-contrast optical-flow experiments."""

from .config import DatasetConfig, ExperimentConfig, TorusConfig, load_experiment_config
from .data import (
    DenseCore,
    load_preprocessed_npz,
    sample_and_preprocess,
    save_preprocessed_npz,
    select_dense_core,
    validate_preprocessed_table,
)
from .torus import TorusFit, fit_extended_torus, make_predominant_direction_cover

__all__ = [
    "DatasetConfig",
    "DenseCore",
    "ExperimentConfig",
    "TorusConfig",
    "TorusFit",
    "fit_extended_torus",
    "load_experiment_config",
    "load_preprocessed_npz",
    "make_predominant_direction_cover",
    "sample_and_preprocess",
    "save_preprocessed_npz",
    "select_dense_core",
    "validate_preprocessed_table",
]
