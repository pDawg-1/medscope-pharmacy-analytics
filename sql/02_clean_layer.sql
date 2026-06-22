-- =====================================================
-- MedScope Pharmacy Analytics
-- 03_analytics_views.sql
-- Purpose: Create analytics-ready Snowflake views for Power BI
-- =====================================================

-- =========================
-- 1. Prescription Detail View
-- =========================

CREATE OR REPLACE VIEW MEDSCOPE_DB.ANALYTICS.VW_PRESCRIPTION_DETAIL AS
SELECT
    pr.prescription_id,
    pr.prescription_date,

    pt.patient_id,
    pt.patient_name,
    pt.age,
    pt.gender,
    pt.state AS patient_state,
    pt.insurance_type,
    pt.chronic_condition_flag,

    doc.doctor_id,
    doc.doctor_name,
    doc.specialty,
    doc.hospital_name,

    ph.pharmacy_id,
    ph.pharmacy_name,
    ph.city AS pharmacy_city,
    ph.state AS pharmacy_state,

    dr.drug_id,
    dr.drug_name,
    dr.drug_category,
    dr.manufacturer,
    dr.primary_diagnosis,

    CASE
        WHEN UPPER(TRIM(pr.diagnosis)) IN ('T2D', 'DIABETES MELLITUS TYPE 2', 'TYPE 2 DIABETES')
            THEN 'Type 2 Diabetes'
        WHEN UPPER(TRIM(pr.diagnosis)) = 'RA'
            THEN 'Rheumatoid Arthritis'
        ELSE pr.diagnosis
    END AS standardized_diagnosis,

    pr.quantity,
    pr.unit_cost,
    pr.total_cost,
    pr.insurance_covered,
    pr.out_of_pocket,
    pr.refill_status,
    pr.payment_type,

    ic.claim_id,
    ic.claim_amount,
    ic.approved_amount,
    ic.claim_status,
    ic.claim_date

FROM MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN pr
LEFT JOIN MEDSCOPE_DB.ANALYTICS.PATIENTS_CLEAN pt
    ON TRIM(UPPER(pr.patient_id)) = TRIM(UPPER(pt.patient_id))
LEFT JOIN MEDSCOPE_DB.ANALYTICS.DOCTORS_CLEAN doc
    ON TRIM(UPPER(pr.doctor_id)) = TRIM(UPPER(doc.doctor_id))
LEFT JOIN MEDSCOPE_DB.ANALYTICS.PHARMACIES_CLEAN ph
    ON TRIM(UPPER(pr.pharmacy_id)) = TRIM(UPPER(ph.pharmacy_id))
LEFT JOIN MEDSCOPE_DB.ANALYTICS.DRUGS_CLEAN dr
    ON TRIM(UPPER(pr.drug_id)) = TRIM(UPPER(dr.drug_id))
LEFT JOIN MEDSCOPE_DB.ANALYTICS.INSURANCE_CLAIMS_CLEAN ic
    ON TRIM(UPPER(pr.prescription_id)) = TRIM(UPPER(ic.prescription_id));


-- =========================
-- 2. Executive KPI View
-- =========================

CREATE OR REPLACE VIEW MEDSCOPE_DB.ANALYTICS.VW_EXECUTIVE_KPIS AS
WITH prescription_metrics AS (
    SELECT
        COUNT(DISTINCT prescription_id) AS total_prescriptions,
        ROUND(SUM(total_cost), 2) AS total_drug_cost,
        ROUND(AVG(total_cost), 2) AS average_prescription_cost
    FROM MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN
),

patient_metrics AS (
    SELECT
        COUNT(DISTINCT patient_id) AS total_patients
    FROM MEDSCOPE_DB.ANALYTICS.PATIENTS_CLEAN
),

doctor_metrics AS (
    SELECT
        COUNT(DISTINCT doctor_id) AS total_doctors
    FROM MEDSCOPE_DB.ANALYTICS.DOCTORS_CLEAN
),

most_prescribed AS (
    SELECT
        dr.drug_name,
        COUNT(*) AS prescription_count
    FROM MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN pr
    LEFT JOIN MEDSCOPE_DB.ANALYTICS.DRUGS_CLEAN dr
        ON TRIM(UPPER(pr.drug_id)) = TRIM(UPPER(dr.drug_id))
    GROUP BY dr.drug_name
    QUALIFY ROW_NUMBER() OVER (ORDER BY COUNT(*) DESC) = 1
)

SELECT
    pm.total_prescriptions,
    pm.total_drug_cost,
    pm.average_prescription_cost,
    pt.total_patients,
    dm.total_doctors,
    mp.drug_name AS most_prescribed_drug
FROM prescription_metrics pm
CROSS JOIN patient_metrics pt
CROSS JOIN doctor_metrics dm
CROSS JOIN most_prescribed mp;


-- =========================
-- 3. Drug Cost Analysis View
-- =========================

CREATE OR REPLACE VIEW MEDSCOPE_DB.ANALYTICS.VW_DRUG_COST_ANALYSIS AS
SELECT
    dr.drug_id,
    dr.drug_name,
    dr.drug_category,
    dr.manufacturer,

    COUNT(pr.prescription_id) AS total_prescriptions,
    ROUND(COALESCE(SUM(pr.total_cost), 0), 2) AS total_drug_cost,
    ROUND(COALESCE(AVG(pr.total_cost), 0), 2) AS average_prescription_cost,
    ROUND(COALESCE(SUM(pr.insurance_covered), 0), 2) AS total_insurance_covered,
    ROUND(COALESCE(SUM(pr.out_of_pocket), 0), 2) AS total_out_of_pocket

FROM MEDSCOPE_DB.ANALYTICS.DRUGS_CLEAN dr
LEFT JOIN MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN pr
    ON TRIM(UPPER(dr.drug_id)) = TRIM(UPPER(pr.drug_id))

GROUP BY
    dr.drug_id,
    dr.drug_name,
    dr.drug_category,
    dr.manufacturer;


-- =========================
-- 4. Doctor Prescriber Analysis View
-- =========================

CREATE OR REPLACE VIEW MEDSCOPE_DB.ANALYTICS.VW_DOCTOR_PRESCRIBER_ANALYSIS AS
SELECT
    doc.doctor_id,
    doc.doctor_name,
    doc.specialty,
    doc.hospital_name,

    COUNT(pr.prescription_id) AS total_prescriptions,
    COUNT(DISTINCT pr.patient_id) AS unique_patients_treated,

    ROUND(SUM(pr.total_cost), 2) AS total_prescription_cost,
    ROUND(AVG(pr.total_cost), 2) AS average_prescription_cost,

    ROUND(SUM(pr.insurance_covered), 2) AS total_insurance_covered,
    ROUND(SUM(pr.out_of_pocket), 2) AS total_out_of_pocket

FROM MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN pr
LEFT JOIN MEDSCOPE_DB.ANALYTICS.DOCTORS_CLEAN doc
    ON TRIM(UPPER(pr.doctor_id)) = TRIM(UPPER(doc.doctor_id))

GROUP BY
    doc.doctor_id,
    doc.doctor_name,
    doc.specialty,
    doc.hospital_name;


-- =========================
-- 5. Patient Prescription Lookup View
-- =========================

CREATE OR REPLACE VIEW MEDSCOPE_DB.ANALYTICS.VW_PATIENT_PRESCRIPTION_LOOKUP AS
SELECT
    patient_id,
    patient_name,
    age,
    gender,
    patient_state,
    insurance_type,
    chronic_condition_flag,

    prescription_id,
    prescription_date,

    drug_name,
    drug_category,
    manufacturer,

    doctor_name,
    specialty,
    hospital_name,

    pharmacy_name,
    pharmacy_city,
    pharmacy_state,

    standardized_diagnosis,
    quantity,
    unit_cost,
    total_cost,
    insurance_covered,
    out_of_pocket,
    refill_status,
    payment_type,
    claim_status

FROM MEDSCOPE_DB.ANALYTICS.VW_PRESCRIPTION_DETAIL;


-- =========================
-- 6. Monthly Prescription Trend View
-- =========================

CREATE OR REPLACE VIEW MEDSCOPE_DB.ANALYTICS.VW_MONTHLY_PRESCRIPTION_TREND AS
SELECT
    TO_CHAR(prescription_date, 'YYYY-MM') AS year_month,
    COUNT(DISTINCT prescription_id) AS total_prescriptions,
    ROUND(SUM(total_cost), 2) AS total_drug_cost,
    ROUND(AVG(total_cost), 2) AS average_prescription_cost,
    ROUND(SUM(insurance_covered), 2) AS total_insurance_covered,
    ROUND(SUM(out_of_pocket), 2) AS total_out_of_pocket
FROM MEDSCOPE_DB.ANALYTICS.PRESCRIPTIONS_CLEAN
GROUP BY TO_CHAR(prescription_date, 'YYYY-MM')
ORDER BY year_month;