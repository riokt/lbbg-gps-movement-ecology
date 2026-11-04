# AGENTS.md

## Project purpose

Bird Migration Intelligence is a reproducible movement-ecology project using the Zenodo `LBBG_SCHIERMONNIKOOG` GPS telemetry dataset (`10.5281/zenodo.20706447`). The current public analysis snapshot is the 2017 GPS file for lesser black-backed gulls (*Larus fuscus*).

This is a research portfolio project, not a dashboard or prediction demo. Preserve scientific traceability, provenance, uncertainty, and limitations in every change.

## Environment and commands

- Use the repository `.venv`, created with Python 3.12.
- Use `uv` for dependency management; do not install ad hoc packages outside `pyproject.toml`.
- Set up or refresh the environment with `uv sync`.
- Run tests with `uv run pytest -q`.
- Run lint checks with `uv run ruff check src tests`.
- The Jupyter kernel is `bird-migration-intelligence`, displayed as `Bird Migration Intelligence (Python 3.12)`.
- Execute notebooks from the repository root with the project kernel. Notebook 02 is the preprocessing example:

  ```bash
  uv run jupyter nbconvert --to notebook --execute --inplace \
    notebooks/02_data_preprocessing.ipynb \
    --ExecutePreprocessor.timeout=600 \
    --ExecutePreprocessor.kernel_name=bird-migration-intelligence
  ```

- Notebook 03 is the current exploratory movement-analysis workflow:

  ```bash
  uv run jupyter nbconvert --to notebook --execute --inplace \
    notebooks/03_exploratory_movement_analysis.ipynb \
    --ExecutePreprocessor.timeout=600 \
    --ExecutePreprocessor.kernel_name=bird-migration-intelligence
  ```

Always verify that an executed notebook contains no error outputs and that its persisted artifacts can be reloaded.

## Data and provenance rules

- Use the existing local files under `data/raw/`; do not silently download another dataset or substitute observation-only data.
- Raw, interim, processed, and generated data are ignored by Git by default. The derived movement-step Parquet outputs are intentionally committed as reproducible analysis artifacts; raw telemetry and downloaded source files must remain ignored. Never commit credentials, access tokens, `.env` files, or private data.
- Preserve source columns and source values. Add canonical or derived fields rather than overwriting source fields.
- Record DOI, repository, licence, authors, file names, hashes where useful, units, coordinate reference system, timestamp convention, and transformations.
- Do not create a code licence that relicences third-party data. Dataset attribution and licence requirements must remain separate from the code licence.
- Treat `data/raw/LBBG_SCHIERMONNIKOOG-gps-2017.csv.gz` as GPS fixes, not movement steps. Do not derive movement distances, stopovers, local solar time, causal environmental effects, or regular sampling assumptions without explicit methodological support.

## Scientific constraints

- Do not silently delete outliers, flagged records, missing-speed records, missing-error records, or invalid rows. Validate first; document any exclusion explicitly.
- Repeated observations from the same individual are not independent. Use individual-aware summaries and validation, and consider random effects only when justified by the data and research question.
- Report effect sizes and uncertainty, not only p-values.
- Distinguish association from causation.
- Keep raw fixes, interpolated locations, and derived movement variables conceptually separate.
- Treat sampling frequency, missingness, sensor accuracy, and incomplete public study years as potential sources of bias.
- Fail loudly on critical validation failures such as unexpected row counts, duplicate event IDs, timestamp parse failures, missing individual identifiers, or out-of-range coordinates.

## Repository workflow

- Notebook order is sequential: `01_dataset_audit.ipynb`, `02_data_preprocessing.ipynb`, and `03_exploratory_movement_analysis.ipynb`. Do not proceed to later analysis notebooks until the selected data, preprocessing decisions, gap threshold, and exploratory scope have been reviewed.
- Put reusable logic in `src/bird_migration/`; keep notebooks readable and focused on orchestration, explanation, and displayed results.
- Save reproducible QC tables as CSV under `reports/` and figures under `reports/figures/`.
- Movement steps must use WGS84 geodesic distance, remain within individual, and preserve long-gap exclusions in a separate dataset. Average displacement speed is not instantaneous flight speed.
- Do not modify earlier notebooks unless the user explicitly requests it; preserve executed outputs when they document the completed workflow.
- Before handing off a change, run the relevant notebook, tests, and lint checks, inspect `git diff --check`, and report generated files and validation results.
- Do not commit or push unless the user explicitly asks for it. Use Conventional Commit messages when asked to commit, such as `feat(preprocessing): add GPS preprocessing workflow` or `fix(audit): correct timestamp validation`.
