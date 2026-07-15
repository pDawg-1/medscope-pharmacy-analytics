# MedScope Current-State and Future-State Process Flows

## Current-State Business Process

The starting point for this project was a set of separate CSV extracts. Without a shared warehouse model, an analyst would repeat the following work for each request.

```mermaid
flowchart LR
    A[Receive separate CSV extracts] --> B[Open and inspect files manually]
    B --> C[Clean inconsistent values]
    C --> D[Join patients, doctors, drugs, pharmacies, prescriptions, and claims]
    D --> E[Recalculate KPIs]
    E --> F[Build one-off charts or answer stakeholder question]
    F --> G[Repeat work for the next request]
```

Problems with that approach:

- Repeated manual preparation.
- Risk of inconsistent joins and calculations.
- Slow response to stakeholder questions.
- No single definition of KPIs such as total prescription cost.
- Limited audit trail for cleaning and validation.

## Future-State MedScope Process

```mermaid
flowchart LR
    A[Synthetic source CSV files] --> B[Snowflake RAW tables]
    B --> C[Deduplicate and standardize]
    C --> D[Clean analytics tables]
    D --> E[Reporting views]
    E --> F[Validation queries and quality checks]
    F --> G[Power BI dashboard]
    E --> H[Controlled Flask chatbot]
    G --> I[Business decision support]
    H --> I
```

## Proposed Refresh Sequence

1. Confirm that all six expected source files are present.
2. Upload the files to the Snowflake internal stage.
3. Run the RAW load script.
4. Run the clean-layer transformations.
5. Rebuild analytics views.
6. Execute SQL and Python validation checks.
7. Investigate critical validation failures.
8. Refresh the Power BI model only after validation approval.
9. Reconcile the headline KPIs and quickly test the main filters before sharing the report.

## Exception Flow

```mermaid
flowchart TD
    A[Run validation] --> B{Critical issue found?}
    B -- No --> C[Approve dashboard refresh]
    B -- Yes --> D[Record affected table and rule]
    D --> E[Correct source or transformation]
    E --> F[Reload affected data]
    F --> A
```

## Responsibility Summary

This is a lightweight RACI-style view for the project. Exact job titles may change in a real organization.

| Activity | Business owner | Data/BI owner | Reviewer |
| --- | --- | --- | --- |
| Define KPIs and business rules | Accountable | Consulted | Consulted |
| Load and transform data | Informed | Responsible | Informed |
| Validate joins and financial logic | Consulted | Responsible | Accountable |
| Build dashboard visuals | Consulted | Responsible | Consulted |
| Conduct UAT | Accountable | Supports | Responsible |
| Approve release/refresh | Accountable | Informed | Consulted |
