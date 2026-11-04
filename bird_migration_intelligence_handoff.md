# Bird Migration Intelligence

## Research Project Handoff for a Coding Agent

**Status:** Project planning and dataset verification\
**Primary goal:** Build a reproducible, research-oriented GitHub
portfolio project using real bird-movement data.\
**Working research theme:** Circadian patterns and individual variation
in migratory bird movement.

------------------------------------------------------------------------

## 1. Project objective

Develop a scientifically defensible, reproducible analysis of bird
migration and movement ecology. The project should demonstrate:

-   Data acquisition and provenance management
-   Data auditing and quality assessment
-   Temporal and geospatial analysis
-   Statistical inference with appropriate treatment of repeated
    observations
-   Clear, reproducible visualizations
-   Well-documented limitations and uncertainty

This is an academic/research portfolio, not merely a dashboard or a
machine-learning demo. Do not add machine learning unless it addresses a
clear research question and can be evaluated without data leakage.

## 2. Dataset-selection history and current decision

### Important lesson from Movebank

Three candidate studies were previously attempted through Movebank, but
the user received **"no data available"** when trying to access the
records. The candidates were:

1.  Red Phalarope
2.  American Woodcock
3.  Blackpoll Warbler

Do not assume that a study catalogue page means its event-level tracking
data are publicly downloadable. Do not build the project around a
Movebank study until actual record-level access has been verified.

### New candidate datasets

The previous discussion identified these alternative repository records.
Treat them as **candidates to verify**, not as independently re-verified
guarantees of access.

#### Candidate A --- American Robin

-   Species: *Turdus migratorius*
-   Repository: Dryad
-   DOI: `10.5061/dryad.pzgmsbd3m`
-   Landing page: https://doi.org/10.5061/dryad.pzgmsbd3m
-   Previously described as a relatively small CSV dataset of processed
    movement steps for 19 GPS-tracked birds, with timestamps, locations,
    movement distances/durations, and day/night classifications.

**Potential research focus:** Circadian patterns in movement, temporal
variation in movement distance, and differences among individuals.

**Important qualification:** The data were described as processed
movement steps, not necessarily raw GPS fixes. Inspect the README and
data dictionary before deciding which analyses are valid. Do not infer
undocumented columns or measurement methods.

#### Candidate B --- Lesser Black-backed Gull

-   Species: *Larus fuscus*
-   Repository: Zenodo
-   DOI: `10.5281/zenodo.20706447`
-   Landing page: https://doi.org/10.5281/zenodo.20706447
-   Previously described as containing GPS files for 29 birds across
    four annual files, plus animal/deployment reference data and
    acceleration data.

**Potential research focus:** Migration routes, seasonal movement,
habitat use, and individual variation.

**Important qualification:** Inspect the actual record, file list,
metadata, licence, and data dictionary. Check file sizes and whether all
files are downloadable. The prior discussion noted that data collected
since 2021 may not be public; verify this from the repository metadata
rather than assuming it.

### Dataset-selection rule

Before committing to either dataset, verify all of the following:

1.  The landing page resolves and identifies the expected study.
2.  The record contains actual downloadable data files, not only an
    abstract or summary.
3.  At least one relevant data file can be downloaded and opened.
4.  The README/data dictionary explains the fields, units, timestamps,
    coordinate reference system, and sampling process.
5.  The licence permits the intended analysis and public description of
    the data.
6.  The study publication and required citation can be identified.
7.  The data are sufficiently suitable for the chosen research question.

If Candidate A fails these checks, evaluate Candidate B. If both fail,
search for another openly downloadable tracking dataset from Dryad,
Zenodo, Movebank Data Repository, or another trusted research
repository. Do not silently substitute observation-only occurrence data
for individual tracking data.

------------------------------------------------------------------------

## 3. Research direction

### Provisional title

**Investigating Circadian Patterns in Migratory Bird Movement Using
Tracking Data**

The title and questions must be revised after inspecting the selected
dataset. In particular, do not call a dataset "GPS tracking" unless its
metadata confirms GPS-derived locations.

### Provisional research questions

1.  How does movement distance or activity vary across time of day?
2.  Does movement behavior vary across migration periods or seasons?
3.  How much variation exists between individual birds?
4.  Are temporal patterns consistent across individuals?

These questions are provisional. Only retain questions supported by the
available variables and study design.

### Potential hypotheses

-   H1: Movement metrics differ between day and night.
-   H2: Movement metrics vary across the migration period.
-   H3: There is meaningful between-individual variation in movement
    behavior.

Do not assume the direction of an effect before examining the relevant
literature and dataset.

### Statistical considerations

-   Repeated observations from the same bird are not independent.
-   Consider mixed-effects models with individual as a random effect
    when the data structure and sample size support them.
-   Inspect distributions and residual assumptions before selecting a
    model.
-   Report effect sizes and uncertainty intervals, not only p-values.
-   Distinguish association from causation.
-   Avoid treating processed movement-step records as independent raw
    location fixes.
-   Do not infer stopover behavior unless the temporal/spatial
    resolution and movement variables support a defensible stopover
    definition.

------------------------------------------------------------------------

## 4. Proposed technical stack

Use Python and a reproducible environment. The exact dependency versions
should be pinned or locked by the package manager.

Suggested tools:

-   Python 3.11 or 3.12
-   `uv` for environment and dependency management
-   `pandas`, `numpy`, `scipy`
-   `geopandas`, `shapely`, `pyproj`
-   `statsmodels`
-   `scikit-learn` only where justified
-   `matplotlib`, `seaborn`, `plotly`
-   `jupyterlab`
-   `pytest`, `ruff`

Do not add large frameworks or a dashboard until the research analysis
is complete.

------------------------------------------------------------------------

## 5. Repository structure

Suggested structure:

``` text
bird-migration-intelligence/
├── data/
│   ├── raw/
│   ├── interim/
│   ├── processed/
│   └── README.md
├── notebooks/
│   ├── 01_dataset_audit.ipynb
│   ├── 02_data_preprocessing.ipynb
│   ├── 03_exploratory_movement_analysis.ipynb
│   ├── 04_statistical_analysis.ipynb
│   └── 05_geospatial_visualization.ipynb
├── src/
│   └── bird_migration/
│       ├── __init__.py
│       ├── ingestion.py
│       ├── preprocessing.py
│       ├── movement.py
│       ├── statistics.py
│       └── visualization.py
├── tests/
├── reports/
│   └── figures/
├── pyproject.toml
├── README.md
├── CITATION.cff
├── .gitignore
└── LICENSE
```

Adjust this structure to the actual data and scope. Avoid creating empty
modules that are not used.

### Data handling and Git policy

-   Do not commit raw tracking data unless its licence explicitly
    permits redistribution.
-   Keep downloaded data outside Git or ignored by `.gitignore` by
    default.
-   Include instructions in `data/README.md` explaining where the data
    come from, how to obtain them, the DOI, licence, and expected
    filenames.
-   Never commit credentials, access tokens, private data, or `.env`
    files.
-   Do not add a repository `LICENSE` that purports to relicense
    third-party data. The code licence and dataset licence are separate.
-   Include attribution and the required citation for the original data
    authors.

------------------------------------------------------------------------

## 6. Initial setup commands

From a terminal:

``` bash
mkdir bird-migration-intelligence
cd bird-migration-intelligence

git init
uv init --package bird-migration-intelligence

uv add pandas numpy scipy
uv add geopandas shapely pyproj
uv add statsmodels
uv add matplotlib seaborn plotly jupyterlab

uv add --dev pytest ruff pre-commit

mkdir -p data/raw data/interim data/processed
mkdir -p notebooks reports/figures tests

touch data/README.md
```

Add a `.gitignore` similar to:

``` gitignore
# Downloaded and generated data
data/raw/*
data/interim/*
data/processed/*
!data/raw/.gitkeep
!data/interim/.gitkeep
!data/processed/.gitkeep
!data/README.md

# Python
__pycache__/
*.py[cod]
.venv/
.ipynb_checkpoints/
.pytest_cache/
.ruff_cache/

# Secrets and local configuration
.env
.env.*
!.env.example

# OS/editor
.DS_Store
.vscode/
.idea/
```

Create `.gitkeep` files if the empty data directories need to be
tracked.

------------------------------------------------------------------------

## 7. First implementation milestone: dataset audit

Do not start with prediction or a dashboard. First obtain the dataset
and create `notebooks/01_dataset_audit.ipynb`.

The notebook should:

1.  Record the dataset name, DOI, repository URL, download date,
    licence, authors, and publication citation.
2.  List the downloaded files and their sizes.
3.  Read the README and data dictionary.
4.  Load the data without silently changing source values.
5.  Display row/column counts, column names, data types, and
    representative records.
6.  Identify the individual identifier, timestamp, coordinate fields,
    movement variables, and sensor/method fields where available.
7.  Check missingness, duplicates, invalid coordinates, timestamp
    parsing, and impossible values.
8.  Summarize observations per individual and temporal coverage.
9.  Plot the spatial extent and temporal coverage, if the data support
    those plots.
10. Write a concise audit report describing data quality, limitations,
    and whether the research questions are feasible.

### Expected outputs

-   A completed `01_dataset_audit.ipynb`
-   A machine-readable data audit summary, if useful
-   A data dictionary mapping original column names to standardized
    names
-   A short decision note: proceed, change research question, or reject
    dataset

### Standardized internal field names

Only map fields that actually exist. Possible names include:

  Standardized field   Meaning
  -------------------- ------------------------------------------------
  `individual_id`      Unique tracked animal
  `timestamp`          Observation or movement-step time
  `latitude`           Latitude in decimal degrees
  `longitude`          Longitude in decimal degrees
  `sensor_type`        GPS, Argos, geolocator, or other method
  `location_error`     Location uncertainty, if supplied
  `distance_m`         Movement distance in metres, if supplied
  `duration_s`         Movement-step duration in seconds, if supplied
  `study_id`           Original study identifier

Preserve the original columns and values. Create standardized columns in
a separate processing step and document every mapping.

------------------------------------------------------------------------

## 8. Quality and scientific standards

The coding agent must follow these rules:

-   Never fabricate data, columns, metadata, citations, or study
    details.
-   Never assume a repository's data are downloadable without checking
    the files.
-   Never silently delete outliers or anomalous observations.
-   Preserve source data and create separate processed outputs.
-   Document coordinate systems, timestamp time zones, units, and sensor
    accuracy.
-   Distinguish raw fixes, interpolated locations, and derived movement
    steps.
-   Treat tracking frequency and missingness as potential sources of
    bias.
-   Use individual-level or otherwise scientifically appropriate
    validation to avoid leakage.
-   Include uncertainty and limitations in figures and written
    interpretation.
-   Do not claim environmental effects or causal relationships from
    observational correlations alone.
-   Keep code modular, tested, documented, and reproducible.

------------------------------------------------------------------------

## 9. Immediate tasks for the coding agent

Work in this order:

1.  Verify the Dryad American Robin DOI and inspect its record metadata
    and file list.
2.  Verify the Zenodo Lesser Black-backed Gull DOI and inspect its
    record metadata and file list.
3.  Determine which candidate has accessible, relevant data and a
    suitable licence.
4.  Download only the selected dataset and its documentation, respecting
    repository terms.
5.  Inspect the real files and create a data dictionary.
6.  Initialize the repository and environment.
7.  Implement the dataset-audit notebook.
8.  Report findings and recommend a final, dataset-supported research
    question.

**Do not proceed to modeling until the dataset audit is complete and the
user has reviewed the selected dataset and research scope.**

------------------------------------------------------------------------

## 10. Definition of done for Milestone 01

Milestone 01 is complete when:

-   [ ] A real dataset has been downloaded successfully.
-   [ ] The DOI, authors, source, licence, and citation are recorded.
-   [ ] The README/data dictionary has been reviewed.
-   [ ] The data can be loaded reproducibly.
-   [ ] The schema and data quality have been audited.
-   [ ] The feasibility of the research questions has been assessed.
-   [ ] The repository setup and data-access instructions are
    documented.

**Current project status:** Dataset selection is not yet finalized. The
American Robin Dryad record is the first candidate to verify; the Lesser
Black-backed Gull Zenodo record is the fallback. The previous Movebank
attempts did not provide accessible event-level data.
