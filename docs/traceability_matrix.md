# MedScope Requirements Traceability Matrix

This matrix connects business needs to implementation and acceptance evidence.

| Business ID | Functional IDs | Implementation artifact | Dashboard/output | UAT cases |
| --- | --- | --- | --- | --- |
| BR-01 | FR-01 to FR-07 | Create, load, clean, and detail-view SQL | Consolidated data model | UAT-01, UAT-02 |
| BR-02 | FR-08, FR-13 | `VW_EXECUTIVE_KPIS` | Executive Overview | UAT-03 |
| BR-03 | FR-09, FR-14, FR-17 | Drug-cost view and weighted DAX measure | Drug Cost Analysis | UAT-04 |
| BR-04 | FR-09, FR-14 | Coverage and out-of-pocket fields | Drug Cost Analysis | UAT-05 |
| BR-05 | FR-10, FR-16 | Doctor analysis view | Doctor Prescriber Analysis | UAT-06 |
| BR-06 | FR-11, FR-15 | Patient lookup view | Patient/Customer View | UAT-07 |
| BR-07 | FR-12 | Monthly trend view | Monthly trend chart | UAT-08 |
| BR-08 | FR-18 to FR-21 | Python checks and SQL validation | Validation output | UAT-01, UAT-02, UAT-09 |
| BR-09 | FR-22 to FR-24 | `chatbot/app.py` | Analytics chatbot | UAT-10, UAT-11 |
| BR-10 | NFR-04, NFR-05 | Synthetic-data statement and `.gitignore` | Privacy-safe repository | UAT-12 |

## Change-Control Rule

When a requirement changes:

1. Update the relevant BR or FR entry.
2. Identify affected SQL, Python, DAX, Power BI, and chatbot artifacts.
3. Update the mapped UAT case.
4. Re-run validation and record the result before approval.

