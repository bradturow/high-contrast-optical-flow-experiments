# Local data

No dataset is committed to this repository.

The legacy experiments used three local inputs or intermediates:

| Artifact | Historical role | SHA-256 |
| --- | --- | --- |
| MPI-Sintel complete dataset | Original flow frames | Directory; see inventory below |
| `HC20_Flow_Patches.pkl` | 250,000 preprocessed top-20%-contrast patches and density columns | `40a8a1f9674e157ae3bbbc30385572a3ffb879a60264de82c463d97308772535` |
| `optical_flow_sample_4000_pf.pickle` | Raw 4,000-patches-per-frame sample | `08189371948199553336ecabacf7f77bc343211ec814d520f6b82062d8220aa1` |

The recovered MPI-Sintel directory contains 8,559 files (5.8 GB), including
1,041 `.flo` files under `training/flow`.

The downstream `K_50_60_Circles.pkl` artifact referenced by the boundary
notebook was not recovered. Historical code attempted to save it using a path
concatenation with a missing separator. The modern fiberwise-clustering pipeline
now regenerates it as `K_50_60_Circles.v1.npz`, which loads with
`allow_pickle=False` and records its construction metadata.

The verified local artifact was 7,526,862 bytes with SHA-256
`990c7ef1e3274981509ed28ebf0b6359477a13603586054aa68178ca95e31f02`.
It contains 55,012 empirical patches, 500 deterministic synthetic bridge
patches, and a mutually exclusive `(28, 55512)` circle-membership matrix. The
historical notebook recorded 55,001 empirical patches; see the reference
results for this 11-patch dependency-sensitive difference.

The migration code can convert the trusted HC20 pickle to a compressed NPZ
artifact whose arrays load with `allow_pickle=False`:

```bash
python scripts/convert_legacy_pickle.py \
  /path/to/HC20_Flow_Patches.pkl \
  data/HC20_Flow_Patches.v1.npz
```

The locally converted artifact was 51,066,528 bytes with SHA-256
`f893aa57ace9aa29ea53a54f8ecf41ba9aa81530fe9aea64edf564d3be1a8b0a`.
Every patch and scalar column was verified equal to the recovered pickle.

Until redistribution permissions are reviewed, keep the original Sintel data
and derived pickle artifacts local. The migrated code should accept paths via
command-line arguments or environment variables rather than absolute paths.

To verify local artifacts without unpickling them:

```bash
python scripts/verify_local_data.py \
  --hc20 /path/to/HC20_Flow_Patches.pkl \
  --raw-sample /path/to/optical_flow_sample_4000_pf.pickle \
  --sintel-root /path/to/MPI-Sintel-complete
```
