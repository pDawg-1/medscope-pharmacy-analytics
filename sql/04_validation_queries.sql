-- =====================================================
-- MedScope Pharmacy Analytics
-- 04_validation_queries.sql
-- Purpose: Validate raw, clean, and analytics view row counts
-- =====================================================

-- =========================
-- 1. Raw table count validation
-- =========================

SELECT 'PATIENTS_RAW' AS table_name, COUNT(*) AS row_count
FROM MEDSCOPE_DB.RAW.PATIENTS
UNION ALL
SELECT 'DOCTORS_RAW', COUNT(*)
FROM MEDSCOPE_DB.RAW.DOCTORS
UNION ALL
SELECT 'PHARMACIES_RAW', COUNT(*)
FROM MEDSCOPE_DB.RAW.PHARMACIES
UNION ALL
SELECT 'DRUGS_RAW', COUNT(*)
FROM MEDSCOPE_DB.RAW.DRUGS
UNION ALL
SELECT 'PRESCRIPTIONS_RAW', COUNT(*)
FROM MEDSCOPE_DB.RAW.PRESCRIPTIONS
UNION ALL
SELECT 'INSURANCE_CLAIMS_RAW', COUNT(*)
FROM MEDSCOPE_DB.RAW.INSURANCE_CLAIMS;


-- =========================
-- 2. Clean table count validation
-- =========================

SELECT 'PATIENTS_CLEAN' AS table_name, COUNT(*) AS row_count
FROM MEDSCOPE_DB.ANALYTICS.PATIENTS_CLEAN
UNION ALL
SELECT 'DOCTORS_CLEAN', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.DOCTORS_CLEAN
UNION ALL
SELECT 'PHARMACIES_CLEAN', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.PHARMACIES_CLEAN
UNION ALL
SELECT 'DRUGS_CLEAN', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.DRUGS_CLEAN
UNION ALL
SELECT 'PRESCRIPTIONS_CLEAN', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN
UNION ALL
SELECT 'INSURANCE_CLAIMS_CLEAN', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.INSURANCE_CLAIMS_CLEAN;


-- =========================
-- 3. Join validation for prescription detail view
-- =========================

SELECT
    COUNT(*) AS total_rows,
    COUNT(patient_name) AS patient_matched_rows,
    COUNT(doctor_name) AS doctor_matched_rows,
    COUNT(pharmacy_name) AS pharmacy_matched_rows,
    COUNT(drug_name) AS drug_matched_rows
FROM MEDSCOPE_DB.ANALYTICS.VW_PRESCRIPTION_DETAIL;


-- =========================
-- 4. Analytics view count validation
-- =========================

SELECT 'VW_PRESCRIPTION_DETAIL' AS view_name, COUNT(*) AS row_count
FROM MEDSCOPE_DB.ANALYTICS.VW_PRESCRIPTION_DETAIL
UNION ALL
SELECT 'VW_EXECUTIVE_KPIS', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS
UNION ALL
SELECT 'VW_DRUG_COST_ANALYSIS', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.VW_DRUG_COST_ANALYSIS
UNION ALL
SELECT 'VW_DOCTOR_PRESCRIBER_ANALYSIS', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.VW_DOCTOR_PRESCRIBER_ANALYSIS
UNION ALL
SELECT 'VW_PATIENT_PRESCRIPTION_LOOKUP', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.VW_PATIENT_PRESCRIPTION_LOOKUP
UNION ALL
SELECT 'VW_MONTHLY_PRESCRIPTION_TREND', COUNT(*)
FROM MEDSCOPE_DB.ANALYTICS.VW_MONTHLY_PRESCRIPTION_TREND;


-- =========================
-- 5. Executive KPI validation
-- =========================

SELECT *
FROM MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS;


-- =========================
-- 6. Patient lookup validation example
-- CVS Pharmacy + Metformin
-- =========================

SELECT
    patient_name,
    age,
    gender,
    standardized_diagnosis,
    drug_name,
    doctor_name,
    specialty,
    pharmacy_name,
    prescription_date,
    total_cost,
    insurance_covered,
    out_of_pocket
FROM MEDSCOPE_DB.ANALYTICS.VW_PATIENT_PRESCRIPTION_LOOKUP
WHERE pharmacy_name ILIKE '%CVS%'
  AND drug_name ILIKE '%Metformin%'
ORDER BY prescription_date;