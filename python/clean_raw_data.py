"""
MedScope raw-data cleaning script.

Purpose:
- Reads intentional messy raw CSV files from data/raw
- Fixes common healthcare analytics data issues
- Writes cleaned CSV files to data/cleaned

Run from the project root:
    python python/clean_raw_data.py
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
CLEAN = ROOT / "data" / "cleaned"
CLEAN.mkdir(parents=True, exist_ok=True)

def standardize_title(series):
    return series.astype(str).str.strip().str.title()

def clean_patients():
    df = pd.read_csv(RAW / "patients_raw.csv")
    df = df.drop_duplicates(subset=["patient_id"])
    df["gender"] = df["gender"].replace({"F": "Female", "M": "Male"}).str.strip().str.title()
    df["insurance_type"] = df["insurance_type"].astype(str).str.strip().str.title()
    df["age"] = pd.to_numeric(df["age"], errors="coerce")
    df["age"] = df["age"].fillna(df["age"].median()).astype(int)
    df = df[(df["age"] >= 0) & (df["age"] <= 110)]
    df.to_csv(CLEAN / "patients.csv", index=False)

def clean_doctors():
    df = pd.read_csv(RAW / "doctors_raw.csv")
    df = df.drop_duplicates(subset=["doctor_id"])
    df["doctor_name"] = df["doctor_name"].astype(str).str.strip()
    df["specialty"] = df["specialty"].astype(str).str.strip().str.title()
    df["hospital_name"] = df["hospital_name"].fillna("Unknown Hospital").astype(str).str.strip()
    df.to_csv(CLEAN / "doctors.csv", index=False)

def clean_pharmacies():
    df = pd.read_csv(RAW / "pharmacies_raw.csv")
    df = df.drop_duplicates(subset=["pharmacy_id"])
    df["pharmacy_name"] = df["pharmacy_name"].astype(str).str.strip().str.title()
    df["pharmacy_name"] = df["pharmacy_name"].replace({"Cvs Pharmacy": "CVS Pharmacy"})
    df["city"] = df["city"].astype(str).str.strip().str.title()
    df["state"] = df["state"].astype(str).str.strip().str.upper()
    df.to_csv(CLEAN / "pharmacies.csv", index=False)

def clean_drugs():
    df = pd.read_csv(RAW / "drugs_raw.csv")
    df = df.drop_duplicates(subset=["drug_id"])
    df["drug_category"] = df["drug_category"].astype(str).str.strip().str.title()
    df["standard_unit_cost"] = pd.to_numeric(df["standard_unit_cost"], errors="coerce")
    df["standard_unit_cost"] = df["standard_unit_cost"].fillna(df["standard_unit_cost"].median())
    df.to_csv(CLEAN / "drugs.csv", index=False)

def clean_prescriptions():
    df = pd.read_csv(RAW / "prescriptions_raw.csv")
    df = df.drop_duplicates(subset=["prescription_id"])
    df["prescription_date"] = pd.to_datetime(df["prescription_date"], errors="coerce")
    df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce").fillna(0).astype(int)
    money_cols = ["unit_cost", "total_cost", "insurance_covered", "out_of_pocket"]
    for col in money_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["insurance_covered"] = df["insurance_covered"].fillna(0)
    df["out_of_pocket"] = df["out_of_pocket"].fillna(df["total_cost"] - df["insurance_covered"])
    df["refill_status"] = df["refill_status"].astype(str).str.strip().str.title()
    df["payment_type"] = df["payment_type"].astype(str).str.strip().str.title()
    df.to_csv(CLEAN / "prescriptions.csv", index=False)

def clean_claims():
    df = pd.read_csv(RAW / "insurance_claims_raw.csv")
    df = df.drop_duplicates(subset=["claim_id"])
    df["claim_status"] = df["claim_status"].astype(str).str.strip().str.title()
    df["claim_date"] = pd.to_datetime(df["claim_date"], errors="coerce")
    df.to_csv(CLEAN / "insurance_claims.csv", index=False)

if __name__ == "__main__":
    clean_patients()
    clean_doctors()
    clean_pharmacies()
    clean_drugs()
    clean_prescriptions()
    clean_claims()
    print("Cleaned MedScope data written to data/cleaned/")
