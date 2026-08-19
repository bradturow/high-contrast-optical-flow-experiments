"""Reusable code for the high-contrast optical-flow experiments."""

from .clustering import (
    BoundaryArtifact,
    ComponentH1,
    FiberwiseClusteringFit,
    assemble_paper_boundary_artifact,
    classify_component_h1,
    fit_fiberwise_clusters,
    load_boundary_npz,
    save_boundary_npz,
    validate_boundary_artifact,
)
from .config import (
    DatasetConfig,
    ExperimentConfig,
    FilamentConfig,
    TorusConfig,
    load_experiment_config,
)
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
    "BoundaryArtifact",
    "ComponentH1",
    "DatasetConfig",
    "DenseCore",
    "ExperimentConfig",
    "FiberwiseClusteringFit",
    "FilamentConfig",
    "TorusConfig",
    "TorusFit",
    "assemble_paper_boundary_artifact",
    "classify_component_h1",
    "fit_extended_torus",
    "fit_fiberwise_clusters",
    "load_boundary_npz",
    "load_experiment_config",
    "load_preprocessed_npz",
    "make_predominant_direction_cover",
    "sample_and_preprocess",
    "save_boundary_npz",
    "save_preprocessed_npz",
    "select_dense_core",
    "validate_boundary_artifact",
    "validate_preprocessed_table",
]
