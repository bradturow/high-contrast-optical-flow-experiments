"""Verify recovered local data without importing or unpickling it."""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


EXPECTED = {
    "hc20": {
        "size": 71_507_665,
        "sha256": "40a8a1f9674e157ae3bbbc30385572a3ffb879a60264de82c463d97308772535",
    },
    "raw_sample": {
        "size": 857_985_396,
        "sha256": "08189371948199553336ecabacf7f77bc343211ec814d520f6b82062d8220aa1",
    },
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_file(label: str, path: Path) -> bool:
    expected = EXPECTED[label]
    size = path.stat().st_size
    digest = sha256(path)
    ok = size == expected["size"] and digest == expected["sha256"]
    print(f"{label}: {'OK' if ok else 'MISMATCH'}")
    print(f"  path: {path}")
    print(f"  size: {size}")
    print(f"  sha256: {digest}")
    return ok


def verify_sintel(path: Path) -> bool:
    all_files = sum(1 for item in path.rglob("*") if item.is_file())
    flow_root = path / "training" / "flow"
    flow_files = sum(1 for item in flow_root.rglob("*.flo") if item.is_file())
    ok = all_files == 8_559 and flow_files == 1_041
    print(f"sintel: {'OK' if ok else 'MISMATCH'}")
    print(f"  path: {path}")
    print(f"  files: {all_files}")
    print(f"  training flow files: {flow_files}")
    return ok


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--hc20", type=Path)
    parser.add_argument("--raw-sample", type=Path)
    parser.add_argument("--sintel-root", type=Path)
    args = parser.parse_args()

    checks = []
    if args.hc20:
        checks.append(verify_file("hc20", args.hc20))
    if args.raw_sample:
        checks.append(verify_file("raw_sample", args.raw_sample))
    if args.sintel_root:
        checks.append(verify_sintel(args.sintel_root))
    if not checks:
        parser.error("provide at least one local artifact path")
    return 0 if all(checks) else 1


if __name__ == "__main__":
    raise SystemExit(main())

