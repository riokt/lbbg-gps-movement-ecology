# Data access

## Selected dataset

- **Record:** LBBG_SCHIERMONNIKOOG — Lesser black-backed gulls (*Larus fuscus*) breeding in Schiermonnikoog, the Netherlands
- **Repository:** Zenodo
- **DOI:** [10.5281/zenodo.20706447](https://doi.org/10.5281/zenodo.20706447)
- **Licence:** CC0
- **Authors:** Judy Shamoun-Baranes, Elspeth Sage, Stacy Shinneman, Sanne Govaert, Peter Desmet, Kees C.J. Camphuysen
- **Source metadata:** `https://zenodo.org/api/records/20706447`
- **Study:** Movebank study 8872901376; the Zenodo record says data collected since 2021 are not public.

The local audit snapshot contains `datapackage.json`, `LBBG_SCHIERMONNIKOOG-reference-data.csv`, and `LBBG_SCHIERMONNIKOOG-gps-2017.csv.gz`. The larger annual GPS and acceleration files are available from the record but were not downloaded for this milestone.

Download the snapshot with:

```bash
curl -L --fail 'https://zenodo.org/api/records/20706447/files/datapackage.json/content' -o data/raw/datapackage.json
curl -L --fail 'https://zenodo.org/api/records/20706447/files/LBBG_SCHIERMONNIKOOG-reference-data.csv/content' -o data/raw/LBBG_SCHIERMONNIKOOG-reference-data.csv
curl -L --fail 'https://zenodo.org/api/records/20706447/files/LBBG_SCHIERMONNIKOOG-gps-2017.csv.gz/content' -o data/raw/LBBG_SCHIERMONNIKOOG-gps-2017.csv.gz
```

The GPS records use UTC/GPS time and WGS84 decimal-degree coordinates, as documented in `datapackage.json`. Preserve the source columns; standardized names are documented in `reports/data_dictionary.csv`.
