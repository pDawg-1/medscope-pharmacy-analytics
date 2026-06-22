"""
MedScope data quality checks.

Run from the project root:
    python python/data_quality_checks.py
"""

from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CLEAN = ROOT / "data" / "cleaned"

tables = {
    "patients": pd.read_csv(CLEAN / "patients.csv"),
    "doctors": pd.read_csv(CLEAN / "doctors.csv"),
    "pharmacies": pd.read_csv(CLEAN / "pharmacies.csv"),
    "drugs": pd.read_csv(CLEAN / "drugs.csv"),
    "prescriptions": pd.read_csv(CLEAN / "prescriptions.csv"),
    "insurance_claims": pd.read_csv(CLEAN / "insurance_claims.csv"),
}

def check_primary_key(table_name, key):
    df = tables[table_name]
    duplicate_count = df[key].duplicated().sum()
    null_count = df[key].isna().sum()
    print(f"{table_name}.{key}: duplicates={duplicate_count}, nulls={null_count}")

def check_nulls(table_name):
    df = tables[table_name]
    print(f"\nNull counts for {table_name}:")
    print(df.isna().sum()[df.isna().sum() > 0])

def check_foreign_key(child_table, child_key, parent_table, parent_key):
    child = tables[child_table]
    parent = tables[parent_table]
    missing = ~child[child_key].isin(parent[parent_key])
    print(f"{child_table}.{child_key} -> {parent_table}.{parent_key}: orphan rows={missing.sum()}")

def check_cost_logic():
    rx = tables["prescriptions"].copy()
    rx["expected_total"] = (rx["unit_cost"] * rx["quantity"]).round(2)
    mismatches = (rx["expected_total"] - rx["total_cost"]).abs() > 0.05
    print(f"Cost mismatches over $0.05: {mismatches.sum()}")

    payment_mismatch = (rx["total_cost"] - rx["insurance_covered"] - rx["out_of_pocket"]).abs() > 0.05
    print(f"Payment mismatches over $0.05: {payment_mismatch.sum()}")

if __name__ == "__main__":
    check_primary_key("patients", "patient_id")
    check_primary_key("doctors", "doctor_id")
    check_primary_key("pharmacies", "pharmacy_id")
    check_primary_key("drugs", "drug_id")
    check_primary_key("prescriptions", "prescription_id")
    check_primary_key("insurance_claims", "claim_id")

    for t in tables:
        check_nulls(t)

    check_foreign_key("prescriptions", "patient_id", "patients", "patient_id")
    check_foreign_key("prescriptions", "doctor_id", "doctors", "doctor_id")
    check_foreign_key("prescriptions", "pharmacy_id", "pharmacies", "pharmacy_id")
    check_foreign_key("prescriptions", "drug_id", "drugs", "drug_id")
    check_foreign_key("insurance_claims", "prescription_id", "prescriptions", "prescription_id")
    check_cost_logic()
