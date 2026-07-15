# MedScope Functional Requirements

## Data Ingestion and Preparation

| ID | Functional requirement | Priority | Implementation |
| --- | --- | --- | --- |
| FR-01 | The system shall create RAW tables for all six source entities. | Must | `sql/01_create_tables.sql` |
| FR-02 | The system shall load staged CSV files into the matching RAW tables. | Must | `sql/01_load_raw_data.sql` |
| FR-03 | The system shall remove duplicate records by business identifier. | Must | `sql/02_clean_layer.sql` |
| FR-04 | The system shall trim and standardize configured categorical fields. | Must | SQL clean layer and `python/clean_raw_data.py` |
| FR-05 | The system shall handle missing age and cost values using documented rules. | Must | SQL and Python cleaning logic |
| FR-06 | The system shall preserve currency precision for cost fields. | Must | Snowflake `NUMBER` definitions and DAX measures |

## Analytics and Reporting

| ID | Functional requirement | Priority | Implementation |
| --- | --- | --- | --- |
| FR-07 | The system shall create a joined prescription-detail view. | Must | `VW_PRESCRIPTION_DETAIL` |
| FR-08 | The system shall calculate total prescriptions, total cost, average cost, total patients, total doctors, and most-prescribed drug. | Must | `VW_EXECUTIVE_KPIS` |
| FR-09 | The system shall aggregate cost and coverage metrics by drug. | Must | `VW_DRUG_COST_ANALYSIS` |
| FR-10 | The system shall aggregate prescription and cost metrics by doctor. | Must | `VW_DOCTOR_PRESCRIBER_ANALYSIS` |
| FR-11 | The system shall provide patient-level prescription details for filtering and lookup. | Must | `VW_PATIENT_PRESCRIPTION_LOOKUP` |
| FR-12 | The system shall aggregate prescription and cost metrics by month. | Should | `VW_MONTHLY_PRESCRIPTION_TREND` |
| FR-13 | The dashboard shall show an Executive Overview page. | Must | Power BI page 1 |
| FR-14 | The dashboard shall show drug-cost and payment analysis. | Must | Power BI page 2 |
| FR-15 | The dashboard shall allow filtering by patient, drug, pharmacy, and diagnosis. | Must | Power BI page 3 |
| FR-16 | The dashboard shall show doctor and specialty analysis. | Must | Power BI page 4 |
| FR-17 | The system shall calculate weighted average prescription cost without summing averages. | Must | DAX weighted-average measure |

## Validation and Conversational Access

| ID | Functional requirement | Priority | Implementation |
| --- | --- | --- | --- |
| FR-18 | The system shall report duplicate and null primary keys. | Must | `python/data_quality_checks.py` |
| FR-19 | The system shall report orphan foreign-key records. | Must | Python checks and SQL join validation |
| FR-20 | The system shall report cost and payment equation mismatches over $0.05. | Must | `check_cost_logic()` |
| FR-21 | The system shall compare RAW, clean, and analytics row counts. | Must | `sql/04_validation_queries.sql` |
| FR-22 | The chatbot shall answer supported KPI questions using Snowflake analytics views. | Could | `chatbot/app.py` |
| FR-23 | The chatbot shall escape recognized drug values before query construction. | Must | `safe_sql_text()` |
| FR-24 | The chatbot shall return a supported-question message for unmatched questions. | Should | Chatbot fallback response |

## Requirement Status

`Implemented` means that a repository artifact exists. It does not by itself prove production readiness; acceptance is recorded through the UAT cases and evidence described in `traceability_matrix.md` and `uat_test_plan.md`.

