# MedScope User Stories and Acceptance Criteria

The stories below describe the main tasks demonstrated in the Power BI report and the controlled chatbot. They are deliberately tied to real pages and views in this repository.

## US-01 Executive overview

**As an** executive sponsor, **I want** a one-page summary of prescription activity and cost **so that** I can understand the overall position without reviewing detail tables.

Acceptance criteria:

- Total prescriptions, total cost, average cost, total patients, and total doctors are visible.
- The most-prescribed drug is identified.
- KPI values match `VW_EXECUTIVE_KPIS`.

## US-02 Drug cost drivers

**As a** pharmacy operations manager, **I want** to compare drug and category costs **so that** I can identify the largest cost drivers.

Acceptance criteria:

- Drugs can be ranked by total cost.
- Average cost uses a weighted calculation where appropriate.
- Insurance-covered and patient-paid amounts are displayed separately.
- Drug-category filtering changes the applicable visuals.

## US-03 Patient prescription lookup

**As a** pharmacy analyst, **I want** to filter prescription details by pharmacy, drug, patient, and diagnosis **so that** I can answer questions such as "Who prescribed Metformin at CVS, and why?" without joining files manually.

Acceptance criteria:

- The lookup displays patient, provider, drug, pharmacy, date, diagnosis, and payment details.
- Selecting CVS Pharmacy and Metformin returns only matching records.
- Age is displayed as a value and is not summed.

## US-04 Provider analysis

**As a** clinical operations analyst, **I want** to compare doctors and specialties **so that** I can review prescribing volume and cost patterns.

Acceptance criteria:

- Doctors can be ranked by prescription count.
- Unique patients and average prescription cost are available by doctor.
- Specialty and doctor filters affect the provider visuals.

## US-05 Monthly trends

**As an** operations manager, **I want** monthly prescription and cost trends **so that** I can identify changes over time.

Acceptance criteria:

- Months appear in chronological order.
- Each month shows prescription volume and cost measures.
- Monthly results reconcile to the underlying clean prescriptions.

## US-06 Data quality

**As a** BI analyst, **I want** repeatable data-quality checks **so that** I can find key, relationship, and cost problems before refreshing the dashboard.

Acceptance criteria:

- Duplicate and null primary keys are reported.
- Orphan relationships are reported.
- Cost and payment mismatches above $0.05 are reported.
- RAW, clean, and view row counts can be reviewed.

## US-07 Controlled analytics chatbot

**As a** non-technical business user, **I want** to ask a supported business question in plain language **so that** I can retrieve a common KPI without writing SQL.

Acceptance criteria:

- Supported KPI questions return values from approved analytics views.
- Recognized drug questions return matching doctor, diagnosis, or availability results.
- Unsupported questions return guidance rather than executing arbitrary SQL.
- Snowflake credentials are read from environment variables.

## US-08 Privacy-safe demonstration

**As a** compliance reviewer, **I want** the demonstration to use synthetic data **so that** no real patient information is exposed.

Acceptance criteria:

- Documentation identifies the dataset as synthetic.
- No real PHI is intentionally included.
- Credentials and local environment files are excluded from source control.
