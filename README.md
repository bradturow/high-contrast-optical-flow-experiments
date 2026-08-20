# An Extended Topological Model for High-Contrast Optical Flow

Computational experiments supporting the manuscript *An Extended Topological
Model for High-Contrast Optical Flow*.

> **Migration status:** the recovered sources are preserved unchanged. The
> modernized Sintel-diagnostics, extended-torus, fiberwise-clustering, and
> boundary-double-cover notebooks now execute in a clean environment. The
> diagnostics notebook reproduces the manuscript's directionality comparison,
> the manuscript-scale $X(1500,50)$ and $X(50,60)$ analyses both run from the
> verified recovered preprocessing artifact, Notebook 02 produces a deterministic pickle-free
> boundary artifact, and Notebook 03 recovers its trivial lifted circle bundle
> and Figure 30. Rebuilding the 250,000-row artifact from raw Sintel remains to
> be completed.

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

The diagnostics and extended-torus workflows support two profiles:

- `quick`: a reduced experiment suitable for tutorials and continuous
  integration.
- `paper`: the full parameters reported in the manuscript.

The profiles are documented in `configs/quick.toml` and `configs/paper.toml`.
The fiberwise-clustering and boundary-double-cover notebooks are deliberately
publication-only because their later stages identify components specific to
the paper dataset. The historical notebooks did not consistently record random
seeds, so the canonical seed for future runs must be validated before the
results are declared reproduced.

## Repository layout

- `notebooks/`: four modernized paper workflows plus three exact legacy
  migration sources.
- `legacy_sources/`: supporting figure/data-exploration notebooks, also copied
  exactly and retained only as migration sources.
- `configs/`: explicit reduced and manuscript-scale parameters.
- `data/`: local data instructions; data files are ignored by Git.
- `provenance/`: source hashes, historical notes, and the manuscript
  figure-to-workflow inventory.
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

## Run the Sintel diagnostics

Notebook 00 defaults to the paper profile and reads the portable preprocessed
artifact. It reproduces the four-way directionality comparison and writes a
machine-readable run record:

```bash
source .venv/bin/activate
jupyter nbconvert --to notebook --execute \
  notebooks/00_sintel_data_diagnostics.ipynb \
  --output 00_sintel_diagnostics_executed.ipynb \
  --output-dir results/paper \
  --ExecutePreprocessor.timeout=1800
```

Set `OPTICAL_FLOW_PROFILE=quick` for the reduced artifact. If the original raw
frames are available, set `MPI_SINTEL_ROOT=/path/to/MPI-Sintel-complete` to add
the optional frame/flow overlay diagnostic. Generated figures and run records
are written below `results/<profile>/` and are ignored by Git.

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

Notebook 01's paper profile writes stable manuscript files for Figures 6, 7 and
14--16 under `results/paper/figures/`. Its two empirical persistence panels
match the submitted Figure 6 diagrams exactly. The four noisy synthetic panels
use an explicit modern seed and noise normalization; the corresponding
historical choices were not recorded. Figure 8 is intentionally retained as a
contextual manuscript asset because it uses a separate Adams-style six-set
cover rather than the 16-set cover used for the bundle computation.

## Run the fiberwise-clustering experiment

Notebook 02 is publication-only because several stages identify components
specific to the complete paper dataset. The equivalent non-interactive command
is:

```bash
source .venv/bin/activate
python scripts/run_fiberwise_clustering.py \
  --config configs/paper.toml \
  --preprocessed data/HC20_Flow_Patches.v1.npz \
  --output data/K_50_60_Circles.v1.npz \
  --summary results/paper/fiberwise_clustering_metrics.json
```

The locked environment reproduces the complete saved clustering structure: 38
initial components, 18 initially unclustered patches, 14 removed graph edges,
45 filtered components, 27 components with usable $H_1$, and 28 final filament
circles. Reconstructing the legacy doubled-angle cover exactly also recovers the
historical 55,001 empirical circle patches and the 55,501-patch augmented
boundary artifact. Notebook 02 regenerates the manuscript outputs for Figures
17--26 under stable filenames in `results/paper/figures/`.

For provenance, the executed clustering code uses intersection cardinality
divided by the mean endpoint cardinality for `rel_card2`. The current manuscript
formula displays a maximum denominator; that textual formula should be
reconciled before publication.

## Run the boundary double-cover experiment

Notebook 03 is publication-only and consumes the portable artifact written by
Notebook 02:

```bash
source .venv/bin/activate
jupyter nbconvert --to notebook --execute \
  notebooks/03_boundary_double_cover.ipynb \
  --output 03_boundary_double_cover_executed.ipynb \
  --output-dir results/paper \
  --ExecutePreprocessor.timeout=1800
```

The notebook constructs a 16-set lifted cover directly with the current
$S^1$ angular metric, confirms that the boundary circle bundle is orientable
with zero Euler class, computes a global toroidal coordinate for all 55,501
patches, and writes Figure 30 to
`results/paper/figures/boundary_torus.pdf`.

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
- [x] Inventory every figure environment used by the submitted manuscript.
- [x] Reproduce the manuscript directionality comparison from the portable
  artifact.
- [x] Reconstruct the six-panel global-persistence comparison in Figure 6.
- [x] Reproduce the Notebook 02 manuscript outputs for Figures 17--26.
- [ ] Rebuild the 250,000-row paper artifact from raw Sintel frames.
- [x] Modernize and validate the boundary double-cover experiment and Figure 30.
- [ ] Generate a figure-to-command manifest.
- [ ] Decide public data hosting and repository license.
