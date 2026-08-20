# Manuscript figure inventory

This inventory was prepared from the figure environments in the submitted
`main.tex`. The manuscript currently contains 31 figure environments and 43
included image files. The number in the first column is the order in which the
figure appears in `main.tex`; the LaTeX label is the durable identifier.

The goal is to reproduce every data-dependent figure that supports a scientific
claim. Conceptual diagrams should have their source preserved and should be
regenerated only when that is useful. A reproduced computation need not be
pixel-identical to the old PDF, but it should use the same data, parameters and
mathematical procedure.

## Status key

- **Reproduced:** the current notebook executes and reproduces the underlying
  result; a stable paper filename/export may still be added.
- **Partial:** the current workflow reproduces part of the result, but a panel,
  comparison or paper-specific visualization remains.
- **Legacy source:** relevant source code has been identified in a preserved
  notebook, but it is not yet a clean public workflow.
- **Preserve:** primarily a conceptual, contextual or manually assembled asset;
  retaining the source/final asset may be sufficient.
- **Pending:** a specific generating cell has not yet been confirmed.

## Figure-to-workflow map

| No. | LaTeX label | Included image file(s) | Kind | Proposed owner | Status and next action |
|---:|---|---|---|---|---|
| 1 | `fig: FramesSintel` | `KEEPER_A.pdf`, `KEEPER_C.pdf` | Contextual data | Notebook 00 | **Partial.** Notebook 00 now renders a reproducible frame/flow overlay when raw Sintel is available. The exact scene/frame choices used for `KEEPER_A.pdf` and `KEEPER_C.pdf` still need to be identified. |
| 2 | `Range_Step_Annulus` | `Binary_Step_Edge_Range_AnnulusB.pdf` | Conceptual model | Model figures | **Legacy source.** The step-edge notebook contains the annulus construction. |
| 3 | `Range_DCT` | `Scalar_DCT.pdf` | Analytic basis | Model figures | **Pending.** The basis is deterministic, but the exact plotting cell has not yet been matched to a preserved public source. |
| 4 | `Flow_DCT` | `DCT_flow_patches_labeled.pdf` | Analytic basis | Model figures | **Pending.** The optical-flow DCT utilities are present in the old Circle Bundles material; add a self-contained plotting cell. |
| 5 | `Optical_Flow_Torus` | `Model_Patch_Diagram.pdf` | Conceptual model | Model figures | **Legacy source.** The step-edge/model and synthetic optical-flow notebooks contain the torus sampling and patch-lattice construction. |
| 6 | `Global_Ripsers` | `Global_Ripsers.pdf` | Data and simulation | Notebook 01 | **Reproduced in substance.** Notebook 01 now reconstructs the complete six-panel comparison. The $X(1500,50)$ and $X(1500,30)$ diagrams match the submitted diagram counts exactly. The synthetic panels use a new documented seed and the current contrast-renormalized noise convention because the historical seed and final normalization step were not recorded. |
| 7 | `sample_predom_dirs` | `Real_Opt_Flow_Sample.pdf` | Data | Notebook 01 | **Reproduced.** Notebook 01 displays patches arranged and labeled by predominant direction; add the publication export name and fixed visual sampling. |
| 8 | `Adams_fiber_projections` | `Adams_Projections_fibers.pdf` | Data | Notebook 01 | **Legacy source.** The manuscript uses specified DCT-plane projections, whereas Notebook 01 currently shows local PCA. Recover the DCT projection cell rather than treating those plots as identical. |
| 9 | `Weak_Predom_Dir_Samples` | `Real_Opt_Flow_Sample_No_Dirs_A.pdf`, `Real_Opt_Flow_Sample_No_Dirs_B.pdf` | Data | Sintel diagnostics / Notebook 01 | **Partial.** Notebook 01 computes directionality; the two paper-specific low-directionality sample panels still need deterministic selection and export. |
| 10 | `Distributions_Of_Directionality` | `directionality_distribution.pdf` | Data | Notebook 00 | **Reproduced.** Notebook 00 recomputes full $X$, $X(1500,30)$, $X(1500,50)$ and $X(50,60)$ from the portable artifact and recreates the submitted four-curve comparison under the stable paper filename. |
| 11 | `Antipatches` | `sample_patches_anti_patches.pdf` | Conceptual model | Model figures | **Legacy source.** Rebuild from the deterministic model-patch functions. |
| 12 | `Decreasing_Directionality` | `Varying_DirectionalityC.pdf`, `Varying_Directionality.pdf` | Conceptual model | Model figures | **Legacy source.** Regenerate the two fixed-parameter model paths as one paper composite. |
| 13 | `Circle_Of_Low_Directionality` | `Circle_Of_Low_Directionality.pdf` | Conceptual model | Model figures | **Legacy source.** Regenerate from the limiting model circle. |
| 14 | `Nerve_With_Cochains` | `Real_Opt_Flow_Triv_Correlations.pdf`, `Real_Oft_Nerve.pdf` | Data / bundle result | Notebook 01 | **Partial.** Notebook 01 computes the local trivializations and characteristic classes, but the exact correlation and labeled-nerve panels are not yet exported. |
| 15 | `Recovered_Patch_Diagrams` | `opt_flow_torus.pdf` | Data / bundle result | Notebook 01 | **Reproduced.** The publication profile recovers the high-directionality lattice and expected counts. Add stable selection and the paper export name. |
| 16 | `low_directionality_recovered_patches` | `opt_flow_torus_low.pdf` | Data / bundle result | Notebook 01 | **Reproduced.** The publication profile recovers the low-directionality lattice and expected counts. Add stable selection and the paper export name. |
| 17 | `Combined_Sample_Figure` | `Sample_Projections.pdf`, `Sample_Projections_rips.pdf` | Data | Notebook 02 | **Reproduced.** Notebook 02 regenerates the three local PCA projections and matching per-fiber persistence diagrams. |
| 18 | `Summary_Part1` | `Sample_Clustered_Fibers_summary.pdf` | Data / clustering | Notebook 02 | **Reproduced.** The three-panel clustering summary and all saved counts match the executed legacy run. |
| 19 | `Sample_Clustered_Fibers` | `Sample_Clustered_Fibers.pdf` | Data / clustering | Notebook 02 | **Reproduced.** The three selected fibers are displayed with their DBSCAN labels under the stable paper filename. |
| 20 | `Binary_Patch_Sample` | `Binary_Range_Patch_Sample.pdf`, `Binary_Flow_Patch_SampleA.pdf`, `Binary_Flow_Patch_SampleB.pdf` | Model/data comparison | Notebook 02 | **Reproduced.** The ten recorded binary pattern indices and the fixed $\pi/6$ flow direction regenerate all three panels. |
| 21 | `Double_Cover_Patches` | `G_component_vis.pdf` | Data / graph | Notebook 02 | **Reproduced.** Notebook 02 rebuilds the representative-patch diagram for the recorded double-cover component. |
| 22 | `Sample_CCs` | `Sample_ccs_w_Corrs.pdf` | Data / circular coordinates | Notebook 02 | **Reproduced.** Components 9, 11 and 15 are coordinatized and compared with predominant direction. Circular-coordinate gauge choices can rotate or reflect the displayed parametrizations. |
| 23 | `Cluster_Persistence` | `Cluster_Persistence.pdf` | Data / persistence | Notebook 02 | **Reproduced.** Notebook 02 reconstructs the graph-weight filtration and stable publication export. |
| 24 | `Summary_Part2` | `Point_Count.pdf`, `Cluster_Count.pdf`, `Optical_Flow_Paper_DiagramsLargest_Cluster_Graph_Vis2.pdf` | Data / graph summary | Notebook 02 | **Reproduced.** The filtered cluster counts, point counts and colored $G_0$ graph are rebuilt from the modern component memberships. |
| 25 | `Missing_Circles` | `composite_circles_ripser.pdf`, `Missing_Circles_cc.pdf` | Data / persistence | Notebook 02 | **Reproduced.** The two component pairs are found by their recorded cardinalities, their persistence is recomputed, and deterministic bridge samples support the circular-coordinate panels. |
| 26 | `fig:Quadratic_Patches` | `Quadratic_Patches.pdf` | Model/data interpretation | Notebook 02 | **Reproduced.** One deterministic representative from each residual component recreates the outlier/quadratic-patch panel. |
| 27 | `fig:HC1_Sample_Projections` | `HC_Fiber_Projections.png` | Data | Sintel diagnostics | **Legacy source.** Rebuild the top-one-percent contrast sample and its fiber projections from the recovered preprocessing artifact. |
| 28 | `Labeled_Frames` | `Labeled_FrameD.png`, `Labeled_FrameB.png`, `Labeled_FrameE.png` | Contextual data | Sintel diagnostics | **Legacy source.** The frame-labeling functions and contrast thresholds are present; make the frame choices explicit and deterministic. |
| 29 | `Optical_Flow_Annulus` | `Binary_Step_Edge_Opt_Flow_AnnulusB.pdf` | Conceptual model | Model figures | **Legacy source.** The recovered step-edge checkpoint contains the optical-flow annulus export. |
| 30 | `Boundary_Torus` | `boundary_torus.pdf` | Data / bundle result | Notebook 03 | **Legacy source.** The input artifact is now portable, but Notebook 03 still needs current-API modernization and end-to-end validation. |
| 31 | `All_Binary_Range_Patches` | `All_Binary_Step_Range_Patches.pdf` | Appendix model catalog | Model figures | **Legacy source.** The step-edge notebook deterministically constructs all 56 patches. |

## Recommended public workflows

The 31 manuscript figures do not require 31 notebooks. They group naturally as
follows:

1. **Sintel data diagnostics (Notebook 00):** figures 1, 9, 10, 27 and 28.
2. **Extended optical-flow torus (Notebook 01):** figures 6--8 and 14--16.
3. **Fiberwise clustering (Notebook 02):** figures 17--26, with model helpers
   used for figures 20 and 26.
4. **Boundary double cover (Notebook 03):** figure 30.
5. **Deterministic model figures:** figures 2--5, 11--13, 20, 26, 29 and 31.

Notebook 00 now completes figure 10 and supplies the reusable raw-frame overlay
needed to identify figure 1. Notebook 02 reproduces figures 17--26 and records
every stable output filename in its run record. The next useful pass is to
recover the exact scene/frame selections for figures 1 and 28, or to continue
with the missing Notebook 01 panels 8 and 14.
