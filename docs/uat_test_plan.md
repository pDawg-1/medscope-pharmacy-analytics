# MedScope User Acceptance Test Plan

## Objective

Confirm that MedScope satisfies its mandatory business requirements and produces reliable dashboard results for the synthetic demonstration dataset.

## Entry Criteria

- RAW files are available and use the expected structure.
- Snowflake load and transformation scripts complete without critical errors.
- Analytics views exist.
- Data-quality checks have been executed.
- Power BI model refresh completes.

## Exit Criteria

- All Must-priority UAT cases pass.
- No open critical data-quality defect remains.
- KPI totals reconcile with Snowflake validation queries.
- Business owner approves the demonstrated workflows.

## Test Cases

| ID | Scenario | Steps | Expected result | Requirement | Status |
| --- | --- | --- | --- | --- | --- |
| UAT-01 | Load all source entities | Run create/load scripts and review RAW counts | Six RAW tables contain expected records | BR-01, FR-01, FR-02 | Not executed |
| UAT-02 | Validate clean keys and joins | Run Python checks and SQL join validation | No duplicate/null primary keys or orphan relationships | BR-08, FR-18, FR-19 | Not executed |
| UAT-03 | Reconcile executive KPIs | Compare dashboard cards with `VW_EXECUTIVE_KPIS` | All displayed KPI values match Snowflake | BR-02 | Not executed |
| UAT-04 | Review drug cost ranking | Sort drugs by total cost on page 2 | Ordering and totals match `VW_DRUG_COST_ANALYSIS` | BR-03 | Not executed |
| UAT-05 | Reconcile payment amounts | Compare insurance and out-of-pocket totals | Components reconcile with total cost within tolerance | BR-04, RULE-06 | Not executed |
| UAT-06 | Identify top prescriber | Compare page 4 ranking with doctor view | Same doctor and prescription count are returned | BR-05 | Not executed |
| UAT-07 | CVS and Metformin lookup | Select CVS Pharmacy and Metformin | Only matching detail records appear with provider and diagnosis | BR-06 | Not executed |
| UAT-08 | Validate monthly trend | Review chronological monthly chart and SQL results | Months are ordered and values reconcile | BR-07 | Not executed |
| UAT-09 | Detect financial mismatch | Introduce or identify a cost difference over $0.05 in a test copy | Validation reports the mismatch | BR-08, FR-20 | Not executed |
| UAT-10 | Ask supported chatbot question | Ask `What is the total drug cost?` | Chatbot returns the Snowflake KPI value | BR-09, FR-22 | Not executed |
| UAT-11 | Ask unsupported chatbot question | Submit an unrelated question | Chatbot lists supported question areas and runs no arbitrary SQL | BR-09, FR-24 | Not executed |
| UAT-12 | Review privacy and secrets | Inspect data statement, tracked files, and ignored environment file | Data is documented as synthetic and credentials are untracked | BR-10 | Not executed |

## Defect Severity

| Severity | Definition | Example |
| --- | --- | --- |
| Critical | Prevents core reporting or exposes protected information/credentials | Dashboard cannot refresh; secret committed |
| High | Produces materially incorrect KPI or relationship result | Total cost does not reconcile |
| Medium | Affects one workflow with a workaround | One slicer does not filter a secondary visual |
| Low | Cosmetic or documentation issue | Label spacing or minor wording |

## Evidence to Capture

- Validation query result screenshots or exported results.
- Power BI page and filter-state screenshots.
- Expected-versus-actual KPI values.
- Test date, tester, environment, and status.
- Defect identifier and retest result where applicable.

