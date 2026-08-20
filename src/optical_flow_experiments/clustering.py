"""Reproducible fiberwise clustering and boundary-artifact construction."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

import circle_bundles as cb
import numpy as np
from circle_bundles.analysis.fiberwise_clustering import (
    fiberwise_clustering,
    get_filtered_cluster_graph,
    get_weights,
)

from .torus import make_predominant_direction_cover

BOUNDARY_FORMAT_VERSION = 1
HISTORICAL_COMPOSITE_SIZE_PAIRS = ((1_897, 1_088), (1_612, 1_120))
HISTORICAL_COMPOSITE_PATTERN_INDICES = (18, 16)


@dataclass(frozen=True)
class FiberwiseClusteringFit:
    """Initial and graph-filtered outputs of the filament clustering pipeline."""

    predominant_directions: np.ndarray
    directionalities: np.ndarray
    cover: object
    components: np.ndarray
    graph: object
    local_labels: np.ndarray
    summary: dict
    filtered_components: np.ndarray
    filtered_graph: object
    filtered_local_labels: np.ndarray
    component_memberships: np.ndarray
    removed_edge_count: int


@dataclass(frozen=True)
class ComponentH1:
    """Strongest one-dimensional persistence class in each global component."""

    births: np.ndarray
    deaths: np.ndarray
    lifetimes: np.ndarray
    death_birth_ratios: np.ndarray
    circular: np.ndarray


@dataclass(frozen=True)
class BoundaryArtifact:
    """Patches and mutually exclusive memberships for the 28 filament circles."""

    patches: np.ndarray
    memberships: np.ndarray
    source_indices: np.ndarray
    metadata: dict


def fit_fiberwise_clusters(
    data: np.ndarray,
    *,
    n_landmarks: int = 16,
    overlap: float = 1.5,
    dbscan_epsilon: float = 0.3,
    dbscan_min_samples: int = 5,
    graph_weight_threshold: float = 0.07,
    build_pca_embeddings: bool = True,
    verbose: bool = False,
) -> FiberwiseClusteringFit:
    """Run the paper's DBSCAN, overlap-graph, and graph-filtering stages."""

    points = np.asarray(data, dtype=float)
    if points.ndim != 2 or points.shape[1] != 18:
        raise ValueError(f"Expected data with shape (N, 18); got {points.shape}.")
    if not np.isfinite(points).all():
        raise ValueError("data contains non-finite values.")
    if float(dbscan_epsilon) <= 0:
        raise ValueError("dbscan_epsilon must be positive.")
    if int(dbscan_min_samples) <= 0:
        raise ValueError("dbscan_min_samples must be positive.")
    if not 0 <= float(graph_weight_threshold) <= 1:
        raise ValueError("graph_weight_threshold must lie in [0, 1].")

    predominant_directions, directionalities = cb.get_predominant_dirs(points)
    cover = make_predominant_direction_cover(
        predominant_directions,
        n_landmarks=n_landmarks,
        overlap=overlap,
    )
    eps_values = np.full(int(n_landmarks), float(dbscan_epsilon))
    min_sample_values = np.full(int(n_landmarks), int(dbscan_min_samples))
    components, graph, _, local_labels, summary = fiberwise_clustering(
        points,
        cover.U,
        eps_values,
        min_sample_values,
        build_pca_embeddings=build_pca_embeddings,
        verbose=verbose,
    )

    get_weights(graph, method="rel_card2")
    (
        filtered_components,
        filtered_graph,
        _,
        filtered_local_labels,
        component_memberships,
    ) = get_filtered_cluster_graph(
        points,
        graph,
        local_labels,
        thresh=float(graph_weight_threshold),
        rule="to_smaller_cluster",
        show_results=False,
    )

    return FiberwiseClusteringFit(
        predominant_directions=np.asarray(predominant_directions),
        directionalities=np.asarray(directionalities),
        cover=cover,
        components=np.asarray(components),
        graph=graph,
        local_labels=np.asarray(local_labels),
        summary=summary,
        filtered_components=np.asarray(filtered_components),
        filtered_graph=filtered_graph,
        filtered_local_labels=np.asarray(filtered_local_labels),
        component_memberships=np.asarray(component_memberships, dtype=bool),
        removed_edge_count=int(graph.number_of_edges() - filtered_graph.number_of_edges()),
    )


def classify_component_h1(
    data: np.ndarray,
    component_memberships: np.ndarray,
    *,
    n_perm: int = 500,
    random_state: int = 0,
    min_death_birth_ratio: float = 2.0,
) -> ComponentH1:
    """Classify components using the legacy sufficient condition ``death > 2 * birth``."""

    points = np.asarray(data, dtype=float)
    memberships = np.asarray(component_memberships, dtype=bool)
    if memberships.ndim != 2 or memberships.shape[1] != len(points):
        raise ValueError("component_memberships must have shape (n_components, n_samples).")
    if int(n_perm) <= 1:
        raise ValueError("n_perm must be greater than 1.")
    if float(min_death_birth_ratio) <= 1:
        raise ValueError("min_death_birth_ratio must be greater than 1.")

    _, _, rips_results = cb.get_local_rips(
        points,
        memberships,
        maxdim=1,
        n_perm=int(n_perm),
        random_state=int(random_state),
    )
    count = len(memberships)
    births = np.zeros(count)
    deaths = np.zeros(count)
    lifetimes = np.zeros(count)
    ratios = np.zeros(count)
    circular = np.zeros(count, dtype=bool)

    for index, result in enumerate(rips_results):
        diagram = np.empty((0, 2)) if result is None else np.asarray(result["dgms"][1])
        if len(diagram) == 0:
            continue
        birth, death = diagram[np.argmax(diagram[:, 1] - diagram[:, 0])]
        births[index] = float(birth)
        deaths[index] = float(death)
        lifetimes[index] = float(death - birth)
        ratios[index] = float(death / birth) if birth > 0 else np.inf
        circular[index] = bool(death > float(min_death_birth_ratio) * birth)

    return ComponentH1(
        births=births,
        deaths=deaths,
        lifetimes=lifetimes,
        death_birth_ratios=ratios,
        circular=circular,
    )


def _component_for_size(
    memberships: np.ndarray,
    candidates: set[int],
    size: int,
) -> int:
    counts = memberships.sum(axis=1)
    matches = [index for index in sorted(candidates) if int(counts[index]) == int(size)]
    if len(matches) != 1:
        raise ValueError(
            f"Expected one non-circular component of size {size}; found component IDs {matches}."
        )
    return matches[0]


def assemble_paper_boundary_artifact(
    data: np.ndarray,
    component_memberships: np.ndarray,
    circular_components: np.ndarray,
    *,
    random_seed: int = 0,
    synthetic_patches_per_fragment: int = 250,
    composite_size_pairs: tuple[tuple[int, int], ...] = HISTORICAL_COMPOSITE_SIZE_PAIRS,
    composite_pattern_indices: tuple[int, ...] = HISTORICAL_COMPOSITE_PATTERN_INDICES,
    cover_metadata: dict | None = None,
) -> BoundaryArtifact:
    """Apply the manuscript's visual component identifications and build Notebook 03 input.

    The two incomplete circles were identified visually in the legacy analysis. Their
    component numbers were execution-order dependent, so this implementation locates them
    by the recorded component cardinalities instead.
    """

    points = np.asarray(data, dtype=float)
    memberships = np.asarray(component_memberships, dtype=bool)
    circular = np.asarray(circular_components, dtype=bool)
    if memberships.ndim != 2 or memberships.shape[1] != len(points):
        raise ValueError("component_memberships must have shape (n_components, n_samples).")
    if circular.shape != (len(memberships),):
        raise ValueError("circular_components must have one value per component.")
    if np.any(memberships.sum(axis=0) > 1):
        raise ValueError("Filtered component memberships must be mutually exclusive.")
    if len(composite_size_pairs) != len(composite_pattern_indices):
        raise ValueError("Each composite component pair needs one synthetic pattern index.")

    circular_ids = set(np.flatnonzero(circular).tolist())
    if len(circular_ids) != 27:
        raise ValueError(
            f"The paper construction expects 27 circular components; found {len(circular_ids)}."
        )
    torus_id = max(circular_ids, key=lambda index: int(memberships[index].sum()))
    single_circle_ids = circular_ids - {torus_id}
    if len(single_circle_ids) != 26:
        raise ValueError("Expected 26 already-complete filament circles after excluding the torus.")

    noncircular_ids = set(range(len(memberships))) - circular_ids
    composite_ids: list[tuple[int, int]] = []
    used: set[int] = set()
    for size_a, size_b in composite_size_pairs:
        component_a = _component_for_size(memberships, noncircular_ids - used, size_a)
        used.add(component_a)
        component_b = _component_for_size(memberships, noncircular_ids - used, size_b)
        used.add(component_b)
        composite_ids.append((component_a, component_b))

    def first_source_index(index: int) -> int:
        return int(np.flatnonzero(memberships[index])[0])

    ordered_single_ids = sorted(single_circle_ids, key=first_source_index)
    circle_masks = [memberships[index].copy() for index in ordered_single_ids]
    circle_masks.extend(memberships[a] | memberships[b] for a, b in composite_ids)
    final_memberships = np.asarray(circle_masks, dtype=bool)
    if final_memberships.shape[0] != 28:
        raise ValueError(f"Expected 28 filament circles; constructed {len(final_memberships)}.")

    empirical_mask = final_memberships.any(axis=0)
    source_indices = np.flatnonzero(empirical_mask).astype(np.int64)
    boundary_patches = points[empirical_mask]
    boundary_memberships = final_memberships[:, empirical_mask]

    rng = np.random.default_rng(int(random_seed))
    patch_types = cb.get_patch_types_list()
    for offset, pattern_index in enumerate(composite_pattern_indices):
        synthetic, _ = cb.make_step_edges(
            int(synthetic_patches_per_fragment),
            patch_types[int(pattern_index)],
            rng=rng,
        )
        extra_memberships = np.zeros(
            (len(boundary_memberships), len(synthetic)),
            dtype=bool,
        )
        extra_memberships[26 + offset] = True
        boundary_patches = np.vstack((boundary_patches, synthetic))
        boundary_memberships = np.hstack((boundary_memberships, extra_memberships))
        source_indices = np.concatenate(
            (source_indices, np.full(len(synthetic), -1, dtype=np.int64))
        )

    if not np.all(boundary_memberships.sum(axis=0) == 1):
        raise ValueError("Every boundary patch must belong to exactly one filament circle.")

    noise_ids = sorted(noncircular_ids - used)
    metadata = {
        "format": "high-contrast-optical-flow-boundary-circles",
        "format_version": BOUNDARY_FORMAT_VERSION,
        "random_seed": int(random_seed),
        "circle_count": len(boundary_memberships),
        "empirical_patch_count": int(empirical_mask.sum()),
        "synthetic_patch_count": int(np.sum(source_indices == -1)),
        "torus_component_id": int(torus_id),
        "single_circle_component_ids": [int(index) for index in ordered_single_ids],
        "composite_component_ids": [[int(a), int(b)] for a, b in composite_ids],
        "composite_component_sizes": [list(map(int, pair)) for pair in composite_size_pairs],
        "composite_pattern_indices": [int(index) for index in composite_pattern_indices],
        "noise_component_ids": [int(index) for index in noise_ids],
    }
    if cover_metadata is not None:
        metadata["cover"] = dict(cover_metadata)
    return BoundaryArtifact(
        patches=np.asarray(boundary_patches, dtype=np.float64),
        memberships=np.asarray(boundary_memberships, dtype=bool),
        source_indices=source_indices,
        metadata=metadata,
    )


def validate_boundary_artifact(artifact: BoundaryArtifact) -> None:
    """Validate a boundary artifact before analysis or serialization."""

    patches = np.asarray(artifact.patches)
    memberships = np.asarray(artifact.memberships)
    source_indices = np.asarray(artifact.source_indices)
    if patches.ndim != 2 or patches.shape[1] != 18 or not np.isfinite(patches).all():
        raise ValueError(
            f"Expected finite boundary patches with shape (N, 18); got {patches.shape}."
        )
    if memberships.shape != (28, len(patches)):
        raise ValueError(
            f"Expected memberships with shape (28, {len(patches)}); got {memberships.shape}."
        )
    if not np.all(memberships.astype(bool).sum(axis=0) == 1):
        raise ValueError("Every boundary patch must belong to exactly one circle.")
    if source_indices.shape != (len(patches),):
        raise ValueError("source_indices must have one entry per boundary patch.")


def save_boundary_npz(artifact: BoundaryArtifact, path: str | Path) -> Path:
    """Save the Notebook 03 input without Python object arrays or pickle support."""

    validate_boundary_artifact(artifact)
    output = Path(path).expanduser()
    output.parent.mkdir(parents=True, exist_ok=True)
    np.savez_compressed(
        output,
        patches=np.asarray(artifact.patches),
        memberships=np.asarray(artifact.memberships, dtype=bool),
        source_indices=np.asarray(artifact.source_indices, dtype=np.int64),
        metadata_json=np.asarray(json.dumps(artifact.metadata, sort_keys=True)),
    )
    return output


def load_boundary_npz(path: str | Path) -> BoundaryArtifact:
    """Load and validate a portable Notebook 03 input artifact."""

    source = Path(path).expanduser()
    with np.load(source, allow_pickle=False) as archive:
        metadata = json.loads(str(archive["metadata_json"].item()))
        if metadata.get("format_version") != BOUNDARY_FORMAT_VERSION:
            raise ValueError(
                f"Unsupported boundary artifact version: {metadata.get('format_version')}."
            )
        artifact = BoundaryArtifact(
            patches=np.asarray(archive["patches"]),
            memberships=np.asarray(archive["memberships"], dtype=bool),
            source_indices=np.asarray(archive["source_indices"], dtype=np.int64),
            metadata=metadata,
        )
    validate_boundary_artifact(artifact)
    return artifact
