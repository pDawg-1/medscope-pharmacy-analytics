-- =====================================================
-- MedScope Pharmacy Analytics
-- 01_create_tables.sql
-- Purpose: Create Snowflake database, schemas, and raw tables
-- =====================================================

CREATE DATABASE IF NOT EXISTS MEDSCOPE_DB;

CREATE SCHEMA IF NOT EXISTS MEDSCOPE_DB.RAW;
CREATE SCHEMA IF NOT EXISTS MEDSCOPE_DB.ANALYTICS;

-- =========================
-- RAW TABLES
-- =========================

CREATE TABLE IF NOT EXISTS MEDSCOPE_DB.RAW.PATIENTS (
    patient_id STRING,
    patient_name STRING,
    age NUMBER,
    gender STRING,
    state STRING,
    insurance_type STRING,
    chronic_condition_flag STRING
);

CREATE TABLE IF NOT EXISTS MEDSCOPE_DB.RAW.DOCTORS (
    doctor_id STRING,
    doctor_name STRING,
    specialty STRING,
    hospital_name STRING
);

CREATE TABLE IF NOT EXISTS MEDSCOPE_DB.RAW.PHARMACIES (
    pharmacy_id STRING,
    pharmacy_name STRING,
    city STRING,
    state STRING
);

CREATE TABLE IF NOT EXISTS MEDSCOPE_DB.RAW.DRUGS (
    drug_id STRING,
    drug_name STRING,
    drug_category STRING,
    manufacturer STRING,
    primary_diagnosis STRING,
    standard_unit_cost NUMBER(10,2)
);

CREATE TABLE IF NOT EXISTS MEDSCOPE_DB.RAW.PRESCRIPTIONS (
    prescription_id STRING,
    patient_id STRING,
    doctor_id STRING,
    drug_id STRING,
    pharmacy_id STRING,
    diagnosis STRING,
    prescription_date DATE,
    quantity NUMBER,
    unit_cost NUMBER(10,2),
    total_cost NUMBER(12,2),
    insurance_covered NUMBER(12,2),
    out_of_pocket NUMBER(12,2),
    refill_status STRING,
    payment_type STRING
);

CREATE TABLE IF NOT EXISTS MEDSCOPE_DB.RAW.INSURANCE_CLAIMS (
    claim_id STRING,
    prescription_id STRING,
    patient_id STRING,
    covered_amount NUMBER(12,2),
    claim_amount NUMBER(12,2),
    approved_amount NUMBER(12,2),
    claim_status STRING,
    claim_date DATE
);