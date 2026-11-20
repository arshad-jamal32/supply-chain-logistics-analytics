
from pathlib import Path
import pandas as pd

# =====================================================
# 1. LOAD DATA
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "DataCoSupplyChainDataset.csv"
)

df = pd.read_csv(
    FILE,
    encoding="latin-1",
    low_memory=False
)

print("=" * 70)
print("DATA QUALITY INVESTIGATION")
print("=" * 70)


# =====================================================
# 2. INVESTIGATE SHIPPING DELAY MISMATCH
# =====================================================

df["Shipping Delay Days"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

df["Calculated Delivery"] = df[
    "Shipping Delay Days"
].apply(
    lambda x: "Late" if x > 0
    else "On Schedule" if x == 0
    else "Early"
)

print("\n1. DELIVERY STATUS VS CALCULATED SHIPPING DELAY")

print(
    pd.crosstab(
        df["Delivery Status"],
        df["Calculated Delivery"],
        margins=True
    )
)

print("\n2. DELIVERY RISK VS CALCULATED SHIPPING DELAY")

print(
    pd.crosstab(
        df["Late_delivery_risk"],
        df["Calculated Delivery"],
        margins=True
    )
)


# =====================================================
# 3. INVESTIGATE THE 4,423 MISMATCH RECORDS
# =====================================================

mismatch = df[
    (df["Shipping Delay Days"] > 0)
    & (df["Late_delivery_risk"] == 0)
]

print("\n3. MISMATCH RECORDS")

print("Total mismatch records:", len(mismatch))

print("\nMismatch by delivery status:")

print(
    mismatch["Delivery Status"]
    .value_counts(dropna=False)
)

print("\nMismatch by shipping mode:")

print(
    mismatch["Shipping Mode"]
    .value_counts(dropna=False)
)

print("\nMismatch by order status:")

print(
    mismatch["Order Status"]
    .value_counts(dropna=False)
)


# =====================================================
# 4. SAFE SAMPLE OF MISMATCH RECORDS
# =====================================================

safe_columns = [
    "Order Id",
    "Order Item Id",
    "Days for shipping (real)",
    "Days for shipment (scheduled)",
    "Shipping Delay Days",
    "Late_delivery_risk",
    "Delivery Status",
    "Shipping Mode",
    "Order Status"
]

print("\n4. SAMPLE MISMATCH RECORDS")

print(
    mismatch[safe_columns]
    .head(10)
    .to_string(index=False)
)


# =====================================================
# 5. VERIFY ACTUAL DATE DIFFERENCE
# =====================================================

df["order date (DateOrders)"] = pd.to_datetime(
    df["order date (DateOrders)"],
    format="mixed"
)

df["shipping date (DateOrders)"] = pd.to_datetime(
    df["shipping date (DateOrders)"],
    format="mixed"
)

df["Calendar Shipping Days"] = (
    df["shipping date (DateOrders)"]
    - df["order date (DateOrders)"]
).dt.days

print("\n5. DATE DIFFERENCE VS ACTUAL SHIPPING DAYS")

print(
    pd.crosstab(
        df["Days for shipping (real)"],
        df["Calendar Shipping Days"],
        margins=True
    )
)

print(
    "\nRecords where date difference differs from actual shipping days:",
    (
        df["Days for shipping (real)"]
        != df["Calendar Shipping Days"]
    ).sum()
)


# =====================================================
# 6. VERIFY PROFIT COLUMNS
# =====================================================

print("\n6. PROFIT COLUMN CONSISTENCY")

print(
    "Benefit and Order Profit Per Order identical:",
    df["Benefit per order"].equals(
        df["Order Profit Per Order"]
    )
)

print(
    "Profit ratio missing values:",
    df["Order Item Profit Ratio"].isna().sum()
)


# =====================================================
# 7. FINAL SUMMARY
# =====================================================

print("\n" + "=" * 70)
print("INVESTIGATION SUMMARY")
print("=" * 70)

print("Total records:", len(df))
print("Mismatch records:", len(mismatch))

print(
    "Shipping canceled mismatch records:",
    (
        mismatch["Delivery Status"]
        == "Shipping canceled"
    ).sum()
)

print(
    "Date difference mismatch records:",
    (
        df["Days for shipping (real)"]
        != df["Calendar Shipping Days"]
    ).sum()
)

print("\nINVESTIGATION COMPLETED!")
print("=" * 70)
