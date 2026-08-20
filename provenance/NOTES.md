# Legacy provenance notes

The archive contains multiple notebook generations: early monolithic notebooks,
private migration notebooks, stripped paper notebooks, checkpoints, and copies
inside an older Circle Bundles repository. The files listed in
`legacy_manifest.csv` are the minimal set needed to preserve the optical-flow
work's provenance.

The large executed notebooks were deliberately not copied into Git. Their
embedded outputs are valuable as historical validation evidence, but they are
too large and too dependent on obsolete notebook state to serve as public
sources. Their hashes allow the originals to be identified later.

Known migration issues include:

- The clean torus notebook uses demo-scale parameters rather than the full
  parameters stated in the manuscript.
- `build_bundle` and `circle_bundles.bundle` refer to obsolete package APIs.
- `plot_local_pca` is not present in the current public analysis module.
- `get_lifted_predom_dirs` was renamed to
  `get_lifted_predominant_dirs`.
- The torus notebook references an undefined `triv_result` for its
  low-directionality plot.
- The clustering notebook assumes particular component indices and uses
  randomized algorithms without recorded seeds.
- `HC20_Flow_patches.pkl` differs in capitalization from the recovered filename;
  this is significant on case-sensitive filesystems.
- The missing `K_50_60_Circles.pkl` save path was constructed without a path
  separator.

The modern Notebook 02 resolves the component-number dependency by locating the
two visually identified incomplete-circle pairs using their recorded
cardinalities. It uses the repository's canonical seed for the synthetic bridge
patches and writes a portable NPZ artifact. Reconstructing the old
doubled-angle Euclidean cover exactly eliminates the earlier 11-patch
discrepancy and recovers all 55,001 historical empirical memberships. Modern
Notebook 03 then constructs its 16-set lifted cover directly with the current
$S^1$ angular metric. It records the difference from the legacy chord-distance
parameterization, confirms the boundary bundle is orientable with zero Euler
class, and regenerates Figure 30.
