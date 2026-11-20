
import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from pathlib import Path
from dotenv import load_dotenv

# --------------------------------------------------
# PROJECT DIRECTORY AND ENVIRONMENT VARIABLES
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")

# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432")
}

if not DB_CONFIG["password"]:
    raise ValueError("Database password not found in .env file.")

print("=" * 65)
print("SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS")
print("PYTHON VISUALIZATION")
print("=" * 65)

# --------------------------------------------------
# DATABASE CONNECTION
# --------------------------------------------------

print("\nConnecting to PostgreSQL...")

connection = psycopg2.connect(**DB_CONFIG)

print("Database connected successfully!")

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

query = '''
SELECT
    "Order Id",
    "Order Item Id",
    "Sales",
    "Benefit per order",
    "Order Item Quantity",
    "Order Item Discount",
    "Order Item Profit Ratio",
    "Delivery Status",
    "Department Name",
    "Category Name",
    "Market",
    "Customer Segment",
    "Shipping Mode",
    "Order Status",
    "Order Region",
    "order date (DateOrders)",
    "Shipping Delay Days"
FROM public.supply_chain;
'''

df = pd.read_sql_query(query, connection)

print("Data loaded successfully!")
print(f"Total rows: {len(df):,}")

connection.close()

# --------------------------------------------------
# CHART FOLDER
# --------------------------------------------------

chart_path = BASE_DIR / "reports" / "charts"
chart_path.mkdir(parents=True, exist_ok=True)

sns.set_theme(style="whitegrid")

# --------------------------------------------------
# 01. MONTHLY REVENUE TREND
# --------------------------------------------------

monthly = (
    df.groupby(df["order date (DateOrders)"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly["order date (DateOrders)"] = (
    monthly["order date (DateOrders)"].dt.to_timestamp()
)

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=monthly,
    x="order date (DateOrders)",
    y="Sales",
    marker="o"
)
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(chart_path / "01_monthly_revenue_trend.png", dpi=300)
plt.close()

print("01. Monthly Revenue Trend created!")

# --------------------------------------------------
# 02. MONTHLY PROFIT TREND
# --------------------------------------------------

monthly_profit = (
    df.groupby(df["order date (DateOrders)"].dt.to_period("M"))[
        "Benefit per order"
    ].sum().reset_index()
)

monthly_profit["order date (DateOrders)"] = (
    monthly_profit["order date (DateOrders)"].dt.to_timestamp()
)

plt.figure(figsize=(14, 6))
sns.lineplot(
    data=monthly_profit,
    x="order date (DateOrders)",
    y="Benefit per order",
    marker="o"
)
plt.title("Monthly Profit Trend")
plt.xlabel("Month")
plt.ylabel("Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(chart_path / "02_monthly_profit_trend.png", dpi=300)
plt.close()

print("02. Monthly Profit Trend created!")

# --------------------------------------------------
# 03. DELIVERY STATUS ANALYSIS
# --------------------------------------------------

delivery = df["Delivery Status"].value_counts().reset_index()
delivery.columns = ["Delivery Status", "Items"]

plt.figure(figsize=(10, 6))
sns.barplot(data=delivery, x="Delivery Status", y="Items")
plt.title("Delivery Status Analysis")
plt.xlabel("Delivery Status")
plt.ylabel("Order Items")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(chart_path / "03_delivery_status_analysis.png", dpi=300)
plt.close()

print("03. Delivery Status Analysis created!")

# --------------------------------------------------
# 04. DEPARTMENT REVENUE
# --------------------------------------------------

department = (
    df.groupby("Department Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(12, 7))
sns.barplot(data=department, x="Sales", y="Department Name")
plt.title("Department-wise Revenue")
plt.xlabel("Revenue")
plt.ylabel("Department")
plt.tight_layout()
plt.savefig(chart_path / "04_department_revenue.png", dpi=300)
plt.close()

print("04. Department Revenue Analysis created!")

# --------------------------------------------------
# 05. MARKET PERFORMANCE
# --------------------------------------------------

market = (
    df.groupby("Market")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(10, 6))
sns.barplot(data=market, x="Market", y="Sales")
plt.title("Market-wise Revenue")
plt.xlabel("Market")
plt.ylabel("Revenue")
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig(chart_path / "05_market_performance.png", dpi=300)
plt.close()

print("05. Market Performance created!")

# --------------------------------------------------
# 06. CUSTOMER SEGMENT REVENUE
# --------------------------------------------------

segment = (
    df.groupby("Customer Segment")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .reset_index()
)

plt.figure(figsize=(9, 6))
sns.barplot(data=segment, x="Customer Segment", y="Sales")
plt.title("Customer Segment Revenue")
plt.xlabel("Customer Segment")
plt.ylabel("Revenue")
plt.tight_layout()
plt.savefig(chart_path / "06_customer_segment_revenue.png", dpi=300)
plt.close()

print("06. Customer Segment Revenue created!")

# --------------------------------------------------
# 07. SHIPPING MODE PERFORMANCE
# --------------------------------------------------

shipping = (
    df.groupby("Shipping Mode")
    .agg(
        Total_Items=("Order Item Id", "count"),
        Late_Items=("Delivery Status",
                    lambda x: (x == "Late delivery").sum())
    )
    .reset_index()
)

shipping["Late Delivery Rate"] = (
    shipping["Late_Items"] / shipping["Total_Items"] * 100
)

plt.figure(figsize=(10, 6))
sns.barplot(
    data=shipping,
    x="Shipping Mode",
    y="Late Delivery Rate"
)
plt.title("Late Delivery Rate by Shipping Mode")
plt.xlabel("Shipping Mode")
plt.ylabel("Late Delivery Rate (%)")
plt.tight_layout()
plt.savefig(chart_path / "07_shipping_mode_performance.png", dpi=300)
plt.close()

print("07. Shipping Mode Performance created!")

# --------------------------------------------------
# 08. DISCOUNT VS PROFITABILITY
# --------------------------------------------------

discount = (
    df.groupby("Order Item Discount")
    .agg(
        Revenue=("Sales", "sum"),
        Profit=("Benefit per order", "sum")
    )
    .reset_index()
)

discount["Profit Margin"] = (
    discount["Profit"] / discount["Revenue"] * 100
)

plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=discount,
    x="Order Item Discount",
    y="Profit Margin",
    alpha=0.6
)
plt.title("Discount vs Profitability")
plt.xlabel("Order Item Discount")
plt.ylabel("Profit Margin (%)")
plt.tight_layout()
plt.savefig(chart_path / "08_discount_vs_profitability.png", dpi=300)
plt.close()

print("08. Discount vs Profitability created!")

# --------------------------------------------------
# 09. PRODUCT CATEGORY PERFORMANCE
# --------------------------------------------------

category = (
    df.groupby("Category Name")["Sales"]
    .sum()
    .nlargest(15)
    .sort_values()
    .reset_index()
)

plt.figure(figsize=(12, 8))
sns.barplot(
    data=category,
    x="Sales",
    y="Category Name"
)
plt.title("Top 15 Product Categories by Revenue")
plt.xlabel("Revenue")
plt.ylabel("Product Category")
plt.tight_layout()
plt.savefig(chart_path / "09_product_category_performance.png", dpi=300)
plt.close()

print("09. Product Category Performance created!")

# --------------------------------------------------
# 10. ORDER STATUS ANALYSIS
# --------------------------------------------------

status = (
    df.groupby("Order Status")["Order Id"]
    .nunique()
    .sort_values(ascending=False)
    .reset_index()
)

status.columns = ["Order Status", "Total Orders"]

plt.figure(figsize=(12, 7))
sns.barplot(
    data=status,
    x="Total Orders",
    y="Order Status"
)
plt.title("Order Status Analysis")
plt.xlabel("Distinct Orders")
plt.ylabel("Order Status")
plt.tight_layout()
plt.savefig(chart_path / "10_order_status_analysis.png", dpi=300)
plt.close()

print("10. Order Status Analysis created!")

# --------------------------------------------------
# 11. REGIONAL DELIVERY PERFORMANCE
# --------------------------------------------------

regional = df[df["Delivery Status"] != "Shipping canceled"].copy()

regional = (
    regional.groupby("Order Region")
    .agg(
        Total_Items=("Order Item Id", "count"),
        Late_Items=("Delivery Status",
                    lambda x: (x == "Late delivery").sum())
    )
    .reset_index()
)

regional["Late Delivery Rate"] = (
    regional["Late_Items"] / regional["Total_Items"] * 100
)

regional = regional.sort_values(
    "Late Delivery Rate",
    ascending=False
)

plt.figure(figsize=(13, 9))
sns.barplot(
    data=regional,
    x="Late Delivery Rate",
    y="Order Region"
)
plt.title("Regional Late Delivery Performance")
plt.xlabel("Late Delivery Rate (%)")
plt.ylabel("Order Region")
plt.tight_layout()
plt.savefig(chart_path / "11_regional_delivery_performance.png", dpi=300)
plt.close()

print("11. Regional Delivery Performance created!")

# --------------------------------------------------
# COMPLETION
# --------------------------------------------------

print("\n" + "=" * 65)
print("ALL 11 VISUALIZATIONS CREATED SUCCESSFULLY!")
print("=" * 65)

print(f"\nCharts saved inside:\n{chart_path}")
