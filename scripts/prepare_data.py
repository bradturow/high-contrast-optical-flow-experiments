#!/usr/bin/env python
"""Create a portable preprocessed artifact from MPI-Sintel flow frames."""

from __future__ import annotations

import argparse
from pathlib import Path

from optical_flow_experiments import (
    load_experiment_config,
    sample_and_preprocess,
    save_preprocessed_npz,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--flow-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    config = load_experiment_config(args.config)
    print(f"Preparing profile: {config.name}")
    table = sample_and_preprocess(args.flow_root, config)
    artifact = save_preprocessed_npz(table, args.output)
    print(f"Saved {len(table)} preprocessed patches to {artifact}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
