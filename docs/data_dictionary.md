# MedScope Data Dictionary

## Entity Relationships

```text
PATIENTS 1 ---- * PRESCRIPTIONS * ---- 1 DOCTORS
                       |
                       +---- 1 DRUGS
                       |
                       +---- 1 PHARMACIES
                       |
                       +---- 0..1 INSURANCE_CLAIMS
```

## Patients

| Field | Type | Description | Rule |
| --- | --- | --- | --- |
| patient_id | String | Unique synthetic patient identifier | Primary key; required |
| patient_name | String | Synthetic patient name | Trim whitespace |
| age | Number | Patient age | Must be 0-110; missing values use median |
| gender | String | Standardized gender value | Map `F/M` to `Female/Male` |
| state | String | Patient state | Uppercase |
| insurance_type | String | Insurance category | Title case |
| chronic_condition_flag | String | Chronic-condition indicator | Standardized text |

## Doctors

| Field | Type | Description | Rule |
| --- | --- | --- | --- |
| doctor_id | String | Unique doctor identifier | Primary key; required |
| doctor_name | String | Provider name | Trim whitespace |
| specialty | String | Provider specialty | Title case |
| hospital_name | String | Associated hospital | Missing values become `Unknown Hospital` |

## Pharmacies

| Field | Type | Description | Rule |
| --- | --- | --- | --- |
| pharmacy_id | String | Unique pharmacy identifier | Primary key; required |
| pharmacy_name | String | Pharmacy business name | Standardize CVS capitalization |
| city | String | Pharmacy city | Title case |
| state | String | Pharmacy state | Uppercase |

## Drugs

| Field | Type | Description | Rule |
| --- | --- | --- | --- |
| drug_id | String | Unique drug identifier | Primary key; required |
| drug_name | String | Drug name | Trim whitespace |
| drug_category | String | Reporting category | Title case |
| manufacturer | String | Manufacturer name | Trim whitespace |
| primary_diagnosis | String | Main associated diagnosis | Informational reporting field |
| standard_unit_cost | Decimal | Standard drug unit cost | Missing values use median |

## Prescriptions

| Field | Type | Description | Rule |
| --- | --- | --- | --- |
| prescription_id | String | Unique prescription identifier | Primary key; required |
| patient_id | String | Prescribed patient | Foreign key to patients |
| doctor_id | String | Prescribing doctor | Foreign key to doctors |
| drug_id | String | Prescribed drug | Foreign key to drugs |
| pharmacy_id | String | Dispensing pharmacy | Foreign key to pharmacies |
| diagnosis | String | Prescription diagnosis/reason | Standardized in detail view |
| prescription_date | Date | Prescription date | Used for monthly reporting |
| quantity | Number | Units prescribed | Used in total-cost validation |
| unit_cost | Decimal | Cost per unit | Currency value |
| total_cost | Decimal | Total prescription cost | Expected to equal unit cost x quantity |
| insurance_covered | Decimal | Amount covered by insurance | Missing values become zero |
| out_of_pocket | Decimal | Amount paid by patient | Derived when missing |
| refill_status | String | Refill category | Title case |
| payment_type | String | Payment category | Title case |

## Insurance Claims

| Field | Type | Description | Rule |
| --- | --- | --- | --- |
| claim_id | String | Unique claim identifier | Primary key; required |
| prescription_id | String | Related prescription | Foreign key to prescriptions |
| patient_id | String | Related patient | Reference identifier |
| covered_amount | Decimal | Covered claim amount | Currency value |
| claim_amount | Decimal | Requested claim amount | Currency value |
| approved_amount | Decimal | Approved claim amount | Currency value |
| claim_status | String | Claim processing status | Title case |
| claim_date | Date | Claim activity date | Parsed as date |

## Derived Reporting Fields

| Field | Source | Definition |
| --- | --- | --- |
| standardized_diagnosis | Prescription diagnosis | Maps known diagnosis variations to a reporting label |
| total_prescriptions | Prescription ID | Distinct prescription count |
| total_drug_cost | Total cost | Sum of prescription total cost |
| average_prescription_cost | Total cost | Average prescription total cost |
| weighted_average_prescription_cost | Drug cost analysis | Total cost divided by total prescription count |
| total_insurance_covered | Insurance covered | Sum of covered amount |
| total_out_of_pocket | Out of pocket | Sum of patient-paid amount |
| unique_patients_treated | Patient ID by doctor | Distinct patient count per doctor |
| year_month | Prescription date | `YYYY-MM` reporting period |

