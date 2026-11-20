
from pathlib import Path
import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_DIR / "data" / "raw" / "DataCoSupplyChainDataset.csv"
CLEAN_FILE = PROJECT_DIR / "data" / "processed" / "supply_chain_cleaned.csv"

print("=" * 60)
print("CLEANED DATASET VALIDATION")
print("=" * 60)

raw = pd.read_csv(
    RAW_FILE,
    encoding="latin-1",
    low_memory=False
)

clean = pd.read_csv(
    CLEAN_FILE,
    encoding="utf-8-sig",
    low_memory=False
)

print("\n1. ROW COUNT COMPARISON")
print("Raw rows:", len(raw))
print("Cleaned rows:", len(clean))
print("Rows preserved:", len(raw) == len(clean))

print("\n2. ORDER ITEM ID VALIDATION")
print(
    "Unique Order Item IDs:",
    clean["Order Item Id"].nunique()
)
print(
    "Duplicate Order Item IDs:",
    clean["Order Item Id"].duplicated().sum()
)

print("\n3. DATE VALIDATION")
print("Order date:", clean["order date (DateOrders)"].min(),
      "to", clean["order date (DateOrders)"].max())

print("\n4. CALCULATED COLUMN VALIDATION")
print(clean[
    [
        "Shipping Delay Days",
        "Calculated Shipping Performance",
        "Order Year",
        "Order Month",
        "Order Month Name",
        "Order Year Month"
    ]
].head(5).to_string(index=False))

print("\n5. CUSTOMER PII CHECK")
pii_columns = [
    "Customer Email",
    "Customer Fname",
    "Customer Lname",
    "Customer Password",
    "Customer Street",
    "Customer Zipcode"
]

print(
    "PII columns remaining:",
    [c for c in pii_columns if c in clean.columns]
)

print("\n6. FINAL DATASET")
print("Shape:", clean.shape)
print("Missing values:", clean.isnull().sum().sum())

print("\nVALIDATION COMPLETED!")
print("=" * 60)
