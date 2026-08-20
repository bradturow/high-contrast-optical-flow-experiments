from pathlib import Path

import numpy as np
import pytest

from optical_flow_experiments import (
    BoundaryArtifact,
    assemble_paper_boundary_artifact,
    load_boundary_npz,
    save_boundary_npz,
    validate_boundary_artifact,
)


def make_mock_components():
    counts = [50, *([1] * 26), 2, 3, 4, 5, *([1] * 14)]
    memberships = np.zeros((45, sum(counts)), dtype=bool)
    start = 0
    for component, count in enumerate(counts):
        memberships[component, start : start + count] = True
        start += count
    circular = np.zeros(45, dtype=bool)
    circular[:27] = True
    data = np.arange(sum(counts) * 18, dtype=float).reshape(sum(counts), 18)
    return data, memberships, circular


def test_assemble_boundary_uses_cardinalities_not_component_numbers():
    data, memberships, circular = make_mock_components()
    artifact = assemble_paper_boundary_artifact(
        data,
        memberships,
        circular,
        random_seed=7,
        synthetic_patches_per_fragment=2,
        composite_size_pairs=((2, 3), (4, 5)),
        composite_pattern_indices=(18, 16),
        cover_metadata={"metric": "RP1 angular distance", "angular_overlap": 1.5},
    )
    validate_boundary_artifact(artifact)
    assert artifact.patches.shape == (44, 18)
    assert artifact.memberships.shape == (28, 44)
    assert artifact.metadata["empirical_patch_count"] == 40
    assert artifact.metadata["synthetic_patch_count"] == 4
    assert artifact.metadata["torus_component_id"] == 0
    assert artifact.metadata["composite_component_ids"] == [[27, 28], [29, 30]]
    assert artifact.metadata["cover"]["angular_overlap"] == 1.5
    np.testing.assert_array_equal(artifact.source_indices[-4:], -1)


def test_boundary_npz_round_trip(tmp_path: Path):
    data, memberships, circular = make_mock_components()
    artifact = assemble_paper_boundary_artifact(
        data,
        memberships,
        circular,
        synthetic_patches_per_fragment=1,
        composite_size_pairs=((2, 3), (4, 5)),
        composite_pattern_indices=(18, 16),
    )
    path = save_boundary_npz(artifact, tmp_path / "boundary.npz")
    restored = load_boundary_npz(path)
    np.testing.assert_allclose(restored.patches, artifact.patches)
    np.testing.assert_array_equal(restored.memberships, artifact.memberships)
    np.testing.assert_array_equal(restored.source_indices, artifact.source_indices)
    assert restored.metadata == artifact.metadata


def test_boundary_validation_rejects_overlapping_memberships():
    artifact = BoundaryArtifact(
        patches=np.zeros((1, 18)),
        memberships=np.ones((28, 1), dtype=bool),
        source_indices=np.array([0]),
        metadata={"format_version": 1},
    )
    with pytest.raises(ValueError, match="exactly one circle"):
        validate_boundary_artifact(artifact)
