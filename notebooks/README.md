# Core notebooks

`00_sintel_data_diagnostics.ipynb`, `01_extended_torus.ipynb`,
`02_fiberwise_clustering.ipynb`, and `03_boundary_double_cover.ipynb` are the
modernized, runnable experiments.

Notebook 00 is a cleaned-up continuation of the recovered *Exploring The Sintel
Dataset* notebook. It loads the portable preprocessed artifact, supports quick
and paper profiles, reproduces the manuscript's four-way directionality
comparison, and writes a machine-readable run record. When `MPI_SINTEL_ROOT` is
set, it also renders an optional raw-frame optical-flow overlay. The
weak-directionality samples, top-one-percent projections, and original
scene/frame choices still need to be identified. Exploratory contrast plots are
left in the preserved legacy source because the manuscript does not report
them.

Notebook 01 keeps the tutorial-style Circle Bundles analysis visible in the
notebook, with a short quick/paper parameter block and portable artifact
loading. Its paper profile reconstructs the six-panel direct-persistence
comparison in Figure 6. The two empirical panels match the submitted diagrams
exactly; the synthetic panels use a documented deterministic seed and the
current Circle Bundles noise-normalization convention because those historical
details were not recorded.

Notebook 02 keeps the recovered fiberwise-clustering analysis visible through
direct `circle_bundles` calls. It is deliberately publication-only: it
reconstructs the exact legacy cover, reproduces Figures 17--26, records the
manuscript-specific component pairings by stable cardinality, and writes
`data/K_50_60_Circles.v1.npz` for Notebook 03. A reduced mode would not support
the later dataset-specific component identifications.

Notebook 03 is also publication-only. It loads the portable Notebook 02 output,
lifts predominant direction to $S^1$, constructs a 16-set cover directly with
the current angular metric, confirms $w_1=0$ and Euler class zero, and computes
a global toroidal coordinate for all 55,501 patches. Its stable paper output is
`results/paper/figures/boundary_torus.pdf` (Figure 30). Interactive bundle views
remain available as an optional snippet but are not started during headless
execution.

The three numbered `real_optical_flow_*` notebooks remain exact copies of the
cleanest sources found in the legacy archive. They intentionally retain their
obsolete imports, placeholder paths, and known defects as provenance.

1. `01_real_optical_flow_torus.ipynb`: reduced extended-torus demonstration.
   It must be restored to the manuscript-scale `X(1500, 50)` experiment for the
   paper profile.
2. `02_real_optical_flow_fiberwise_clustering.ipynb`: provenance source for the
   main `X(50, 60)` filament clustering experiment; replaced operationally by
   `02_fiberwise_clustering.ipynb`.
3. `03_real_optical_flow_boundary_double_cover.ipynb`: the boundary bundle
   analysis, dependent on the output of notebook 02.

Do not treat output-free execution as sufficient validation. The numerical
targets in `../results/reference/expected_results.json` must also be checked.
