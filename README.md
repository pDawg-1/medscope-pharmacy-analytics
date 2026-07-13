# MedScope - Prescription Cost & Pharmacy Analytics Dashboard

MedScope is an end-to-end healthcare analytics project built to analyze prescription volume, drug spending, insurance coverage, patient out-of-pocket cost, and doctor prescribing patterns. The project uses Snowflake as the data warehouse, SQL for cleaning and analytics views, and Power BI for dashboard reporting.

## Project Objective

Healthcare and pharmacy teams need a clear way to monitor prescription costs, identify high-cost drugs, understand insurance coverage, and review provider prescribing patterns. This dashboard helps users quickly answer business questions such as:

* What is the total prescription cost?
* Which drugs are driving the highest spending?
* How much is covered by insurance versus paid out of pocket?
* Which doctors are prescribing the most?
* How are prescriptions trending month by month?
* Can users look up patient-level prescription details?

## Tech Stack

* Snowflake
* SQL
* Power BI
* Data Modeling
* DAX
* Python and pandas
* Synthetic Excel/CSV dataset

## Data Source and Privacy

MedScope uses a synthetic pharmacy dataset supplied with the project. All patient, doctor, prescription, pharmacy, drug, and insurance-claim records are fictional; the project does not contain real protected health information.

The original data-generation process is not part of this repository. The included files are treated as source-system extracts so the project can demonstrate cleaning, validation, warehouse modeling, reporting, and conversational analytics without exposing sensitive healthcare information.

## Data Pipeline

The project follows this flow:

```text
Synthetic CSV files -> Snowflake RAW tables -> Snowflake CLEAN tables -> Analytics views -> Power BI and Flask chatbot
```

## Snowflake Design

The Snowflake layer is organized into three main layers:

### RAW Layer

Stores the original uploaded pharmacy, patient, doctor, drug, prescription, and insurance claim data.

### CLEAN Layer

Creates deduplicated and validated tables from the raw data to prevent duplicate loads and improve reporting reliability.

### ANALYTICS Layer

Creates reporting-ready views that are connected directly to Power BI.

## Build Order

1. Run `sql/01_create_tables.sql` in Snowflake.
2. Upload the six files from `data/raw/` to `@MEDSCOPE_DB.RAW.MEDSCOPE_CSV_STAGE`.
3. Run `sql/01_load_raw_data.sql` to load the staged files.
4. Run `sql/02_clean_layer.sql` to create the deduplicated clean tables.
5. Run `sql/03_analytics_views.sql` to create reporting views.
6. Run `sql/04_validation_queries.sql` and `python/data_quality_checks.py`.
7. Refresh the Power BI model and verify its slicers and totals.

## Dashboard Pages

### 1. Executive Overview

Shows total prescriptions, total drug cost, average prescription cost, total patients, total doctors, most prescribed drug, monthly prescription trend, and drug cost by category.

### 2. Drug Cost Analysis

Analyzes top drugs by total cost, average prescription cost by drug category, insurance covered versus patient out-of-pocket cost, and high-cost prescription records.

### 3. Patient Prescription Lookup

Allows users to filter by pharmacy, drug, and patient to view detailed prescription records, diagnosis, doctor, specialty, insurance covered, and out-of-pocket cost.

### 4. Doctor Prescriber Analysis

Shows top prescribing doctors, prescriptions by specialty, average prescription cost by doctor, unique patients treated, and doctor-level prescription summaries.

### 5. Natural Language Q&A

Demonstrates Power BI Q&A for supported business questions. Microsoft has announced retirement of this visual in December 2026; the Flask chatbot in `chatbot/` is the project's longer-term conversational interface.

## Key Features

* Built a Snowflake warehouse with raw, clean, and analytics layers.
* Removed duplicate records and standardized business fields using SQL clean tables.
* Added Python cleaning and data-quality checks for keys, nulls, relationships, and cost logic.
* Standardized diagnosis values for cleaner reporting.
* Created Snowflake views for executive KPIs, drug cost analysis, patient lookup, doctor analysis, and monthly prescription trends.
* Connected Snowflake analytics views to Power BI.
* Built an interactive dashboard with slicers, KPI cards, trend charts, lookup tables, and detailed prescription summaries.
* Validated row counts and joins before using the data in Power BI.

## Project Files

```text
data/              Dataset files
sql/               Snowflake SQL scripts
Dashboard files/   Power BI dashboard file and exported PDF
docs/              Notes and documentation
python/            Helper scripts if needed
```

## SQL Scripts

```text
01_create_tables.sql       Creates database, schemas, and raw tables
01_load_raw_data.sql       Loads staged CSV files into raw tables
02_clean_layer.sql         Creates clean deduplicated tables
03_analytics_views.sql     Creates Power BI reporting views
04_validation_queries.sql  Validates row counts, joins, and KPIs
```

## Final Outcome

The final dashboard provides a pharmacy analytics reporting solution that helps users understand prescription cost drivers, patient payment burden, insurance coverage, provider activity, and monthly prescription trends. Because the data is synthetic, the results demonstrate the technical solution and are not intended for real clinical decision-making.
