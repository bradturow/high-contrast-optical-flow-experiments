# An Extended Topological Model for High-Contrast Optical Flow

Computational experiments supporting the manuscript *An Extended Topological
Model for High-Contrast Optical Flow*.

> **Staging status:** the source notebooks have been recovered from the legacy
> research archive, but they have not yet been modernized or re-executed in this
> repository. Historical numerical results are recorded only as validation
> targets, not as claims of a fresh reproduction.

## Experiment pipeline

```text
MPI-Sintel flow frames
        |
        v
preprocess high-contrast 3 x 3 flow patches (250,000 patches)
        |
        +--> X(1500, 50): extended optical-flow torus
        |
        +--> X(50, 60): fiberwise clustering and step-edge circles
                              |
                              v
                    boundary double-cover experiment
```

The repository will support two profiles:

- `quick`: a reduced experiment suitable for tutorials and continuous
  integration.
- `paper`: the full parameters reported in the manuscript.

The profiles are documented in `configs/quick.toml` and
`configs/paper.toml`. The historical notebooks did not consistently record
random seeds, so the canonical seed for future runs must be validated before
the results are declared reproduced.

## Repository layout

- `notebooks/`: the three cleanest legacy experiment notebooks, copied exactly.
- `legacy_sources/`: supporting figure/data-exploration notebooks, also copied
  exactly and retained only as migration sources.
- `configs/`: explicit reduced and manuscript-scale parameters.
- `data/`: local data instructions; data files are ignored by Git.
- `provenance/`: source hashes and notes about historical executed notebooks.
- `results/reference/`: numerical targets extracted from the manuscript and
  saved notebook outputs.
- `scripts/`: non-executing integrity checks and, later, reusable experiment
  entry points.

## Data

The MPI-Sintel dataset and legacy pickle artifacts are not included. See
`data/README.md` for the expected local layout and integrity information.

## Development installation

The experiment environment currently points to the reviewed Circle Bundles
commit used for migration:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.in
```

`requirements.in` is a bootstrap specification, not yet a tested lock file. A
platform-specific lock will be generated only after the full notebooks run
successfully in a clean environment.

## Reproducibility status

- [x] Identify and preserve the canonical legacy notebook sources.
- [x] Record hashes for source notebooks and large local data artifacts.
- [x] Separate quick/demo parameters from manuscript-scale parameters.
- [ ] Replace obsolete Circle Bundles API calls.
- [ ] Extract reusable preprocessing and clustering functions from notebooks.
- [ ] Run the quick profile in a clean environment.
- [ ] Run the full paper profile and compare against historical targets.
- [ ] Generate a figure-to-command manifest.
- [ ] Decide public data hosting and repository license.

