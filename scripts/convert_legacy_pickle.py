#!/usr/bin/env python
"""Convert the trusted recovered HC20 pandas pickle to portable NPZ arrays."""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from optical_flow_experiments import save_preprocessed_npz, validate_preprocessed_table


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Trusted legacy pandas pickle")
    parser.add_argument("output", type=Path, help="Destination .npz artifact")
    args = parser.parse_args()

    table = pd.read_pickle(args.input)
    validate_preprocessed_table(table)
    destination = save_preprocessed_npz(table, args.output)
    print(f"Converted {len(table)} rows to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
