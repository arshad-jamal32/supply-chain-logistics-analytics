from pathlib import Path
import pandas as pd

# =====================================================
# 1. PROJECT PATHS
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

RAW_DATA_DIR = PROJECT_DIR / "data" / "raw"

MAIN_FILE = RAW_DATA_DIR / "DataCoSupplyChainDataset.csv"
DESCRIPTION_FILE = RAW_DATA_DIR / "DescriptionDataCoSupplyChain.csv"


# =====================================================
# 2. CHECK FILE EXISTENCE
# =====================================================

print("=" * 65)
print("SUPPLY CHAIN DATASET VERIFICATION")
print("=" * 65)

for file in [MAIN_FILE, DESCRIPTION_FILE]:

    if not file.exists():
        raise FileNotFoundError(f"File not found: {file}")

    size_mb = file.stat().st_size / (1024 * 1024)

    print(f"\nFile: {file.name}")
    print(f"Size: {size_mb:.2f} MB")
    print("Status: Found")


# =====================================================
# 3. LOAD MAIN DATASET
# =====================================================

print("\n" + "=" * 65)
print("LOADING MAIN DATASET")
print("=" * 65)

df = pd.read_csv(MAIN_FILE, encoding="latin-1", low_memory=False)

print("\nMain dataset loaded successfully!")


# =====================================================
# 4. BASIC DATASET INFORMATION
# =====================================================

print("\n" + "=" * 65)
print("BASIC DATASET INFORMATION")
print("=" * 65)

print("\nTotal Rows:", df.shape[0])
print("Total Columns:", df.shape[1])

print("\nDataset Memory Usage:")
print(f"{df.memory_usage(deep=True).sum() / (1024**2):.2f} MB")


# =====================================================
# 5. COLUMN NAMES
# =====================================================

print("\n" + "=" * 65)
print("ALL COLUMN NAMES")
print("=" * 65)

for number, column in enumerate(df.columns, start=1):
    print(f"{number}. {column}")


# =====================================================
# 6. DATA TYPES
# =====================================================

print("\n" + "=" * 65)
print("COLUMN DATA TYPES")
print("=" * 65)

print(df.dtypes.to_string())


# =====================================================
# 7. MISSING VALUES
# =====================================================

print("\n" + "=" * 65)
print("MISSING VALUE ANALYSIS")
print("=" * 65)

missing = df.isnull().sum()

missing = missing[missing > 0].sort_values(ascending=False)

if missing.empty:
    print("\nNo missing values found.")
else:
    print("\nColumns containing missing values:")
    print(missing.to_string())


# =====================================================
# 8. DUPLICATE ANALYSIS
# =====================================================

print("\n" + "=" * 65)
print("DUPLICATE ANALYSIS")
print("=" * 65)

print("\nCompletely Duplicate Rows:", df.duplicated().sum())

if "Order Item Id" in df.columns:
    print("Duplicate Order Item IDs:", df["Order Item Id"].duplicated().sum())

if "Order Id" in df.columns:
    print("Unique Orders:", df["Order Id"].nunique())


# =====================================================
# 9. SAFE SAMPLE RECORDS
# =====================================================

print("\n" + "=" * 65)
print("SAMPLE DATA (SELECTED NON-PII COLUMNS)")
print("=" * 65)

safe_columns = [
    "Type",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Delivery Status",
    "Late_delivery_risk",
    "Market",
    "Order Region",
    "Order Status",
    "Shipping Mode",
    "Sales",
    "Order Item Quantity",
]

available_columns = [col for col in safe_columns if col in df.columns]

print(df[available_columns].head(5).to_string(index=False))


# =====================================================
# 10. IMPORTANT CATEGORY CHECKS
# =====================================================

print("\n" + "=" * 65)
print("IMPORTANT BUSINESS CATEGORIES")
print("=" * 65)

category_columns = ["Shipping Mode", "Delivery Status", "Order Status", "Market"]

for column in category_columns:

    if column in df.columns:

        print(f"\n{column}:")
        print(df[column].value_counts(dropna=False).to_string())


# =====================================================
# 11. NUMERICAL COLUMN SUMMARY
# =====================================================

print("\n" + "=" * 65)
print("NUMERICAL DATA SUMMARY")
print("=" * 65)

numeric_columns = [
    "Sales",
    "Order Item Quantity",
    "Order Item Profit Ratio",
    "Order Item Discount",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
]

available_numeric = [col for col in numeric_columns if col in df.columns]

print(df[available_numeric].describe().round(2).to_string())


# =====================================================
# 12. VERIFY DESCRIPTION FILE
# =====================================================

print("\n" + "=" * 65)
print("DATA DICTIONARY VERIFICATION")
print("=" * 65)

try:

    description_df = pd.read_csv(
        DESCRIPTION_FILE, encoding="latin-1", sep=None, engine="python"
    )

    print("\nData dictionary loaded successfully!")

    print("Rows:", description_df.shape[0])
    print("Columns:", description_df.shape[1])

    print("\nData dictionary preview:")

    print(description_df.head(10).to_string(index=False))

except Exception as error:

    print("\nData dictionary loading issue:")
    print(error)


# =====================================================
# 13. FINAL VERIFICATION
# =====================================================

print("\n" + "=" * 65)
print("VERIFICATION SUMMARY")
print("=" * 65)

print("Main dataset rows:", df.shape[0])
print("Main dataset columns:", df.shape[1])
print("Completely duplicate rows:", df.duplicated().sum())
print("Missing values:", df.isnull().sum().sum())

print("\nDataset verification completed!")

print("=" * 65)
