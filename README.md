# Bird Migration Intelligence

Reproducible GPS telemetry and movement-ecology analysis of lesser black-backed gulls (*Larus fuscus*) from the `LBBG_SCHIERMONNIKOOG` study.

## Research question

How do GPS-derived location and movement patterns vary by time of day and individual in the publicly available 2017 sample?

This project focuses on data provenance, GPS quality assessment, irregular sampling, geodesic movement-step derivation, temporal exploration, and individual variation. It is an exploratory research workflow—not a dashboard or machine-learning demonstration.

## Dataset

- **Repository:** Zenodo
- **Record:** [10.5281/zenodo.20706447](https://doi.org/10.5281/zenodo.20706447)
- **Species:** Lesser black-backed gull (*Larus fuscus*)
- **Study:** `LBBG_SCHIERMONNIKOOG`
- **Licence:** CC0
- **Public analysis snapshot:** 2017 GPS telemetry
- **Coverage:** 441,979 GPS fixes from 20 individuals

The repository does not commit raw telemetry. Download instructions, provenance, licence information, and expected local filenames are documented in [data/README.md](data/README.md). The derived movement-step Parquet outputs are committed as reproducible analysis artifacts.

## Reproduce the analysis

The project uses Python 3.12, `uv`, and the VS Code/Jupyter kernel `Bird Migration Intelligence (Python 3.12)`.

```bash
uv sync
uv run pytest -q
uv run ruff check src tests
```

Execute the notebooks from the repository root:

```bash
uv run jupyter nbconvert --to notebook --execute --inplace \
  notebooks/01_dataset_audit.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=bird-migration-intelligence

uv run jupyter nbconvert --to notebook --execute --inplace \
  notebooks/02_data_preprocessing.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=bird-migration-intelligence

uv run jupyter nbconvert --to notebook --execute --inplace \
  notebooks/03_exploratory_movement_analysis.ipynb \
  --ExecutePreprocessor.timeout=600 \
  --ExecutePreprocessor.kernel_name=bird-migration-intelligence
```

## Completed workflow

1. **Notebook 01 — Dataset audit**
   - Verified schema, provenance, missingness, coordinates, timestamps, duplicates, and individual coverage.
2. **Notebook 02 — Data preprocessing**
   - Preserved all source columns and rows.
   - Added canonical fields and UTC temporal fields.
   - Exported the validated Parquet dataset.
3. **Notebook 03 — Exploratory movement analysis**
   - Quantified irregular GPS sampling.
   - Derived WGS84 geodesic steps between consecutive fixes within individuals.
   - Excluded long-gap pairs from the primary step table while preserving them separately.
   - Compared derived average displacement speed with source ground-speed values.
   - Produced individual, hourly, daily, monthly, and quality-control summaries.

Notebook 04 modeling has not been started. Later statistical analysis should account for repeated observations within individuals.

## Key exploratory results

- Median positive sampling interval: **592 seconds**.
- Selected continuity threshold: **1 hour**.
- Retained movement steps: **441,814**.
- Long-gap pairs excluded from primary steps: **145**.
- Terminal fixes without a following fix: **20**.
- Median retained geodesic step distance: **11.4 m**.
- Median derived average displacement speed: **0.023 m/s**.
- Individual median step distances ranged from approximately **6.0 m to 20.1 m**.

These are descriptive results only. UTC hour is not local solar time, average displacement speed is not instantaneous flight speed, and summed step distance reflects both movement and observation coverage.

## Main outputs

- [Dataset audit notebook](notebooks/01_dataset_audit.ipynb)
- [Preprocessing notebook](notebooks/02_data_preprocessing.ipynb)
- [Exploratory movement notebook](notebooks/03_exploratory_movement_analysis.ipynb)
- [Preprocessed GPS fixes](data/processed/lbbg_gps_fixes_preprocessed.parquet)
- [Retained movement steps](data/interim/lbbg_movement_steps.parquet)
- [Excluded movement-step candidates](data/interim/lbbg_movement_steps_excluded.parquet)
- [Movement summary by individual](reports/movement_summary_by_individual.csv)
- [Sampling interval summary](reports/sampling_interval_summary.csv)
- [Movement quality report](reports/movement_quality_report.csv)
- [Gap-threshold sensitivity](reports/sampling_gap_threshold_sensitivity.csv)
- [Research interpretation](reports/movement_interpretation.txt)
- [Figures](reports/figures/)

## Scientific safeguards

- Raw GPS fixes are not treated as movement steps.
- Movement distances use WGS84 geodesic calculations, not Euclidean latitude/longitude degrees.
- Steps never cross individual boundaries.
- Long tracking gaps, source flags, and missing values are retained and documented.
- Unusual movements are review flags, not automatic deletions.
- Repeated observations within individuals are not independent samples.
- No stopover, causal environmental, or local day/night claims are made from this exploratory workflow.

## Citation

Shamoun-Baranes, J., Sage, E., Shinneman, S., Govaert, S., Desmet, P., & Camphuysen, K. C. J. (2026). *LBBG_SCHIERMONNIKOOG - Lesser black-backed gulls (Larus fuscus, Laridae) breeding in Schiermonnikoog (the Netherlands)*. Zenodo. [https://doi.org/10.5281/zenodo.20706447](https://doi.org/10.5281/zenodo.20706447)
