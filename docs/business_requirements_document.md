# MedScope Business Requirements Document

## 1. Document Purpose

This Business Requirements Document defines the business problem, scope, stakeholders, requirements, assumptions, and success criteria for MedScope, a pharmacy prescription-cost and utilization analytics solution.

## 2. Business Problem

Pharmacy and healthcare operations teams receive prescription information across patients, doctors, pharmacies, drugs, and insurance claims. Without a consolidated reporting layer, users must combine separate source extracts to answer basic cost, utilization, coverage, and prescribing questions. This creates slow analysis, inconsistent calculations, and limited visibility into patient financial burden.

## 3. Business Objective

Create a trusted analytics solution that allows authorized business users to:

- Monitor prescription volume and cost.
- Identify major drug-cost drivers.
- Compare insurance-covered and patient-paid amounts.
- Analyze doctor prescribing activity.
- Review monthly prescription trends.
- Filter prescription details by patient, pharmacy, drug, diagnosis, and provider.
- Ask a controlled set of plain-language analytics questions.

## 4. Stakeholders

| Stakeholder | Need | MedScope capability |
| --- | --- | --- |
| Executive sponsor | High-level cost and utilization visibility | Executive Overview page |
| Pharmacy operations manager | Pharmacy and drug activity analysis | Drug Cost and Patient Lookup pages |
| Finance/claims analyst | Insurance and out-of-pocket reconciliation | Coverage measures and validation rules |
| Clinical operations analyst | Provider, specialty, drug, and diagnosis patterns | Doctor Prescriber Analysis page |
| Data engineer/administrator | Repeatable and auditable data preparation | RAW tables, clean tables, analytics views |
| BI analyst | Stable reporting fields and calculations | Analytics views and DAX measures |
| Compliance/privacy reviewer | Protection of patient information | Synthetic dataset and limited project scope |

## 5. Project Scope

### In scope

- Six synthetic source extracts: patients, doctors, pharmacies, drugs, prescriptions, and insurance claims.
- Data loading into Snowflake RAW tables.
- Deduplication, standardization, and null handling.
- Reporting-ready Snowflake analytics views.
- Power BI pages for executive, drug-cost, patient, and provider analysis.
- Controlled Flask chatbot questions mapped to approved SQL statements.
- Data-quality and business-rule validation.

### Out of scope

- Clinical diagnosis or treatment recommendations.
- Real patient or protected health information.
- Prescription ordering or claim adjudication.
- Source-system write-back.
- Real-time streaming.
- General-purpose generative AI questions.
- Production identity and access management.

## 6. Assumptions and Constraints

- All supplied records are synthetic.
- Source extracts use the documented column structures.
- Snowflake credentials and warehouse access are provided through environment variables.
- Power BI users have permission to access the reporting model.
- Dashboard freshness depends on completion of the batch load and report refresh.
- The chatbot supports only documented question patterns.

## 7. High-Level Business Requirements

| ID | Business requirement | Business value | Priority |
| --- | --- | --- | --- |
| BR-01 | Provide one consolidated prescription analytics solution. | Reduces manual reconciliation across source extracts. | Must |
| BR-02 | Show executive prescription, cost, patient, doctor, and drug KPIs. | Enables rapid operational review. | Must |
| BR-03 | Identify drug and category cost drivers. | Supports cost-management decisions. | Must |
| BR-04 | Compare insurance coverage with patient out-of-pocket cost. | Exposes affordability and payment burden. | Must |
| BR-05 | Analyze provider and specialty prescribing activity. | Supports provider-pattern analysis. | Must |
| BR-06 | Allow detailed prescription lookup using business filters. | Reduces time required to investigate individual records. | Must |
| BR-07 | Display monthly prescription and cost trends. | Supports change and seasonality analysis. | Should |
| BR-08 | Validate source keys, joins, nulls, and financial calculations. | Improves trust in reported results. | Must |
| BR-09 | Provide controlled natural-language access to common KPIs. | Improves accessibility for non-technical users. | Could |
| BR-10 | Prevent use of real protected health information in the demonstration. | Reduces privacy and compliance risk. | Must |

## 8. Business Rules

| ID | Rule |
| --- | --- |
| RULE-01 | Each clean entity must contain no more than one record per primary identifier. |
| RULE-02 | Patient age must be between 0 and 110 after cleaning. |
| RULE-03 | Missing insurance-covered amounts default to zero. |
| RULE-04 | Missing out-of-pocket amount is derived as total cost minus insurance-covered amount. |
| RULE-05 | Total cost should equal unit cost multiplied by quantity within a $0.05 tolerance. |
| RULE-06 | Insurance-covered plus out-of-pocket should equal total cost within a $0.05 tolerance. |
| RULE-07 | Prescription foreign keys should match patient, doctor, pharmacy, and drug entities. |
| RULE-08 | Diagnosis variants for Type 2 Diabetes and Rheumatoid Arthritis are standardized for reporting. |
| RULE-09 | KPI counts use distinct business identifiers where duplication could overstate results. |
| RULE-10 | Chatbot questions execute only predefined query patterns against analytics views. |

## 9. Non-Functional Requirements

| ID | Requirement | Acceptance measure |
| --- | --- | --- |
| NFR-01 | Usability | A user can reach each main analysis area from a clearly named report page. |
| NFR-02 | Data quality | Validation reports zero duplicate/null primary keys and zero orphan foreign keys. |
| NFR-03 | Accuracy | Financial mismatches above $0.05 are identified before report approval. |
| NFR-04 | Security | Credentials are loaded from environment variables and are not committed to source control. |
| NFR-05 | Privacy | Repository data is synthetic and contains no real PHI. |
| NFR-06 | Maintainability | Load, clean, analytics, and validation SQL are separated into ordered scripts. |
| NFR-07 | Auditability | Requirement, source, transformation, report, and UAT mappings are documented. |
| NFR-08 | Performance target | Standard dashboard interactions should respond within five seconds under demonstration-scale data. |

## 10. Success Criteria

- All mandatory requirements pass UAT.
- Key and relationship checks report no critical defects.
- Dashboard totals match approved Snowflake validation queries.
- Users can complete the executive, cost, provider, and patient lookup scenarios.
- No credentials or real patient information appear in the repository.

## 11. Risks and Mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Inconsistent source values | Incorrect grouping and filters | Standardize text and diagnosis values in the clean and analytics layers. |
| Duplicate source records | Inflated counts and costs | Deduplicate by business key using `ROW_NUMBER()`. |
| Broken entity relationships | Missing report details | Run foreign-key and join-completeness checks. |
| Incorrect financial totals | Untrusted dashboard | Validate cost and payment equations with a tolerance. |
| Credential exposure | Security incident | Use ignored `.env` files and environment variables. |
| Chatbot misunderstood as unrestricted AI | Incorrect stakeholder expectations | Document supported question patterns and approved SQL mapping. |

