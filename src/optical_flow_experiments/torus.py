"""Current-API implementation of the extended optical-flow torus analysis."""

from __future__ import annotations

from dataclasses import dataclass

import circle_bundles as cb
import numpy as np


@dataclass(frozen=True)
class TorusFit:
    predominant_directions: np.ndarray
    directionalities: np.ndarray
    cover: object
    bundle: cb.Bundle
    local_trivializations: object
    classes: object
    fiber_angles: np.ndarray


def make_predominant_direction_cover(
    predominant_directions: np.ndarray,
    *,
    n_landmarks: int = 16,
    overlap: float = 1.5,
):
    """Cover RP1 by overlapping angular metric balls."""

    directions = np.asarray(predominant_directions, dtype=float).reshape(-1, 1)
    if len(directions) == 0:
        raise ValueError("predominant_directions is empty.")
    if int(n_landmarks) < 3:
        raise ValueError("n_landmarks must be at least 3.")
    if float(overlap) <= 1:
        raise ValueError("overlap must be greater than 1.")

    landmarks = np.linspace(0, np.pi, int(n_landmarks), endpoint=False).reshape(-1, 1)
    radius = float(overlap) * np.pi / (2 * int(n_landmarks))
    return cb.get_metric_ball_cover(
        directions,
        landmarks,
        radius=radius,
        metric=cb.RP1AngleMetric(),
    )


def fit_extended_torus(
    data: np.ndarray,
    *,
    n_landmarks: int = 16,
    overlap: float = 1.5,
    show_summaries: bool = False,
) -> TorusFit:
    """Fit local bundle coordinates, classes, and a global fiber angle."""

    points = np.asarray(data, dtype=float)
    if points.ndim != 2 or points.shape[1] != 18:
        raise ValueError(f"Expected data with shape (N, 18); got {points.shape}.")
    if not np.isfinite(points).all():
        raise ValueError("data contains non-finite values.")

    predominant_directions, directionalities = cb.get_predominant_dirs(points)
    cover = make_predominant_direction_cover(
        predominant_directions,
        n_landmarks=n_landmarks,
        overlap=overlap,
    )
    bundle = cb.Bundle(X=points, cover=cover)
    local = bundle.get_local_trivs(show_summary=show_summaries)
    classes = bundle.get_classes(show_classes=show_summaries)
    fiber_angles = bundle.get_global_trivialization()
    return TorusFit(
        predominant_directions=predominant_directions,
        directionalities=directionalities,
        cover=cover,
        bundle=bundle,
        local_trivializations=local,
        classes=classes,
        fiber_angles=np.asarray(fiber_angles, dtype=float),
    )
