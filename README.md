# Bird Migration Intelligence

Milestone 01 audits the Zenodo dataset **LBBG_SCHIERMONNIKOOG**: GPS tracking of lesser black-backed gulls (*Larus fuscus*) breeding on Schiermonnikoog, the Netherlands.

## Dataset decision

The American Robin Dryad record was rejected for this run because its public metadata and landing page were accessible, but its individual-file and API download routes returned HTTP 403/401 from the execution environment. The Zenodo fallback has directly downloadable files, a Frictionless `datapackage.json`, an open CC0 licence, and a relevant GPS file.

Selected record: [Zenodo 10.5281/zenodo.20706447](https://doi.org/10.5281/zenodo.20706447). The record contains GPS and acceleration files for a study active from 2017–2022; its metadata states that data collected since 2021 are not publicly available. This audit uses the documentation, reference data, and the 2017 GPS file only.

## Reproduce the audit

```bash
uv sync
uv run python -m bird_migration.audit
uv run pytest
```

The audit writes `reports/dataset_audit.json`, `reports/data_dictionary.csv`, and a short decision note. Raw files are downloaded locally and ignored by Git. See [data/README.md](data/README.md) for provenance and download instructions.

Modeling is intentionally deferred until the dataset and research scope have been reviewed.
