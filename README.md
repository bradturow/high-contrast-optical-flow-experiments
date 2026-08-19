# An Extended Topological Model for High-Contrast Optical Flow

Computational experiments supporting the manuscript *An Extended Topological
Model for High-Contrast Optical Flow*.

> **Migration status:** the recovered sources are preserved unchanged. The
> modernized extended-torus and fiberwise-clustering notebooks now execute in a
> clean environment. The manuscript-scale $X(1500,50)$ and $X(50,60)$ analyses
> both run from the verified recovered preprocessing artifact, and Notebook 02
> produces a deterministic, pickle-free input for the boundary experiment.
> Rebuilding the 250,000-row artifact from raw Sintel and modernizing Notebook 03
> remain to be completed.

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

- `notebooks/`: the modernized extended-torus and fiberwise-clustering
  experiments plus three exact legacy migration sources.
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

`requirements.in` is the human-maintained bootstrap specification.
`requirements-lock.txt` records the clean environment used for the successful
macOS arm64 / Python 3.13 quick-profile run.

## Run the extended-torus experiment

To construct the quick artifact deterministically from raw Sintel and execute
the notebook:

```bash
source .venv/bin/activate
python scripts/prepare_data.py \
  --config configs/quick.toml \
  --flow-root /path/to/MPI-Sintel-complete/training/flow \
  --output data/preprocessed_quick.v1.npz
jupyter nbconvert --to notebook --execute \
  notebooks/01_extended_torus.ipynb \
  --output 01_extended_torus_executed.ipynb \
  --output-dir results/quick \
  --ExecutePreprocessor.timeout=1800
```

For the manuscript-scale analysis, set `OPTICAL_FLOW_PROFILE` and
`OPTICAL_FLOW_PREPROCESSED` to `configs/paper.toml` and a compatible 250,000-row
portable artifact, respectively.

## Run the fiberwise-clustering experiment

Notebook 02 defaults to the paper profile. The equivalent non-interactive
command is:

```bash
source .venv/bin/activate
python scripts/run_fiberwise_clustering.py \
  --config configs/paper.toml \
  --preprocessed data/HC20_Flow_Patches.v1.npz \
  --output data/K_50_60_Circles.v1.npz \
  --summary results/paper/fiberwise_clustering_metrics.json
```

The locked environment reproduces all major saved clustering results: 38
initial components, 18 initially unclustered patches, 14 removed graph edges,
45 filtered components, 27 components with usable $H_1$, and 28 final filament
circles. It assigns 55,012 empirical patches to those circles, 11 more than the
55,001 recorded by the historical Python 3.10 execution. Both values are kept
in the reference results so this small dependency-sensitive discrepancy is
visible.

## Reproducibility status

- [x] Identify and preserve the canonical legacy notebook sources.
- [x] Record hashes for source notebooks and large local data artifacts.
- [x] Separate quick/demo parameters from manuscript-scale parameters.
- [x] Replace obsolete Circle Bundles API calls in the extended-torus workflow.
- [x] Extract reusable preprocessing and dense-core selection functions.
- [x] Run the quick profile from raw Sintel frames in a clean environment.
- [x] Run the $X(1500,50)$ paper analysis from the verified recovered artifact.
- [x] Reproduce the $X(50,60)$ fiberwise-clustering structure.
- [x] Generate a portable, validated Notebook 03 input artifact.
- [ ] Rebuild the 250,000-row paper artifact from raw Sintel frames.
- [ ] Modernize and validate the boundary double-cover experiment.
- [ ] Generate a figure-to-command manifest.
- [ ] Decide public data hosting and repository license.
