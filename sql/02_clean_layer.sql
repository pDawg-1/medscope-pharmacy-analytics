-- =====================================================
-- MedScope Pharmacy Analytics
-- 02_clean_layer.sql
-- Purpose: Create deduplicated, standardized analytics tables
--          from the Snowflake RAW layer.
-- =====================================================

-- Keep one row per patient and standardize text fields.
CREATE OR REPLACE TABLE MEDSCOPE_DB.ANALYTICS.PATIENTS_CLEAN AS
WITH ranked_patients AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(patient_id)
            ORDER BY TRIM(patient_id)
        ) AS row_num
    FROM MEDSCOPE_DB.RAW.PATIENTS
    WHERE patient_id IS NOT NULL
),
patient_stats AS (
    SELECT MEDIAN(age) AS median_age
    FROM ranked_patients
    WHERE row_num = 1
      AND age BETWEEN 0 AND 110
)
SELECT
    TRIM(patient_id) AS patient_id,
    TRIM(patient_name) AS patient_name,
    TRUNC(COALESCE(age, median_age)) AS age,
    CASE
        WHEN UPPER(TRIM(gender)) IN ('F', 'FEMALE') THEN 'Female'
        WHEN UPPER(TRIM(gender)) IN ('M', 'MALE') THEN 'Male'
        ELSE INITCAP(TRIM(gender))
    END AS gender,
    UPPER(TRIM(state)) AS state,
    INITCAP(TRIM(insurance_type)) AS insurance_type,
    INITCAP(TRIM(chronic_condition_flag)) AS chronic_condition_flag
FROM ranked_patients
CROSS JOIN patient_stats
WHERE row_num = 1
  AND COALESCE(age, median_age) BETWEEN 0 AND 110;


-- Keep one row per doctor and preserve useful records when hospital is missing.
CREATE OR REPLACE TABLE MEDSCOPE_DB.ANALYTICS.DOCTORS_CLEAN AS
SELECT
    TRIM(doctor_id) AS doctor_id,
    TRIM(doctor_name) AS doctor_name,
    INITCAP(TRIM(specialty)) AS specialty,
    COALESCE(NULLIF(TRIM(hospital_name), ''), 'Unknown Hospital') AS hospital_name
FROM MEDSCOPE_DB.RAW.DOCTORS
WHERE doctor_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY TRIM(doctor_id)
    ORDER BY TRIM(doctor_id)
) = 1;


-- Keep one row per pharmacy and standardize names and locations.
CREATE OR REPLACE TABLE MEDSCOPE_DB.ANALYTICS.PHARMACIES_CLEAN AS
SELECT
    TRIM(pharmacy_id) AS pharmacy_id,
    CASE
        WHEN UPPER(TRIM(pharmacy_name)) = 'CVS PHARMACY' THEN 'CVS Pharmacy'
        ELSE INITCAP(TRIM(pharmacy_name))
    END AS pharmacy_name,
    INITCAP(TRIM(city)) AS city,
    UPPER(TRIM(state)) AS state
FROM MEDSCOPE_DB.RAW.PHARMACIES
WHERE pharmacy_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY TRIM(pharmacy_id)
    ORDER BY TRIM(pharmacy_id)
) = 1;


-- Keep one row per drug and preserve currency precision.
CREATE OR REPLACE TABLE MEDSCOPE_DB.ANALYTICS.DRUGS_CLEAN AS
WITH ranked_drugs AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY TRIM(drug_id)
            ORDER BY TRIM(drug_id)
        ) AS row_num
    FROM MEDSCOPE_DB.RAW.DRUGS
    WHERE drug_id IS NOT NULL
),
drug_stats AS (
    SELECT MEDIAN(standard_unit_cost) AS median_unit_cost
    FROM ranked_drugs
    WHERE row_num = 1
      AND standard_unit_cost IS NOT NULL
)
SELECT
    TRIM(drug_id) AS drug_id,
    TRIM(drug_name) AS drug_name,
    INITCAP(TRIM(drug_category)) AS drug_category,
    TRIM(manufacturer) AS manufacturer,
    TRIM(primary_diagnosis) AS primary_diagnosis,
    COALESCE(standard_unit_cost, median_unit_cost) AS standard_unit_cost
FROM ranked_drugs
CROSS JOIN drug_stats
WHERE row_num = 1;


-- Keep one row per prescription and standardize categorical fields.
CREATE OR REPLACE TABLE MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN AS
SELECT
    TRIM(prescription_id) AS prescription_id,
    TRIM(patient_id) AS patient_id,
    TRIM(doctor_id) AS doctor_id,
    TRIM(drug_id) AS drug_id,
    TRIM(pharmacy_id) AS pharmacy_id,
    TRIM(diagnosis) AS diagnosis,
    prescription_date,
    quantity,
    unit_cost,
    total_cost,
    COALESCE(insurance_covered, 0) AS insurance_covered,
    COALESCE(out_of_pocket, total_cost - COALESCE(insurance_covered, 0)) AS out_of_pocket,
    INITCAP(TRIM(refill_status)) AS refill_status,
    INITCAP(TRIM(payment_type)) AS payment_type
FROM MEDSCOPE_DB.RAW.PRESCRIPTIONS
WHERE prescription_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY TRIM(prescription_id)
    ORDER BY TRIM(prescription_id)
) = 1;


-- Keep one row per claim and standardize its status.
CREATE OR REPLACE TABLE MEDSCOPE_DB.ANALYTICS.INSURANCE_CLAIMS_CLEAN AS
SELECT
    TRIM(claim_id) AS claim_id,
    TRIM(prescription_id) AS prescription_id,
    TRIM(patient_id) AS patient_id,
    covered_amount,
    claim_amount,
    approved_amount,
    INITCAP(TRIM(claim_status)) AS claim_status,
    claim_date
FROM MEDSCOPE_DB.RAW.INSURANCE_CLAIMS
WHERE claim_id IS NOT NULL
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY TRIM(claim_id)
    ORDER BY TRIM(claim_id)
) = 1;
