#!/usr/bin/env python
"""Run Notebook 02's clustering pipeline and write the portable Notebook 03 input."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np

from optical_flow_experiments import (
    assemble_paper_boundary_artifact,
    classify_component_h1,
    fit_fiberwise_clusters,
    load_experiment_config,
    load_preprocessed_npz,
    save_boundary_npz,
    select_dense_core,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--preprocessed", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--summary", type=Path)
    parser.add_argument("--h1-n-perm", type=int, default=500)
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    filament = config.filaments
    table = load_preprocessed_npz(args.preprocessed)
    core = select_dense_core(
        table,
        density_k=filament.density_k,
        density_fraction=filament.density_fraction,
    )
    if len(core.data) != filament.expected_patch_count:
        raise ValueError(
            f"Expected {filament.expected_patch_count} selected patches; found {len(core.data)}."
        )

    fit = fit_fiberwise_clusters(
        core.data,
        n_landmarks=filament.cover_landmarks,
        overlap=filament.cover_overlap,
        dbscan_epsilon=filament.dbscan_epsilon,
        dbscan_min_samples=filament.dbscan_min_samples,
        graph_weight_threshold=filament.graph_weight_threshold,
        build_pca_embeddings=False,
    )
    h1 = classify_component_h1(
        core.data,
        fit.component_memberships,
        n_perm=args.h1_n_perm,
        random_state=config.random_seed,
    )
    artifact = assemble_paper_boundary_artifact(
        core.data,
        fit.component_memberships,
        h1.circular,
        random_seed=config.random_seed,
        synthetic_patches_per_fragment=filament.synthetic_patches_per_fragment,
        cover_metadata={
            "metric": "RP1 angular distance",
            "landmarks": filament.cover_landmarks,
            "angular_radius": (
                filament.cover_overlap * np.pi / (2 * filament.cover_landmarks)
            ),
            "angular_overlap": filament.cover_overlap,
        },
    )
    output = save_boundary_npz(artifact, args.output)
    sha256 = hashlib.sha256(output.read_bytes()).hexdigest()

    initial_ids = np.unique(fit.components[fit.components >= 0])
    summary = {
        "profile": config.name,
        "selected_patch_count": len(core.data),
        "initial_global_clusters": len(initial_ids),
        "initial_unclustered_points": int(np.sum(fit.components == -1)),
        "largest_initial_component_points": int(np.max(fit.summary["point_counts"])),
        "removed_edges": fit.removed_edge_count,
        "filtered_components": len(fit.component_memberships),
        "filtered_components_with_usable_h1": int(h1.circular.sum()),
        "boundary": artifact.metadata,
        "artifact_sha256": sha256,
    }
    if args.summary is not None:
        args.summary.parent.mkdir(parents=True, exist_ok=True)
        args.summary.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(f"Saved portable boundary artifact to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
