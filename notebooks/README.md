# Core notebooks

These three notebooks are exact copies of the cleanest sources found in the
legacy archive. They intentionally retain their obsolete imports, placeholder
paths, and known defects until the migration work begins.

1. `01_real_optical_flow_torus.ipynb`: reduced extended-torus demonstration.
   It must be restored to the manuscript-scale `X(1500, 50)` experiment for the
   paper profile.
2. `02_real_optical_flow_fiberwise_clustering.ipynb`: the main `X(50, 60)`
   filament clustering experiment.
3. `03_real_optical_flow_boundary_double_cover.ipynb`: the boundary bundle
   analysis, dependent on the output of notebook 02.

Do not treat output-free execution as sufficient validation. The numerical
targets in `../results/reference/expected_results.json` must also be checked.

