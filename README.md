# MedScope – Prescription Cost & Pharmacy Analytics Dashboard

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
* Excel dataset

## Data Pipeline

The project follows this flow:

```text
Dataset → Snowflake RAW tables → Snowflake CLEAN tables → Analytics Views → Power BI Dashboard
```

## Snowflake Design

The Snowflake layer is organized into three main layers:

### RAW Layer

Stores the original uploaded pharmacy, patient, doctor, drug, prescription, and insurance claim data.

### CLEAN Layer

Creates deduplicated and validated tables from the raw data to prevent duplicate loads and improve reporting reliability.

### ANALYTICS Layer

Creates reporting-ready views that are connected directly to Power BI.

## Dashboard Pages

### 1. Executive Overview

Shows total prescriptions, total drug cost, average prescription cost, total patients, total doctors, most prescribed drug, monthly prescription trend, and drug cost by category.

### 2. Drug Cost Analysis

Analyzes top drugs by total cost, average prescription cost by drug category, insurance covered versus patient out-of-pocket cost, and high-cost prescription records.

### 3. Patient Prescription Lookup

Allows users to filter by pharmacy, drug, and patient to view detailed prescription records, diagnosis, doctor, specialty, insurance covered, and out-of-pocket cost.

### 4. Doctor Prescriber Analysis

Shows top prescribing doctors, prescriptions by specialty, average prescription cost by doctor, unique patients treated, and doctor-level prescription summaries.

## Key Features

* Built a Snowflake warehouse with raw, clean, and analytics layers.
* Removed duplicate records using SQL clean tables.
* Standardized diagnosis values for cleaner reporting.
* Created Snowflake views for executive KPIs, drug cost analysis, patient lookup, doctor analysis, and monthly prescription trends.
* Connected Snowflake analytics views to Power BI.
* Built an interactive dashboard with slicers, KPI cards, trend charts, lookup tables, and detailed prescription summaries.
* Validated row counts and joins before using the data in Power BI.

## Project Files

```text
data/              Dataset files
sql/               Snowflake SQL scripts
dashboard files/   Power BI dashboard file and exported PDF
docs/              Notes and documentation
python/            Helper scripts if needed
```

## SQL Scripts

```text
01_create_tables.sql       Creates database, schemas, and raw tables
02_clean_layer.sql         Creates clean deduplicated tables
03_analytics_views.sql     Creates Power BI reporting views
04_validation_queries.sql  Validates row counts, joins, and KPIs
```

## Final Outcome

The final dashboard provides a complete pharmacy analytics reporting solution that helps users understand prescription cost drivers, patient payment burden, insurance coverage, provider activity, and monthly prescription trends.
