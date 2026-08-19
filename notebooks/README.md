# Core notebooks

`01_extended_torus.ipynb` and `02_fiberwise_clustering.ipynb` are the modernized,
runnable experiments. They use the current Circle Bundles API, typed
quick/paper profiles, and portable artifact formats.

Notebook 02 defaults to the paper profile. It reproduces the saved clustering
structure and writes `data/K_50_60_Circles.v1.npz` for Notebook 03. Its quick
profile stops after clustering diagnostics because the final two component
pairings were manuscript-specific visual identifications.

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
