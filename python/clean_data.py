
from pathlib import Path
import pandas as pd

# ============================================================
# 1. PROJECT PATHS
# ============================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

RAW_FILE = PROJECT_DIR / "data" / "raw" / "DataCoSupplyChainDataset.csv"
OUTPUT_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_FILE = OUTPUT_DIR / "supply_chain_cleaned.csv"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 65)
print("SUPPLY CHAIN DATA CLEANING")
print("=" * 65)

# ============================================================
# 2. LOAD RAW DATA
# ============================================================

print("\nLoading raw dataset...")

df = pd.read_csv(
    RAW_FILE,
    encoding="latin-1",
    low_memory=False
)

print("Original rows:", len(df))
print("Original columns:", len(df.columns))

# ============================================================
# 3. REMOVE UNNECESSARY / SENSITIVE COLUMNS
# ============================================================

columns_to_remove = [
    # Customer personal information
    "Customer Email",
    "Customer Fname",
    "Customer Lname",
    "Customer Password",
    "Customer Street",
    "Customer Zipcode",
    "Customer City",
    "Customer State",
    "Customer Country",

    # Customer identifiers not required for current analysis
    "Customer Id",
    "Order Customer Id",

    # Sensitive or unnecessary location details
    "Latitude",
    "Longitude",

    # High-missing-value / unnecessary columns
    "Product Description",
    "Order Zipcode",
    "Product Image",

    # Duplicate profit column
    "Order Profit Per Order"
]

# Safety check: ensure all requested columns exist
missing_columns = [
    col for col in columns_to_remove
    if col not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Columns not found: {missing_columns}"
    )

df.drop(columns=columns_to_remove, inplace=True)

print("\nRemoved columns:", len(columns_to_remove))
print("Remaining columns:", len(df.columns))

# ============================================================
# 4. CONVERT DATE COLUMNS
# ============================================================

date_columns = [
    "order date (DateOrders)",
    "shipping date (DateOrders)"
]

for col in date_columns:
    df[col] = pd.to_datetime(
        df[col],
        format="mixed",
        errors="coerce"
    )

# Validate date conversion
for col in date_columns:
    invalid_dates = df[col].isna().sum()
    print(f"Invalid dates in {col}: {invalid_dates}")

if df[date_columns].isna().any().any():
    raise ValueError(
        "Invalid dates found. Review the raw dataset before continuing."
    )

# ============================================================
# 5. CREATE SHIPPING ANALYTICS COLUMNS
# ============================================================

df["Shipping Delay Days"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

df["Calculated Shipping Performance"] = (
    df["Shipping Delay Days"].apply(
        lambda x:
        "Late" if x > 0
        else "Early" if x < 0
        else "On Schedule"
    )
)

# ============================================================
# 6. CREATE ORDER DATE ANALYTICS COLUMNS
# ============================================================

order_date = df["order date (DateOrders)"]

df["Order Year"] = order_date.dt.year
df["Order Month"] = order_date.dt.month
df["Order Month Name"] = order_date.dt.month_name()
df["Order Year Month"] = order_date.dt.to_period("M").astype(str)

# ============================================================
# 7. CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 65)
print("MISSING VALUE REPORT")
print("=" * 65)

missing_report = (
    df.isnull()
    .sum()
    .reset_index()
)

missing_report.columns = ["Column", "Missing Values"]

missing_report = missing_report[
    missing_report["Missing Values"] > 0
]

if missing_report.empty:
    print("No missing values found.")
else:
    print(missing_report.to_string(index=False))

# ============================================================
# 8. CHECK DUPLICATES
# ============================================================

print("\n" + "=" * 65)
print("DUPLICATE CHECK")
print("=" * 65)

print(
    "Duplicate complete rows:",
    df.duplicated().sum()
)

print(
    "Duplicate Order Item Id:",
    df["Order Item Id"].duplicated().sum()
)

# ============================================================
# 9. VALIDATE DATASET
# ============================================================

print("\n" + "=" * 65)
print("FINAL DATA VALIDATION")
print("=" * 65)

print("Final rows:", len(df))
print("Final columns:", len(df.columns))

print("\nDate range:")
print("From:", df["order date (DateOrders)"].min())
print("To:", df["order date (DateOrders)"].max())

print("\nDelivery performance:")
print(
    df["Calculated Shipping Performance"]
    .value_counts()
)

print("\nOrder status:")
print(df["Order Status"].value_counts())

# Confirm no customer PII columns remain
sensitive_columns = [
    "Customer Email",
    "Customer Fname",
    "Customer Lname",
    "Customer Password",
    "Customer Street",
    "Customer Zipcode",
    "Customer City",
    "Customer State",
    "Customer Country",
    "Customer Id",
    "Order Customer Id"
]

remaining_sensitive = [
    col for col in sensitive_columns
    if col in df.columns
]

if remaining_sensitive:
    raise ValueError(
        f"Sensitive columns still present: {remaining_sensitive}"
    )

# ============================================================
# 10. SAVE CLEANED DATASET
# ============================================================

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig"
)

print("\n" + "=" * 65)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("=" * 65)

print("\nSaved file:")
print(OUTPUT_FILE)

print("\nFinal dataset shape:", df.shape)
print("Raw dataset remains unchanged.")
