
from pathlib import Path
import pandas as pd

# =====================================================
# 1. PROJECT PATHS
# =====================================================

PROJECT_DIR = Path(__file__).resolve().parents[1]

MAIN_FILE = (
    PROJECT_DIR
    / "data"
    / "raw"
    / "DataCoSupplyChainDataset.csv"
)

print("=" * 75)
print("SUPPLY CHAIN - ADVANCED DATA PROFILING")
print("=" * 75)


# =====================================================
# 2. LOAD DATASET
# =====================================================

df = pd.read_csv(
    MAIN_FILE,
    encoding="latin-1",
    low_memory=False
)

print("\nDataset loaded successfully!")
print("Total records:", len(df))


# =====================================================
# 3. DATE RANGE ANALYSIS
# =====================================================

print("\n" + "=" * 75)
print("1. DATE RANGE ANALYSIS")
print("=" * 75)

date_columns = [
    "order date (DateOrders)",
    "shipping date (DateOrders)"
]

for column in date_columns:

    df[column] = pd.to_datetime(
        df[column],
        format="mixed",
        errors="coerce"
    )

    print(f"\n{column}")

    print("Minimum date:", df[column].min())
    print("Maximum date:", df[column].max())

    print(
        "Invalid or missing dates:",
        df[column].isna().sum()
    )


# =====================================================
# 4. DELIVERY DAYS ANALYSIS
# =====================================================

print("\n" + "=" * 75)
print("2. DELIVERY DAYS ANALYSIS")
print("=" * 75)

print("\nActual shipping days:")

print(
    df["Days for shipping (real)"]
    .describe()
    .round(2)
)

print("\nScheduled shipping days:")

print(
    df["Days for shipment (scheduled)"]
    .describe()
    .round(2)
)

df["Shipping Delay Days"] = (
    df["Days for shipping (real)"]
    - df["Days for shipment (scheduled)"]
)

print("\nShipping delay days:")

print(
    df["Shipping Delay Days"]
    .describe()
    .round(2)
)

print("\nShipping delay classification:")

print(
    df["Shipping Delay Days"]
    .apply(
        lambda x:
        "Late" if x > 0
        else "On Schedule" if x == 0
        else "Early"
    )
    .value_counts()
)


# =====================================================
# 5. LATE DELIVERY RISK VALIDATION
# =====================================================

print("\n" + "=" * 75)
print("3. LATE DELIVERY RISK VALIDATION")
print("=" * 75)

print("\nLate delivery risk distribution:")

print(
    df["Late_delivery_risk"]
    .value_counts(dropna=False)
)

print("\nDelivery status distribution:")

print(
    df["Delivery Status"]
    .value_counts(dropna=False)
)

print("\nLate Delivery Risk vs Delivery Status:")

risk_status_table = pd.crosstab(
    df["Delivery Status"],
    df["Late_delivery_risk"],
    margins=True
)

print(risk_status_table)

print("\nLate delivery risk vs shipping delay:")

print(
    pd.crosstab(
        df["Late_delivery_risk"],
        df["Shipping Delay Days"] > 0,
        margins=True
    )
)


# =====================================================
# 6. PRODUCT AND CATEGORY ANALYSIS
# =====================================================

print("\n" + "=" * 75)
print("4. PRODUCT AND CATEGORY ANALYSIS")
print("=" * 75)

print(
    "\nUnique products:",
    df["Product Name"].nunique()
)

print(
    "Unique categories:",
    df["Category Name"].nunique()
)

print(
    "Unique departments:",
    df["Department Name"].nunique()
)

print("\nProduct categories:")

print(
    df["Category Name"]
    .value_counts()
    .to_string()
)

print("\nTop 10 products by sales:")

top_products = (
    df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

print(top_products.round(2).to_string())


# =====================================================
# 7. PROFITABILITY ANALYSIS
# =====================================================

print("\n" + "=" * 75)
print("5. PROFITABILITY ANALYSIS")
print("=" * 75)

profit_columns = [
    "Order Item Profit Ratio",
    "Benefit per order",
    "Order Profit Per Order"
]

for column in profit_columns:

    print(f"\n{column}")

    print(
        df[column]
        .describe()
        .round(3)
    )

print("\nNegative profit ratio records:")

negative_profit = df[
    df["Order Item Profit Ratio"] < 0
]

print(
    "Total records:",
    len(negative_profit)
)

print(
    "Percentage:",
    round(
        len(negative_profit) / len(df) * 100,
        2
    ),
    "%"
)

print("\nNegative profit ratio by category:")

if not negative_profit.empty:

    print(
        negative_profit
        .groupby("Category Name")
        .size()
        .sort_values(ascending=False)
        .head(10)
    )


# =====================================================
# 8. NUMERICAL VALUE VALIDATION
# =====================================================

print("\n" + "=" * 75)
print("6. NUMERICAL VALUE VALIDATION")
print("=" * 75)

numeric_checks = [
    "Sales",
    "Order Item Quantity",
    "Order Item Discount",
    "Order Item Product Price",
    "Product Price",
    "Days for shipping (real)",
    "Days for shipment (scheduled)"
]

for column in numeric_checks:

    print(f"\n{column}")

    print("Minimum:", df[column].min())
    print("Maximum:", df[column].max())

    print("Zero values:", (df[column] == 0).sum())

    print("Negative values:", (df[column] < 0).sum())


# =====================================================
# 9. ORDER STATUS AND CANCELLATION ANALYSIS
# =====================================================

print("\n" + "=" * 75)
print("7. ORDER STATUS ANALYSIS")
print("=" * 75)

print("\nOrder status distribution:")

print(
    df["Order Status"]
    .value_counts(dropna=False)
)

print("\nOrder status vs delivery status:")

print(
    pd.crosstab(
        df["Order Status"],
        df["Delivery Status"],
        margins=True
    )
)

print("\nCancellation records:")

print(
    "CANCELED order status:",
    (df["Order Status"] == "CANCELED").sum()
)

print(
    "Shipping canceled delivery status:",
    (df["Delivery Status"] == "Shipping canceled").sum()
)


# =====================================================
# 10. BUSINESS DATA CONSISTENCY CHECKS
# =====================================================

print("\n" + "=" * 75)
print("8. BUSINESS DATA CONSISTENCY CHECKS")
print("=" * 75)

# Check whether shipping date is before order date

invalid_date_sequence = df[
    df["shipping date (DateOrders)"]
    < df["order date (DateOrders)"]
]

print(
    "\nShipping date before order date:",
    len(invalid_date_sequence)
)

# Check missing Order IDs

print(
    "Missing Order IDs:",
    df["Order Id"].isna().sum()
)

# Check missing Order Item IDs

print(
    "Missing Order Item IDs:",
    df["Order Item Id"].isna().sum()
)

# Check negative or zero quantities

print(
    "Zero quantity records:",
    (df["Order Item Quantity"] == 0).sum()
)

print(
    "Negative quantity records:",
    (df["Order Item Quantity"] < 0).sum()
)

# Check invalid late delivery risk values

print(
    "Unexpected late delivery risk values:",
    (~df["Late_delivery_risk"].isin([0, 1])).sum()
)


# =====================================================
# 11. REGIONAL PERFORMANCE OVERVIEW
# =====================================================

print("\n" + "=" * 75)
print("9. REGIONAL PERFORMANCE OVERVIEW")
print("=" * 75)

regional_summary = (
    df.groupby("Order Region")
    .agg(
        Total_Records=("Order Id", "size"),
        Unique_Orders=("Order Id", "nunique"),
        Total_Sales=("Sales", "sum"),
        Average_Sales=("Sales", "mean"),
        Late_Delivery_Records=(
            "Late_delivery_risk",
            "sum"
        )
    )
    .sort_values(
        "Total_Sales",
        ascending=False
    )
)

regional_summary["Late_Risk_Percentage"] = (
    regional_summary["Late_Delivery_Records"]
    / regional_summary["Total_Records"]
    * 100
)

print(
    regional_summary.round(2).to_string()
)


# =====================================================
# 12. FINAL PROFILING SUMMARY
# =====================================================

print("\n" + "=" * 75)
print("FINAL PROFILING SUMMARY")
print("=" * 75)

print("Total records:", len(df))

print(
    "Date parsing errors:",
    df[date_columns].isna().sum().sum()
)

print(
    "Negative profit ratio records:",
    (df["Order Item Profit Ratio"] < 0).sum()
)

print(
    "Late delivery risk records:",
    (df["Late_delivery_risk"] == 1).sum()
)

print(
    "Unique orders:",
    df["Order Id"].nunique()
)

print("\nADVANCED DATA PROFILING COMPLETED!")

print("=" * 75)
