
import psycopg2
import pandas as pd
import numpy as np
import os
from pathlib import Path
from dotenv import load_dotenv

# ============================================================
# SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
# PYTHON ANALYSIS - BUSINESS PERFORMANCE
# ============================================================

# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
REPORTS_DIR = BASE_DIR / "reports"

REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# PostgreSQL configuration
load_dotenv(BASE_DIR / ".env")

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432")
}

if not DB_CONFIG["password"]:
    raise ValueError("Database password not found in .env file.")


def load_data():

    print("\nConnecting to PostgreSQL...")

    connection = psycopg2.connect(**DB_CONFIG)

    query = """
        SELECT *
        FROM public.supply_chain;
    """

    df = pd.read_sql_query(query, connection)

    connection.close()

    print("Data loaded successfully!")
    print(f"Total rows: {len(df):,}")
    print(f"Total columns: {len(df.columns)}")

    return df


def overall_business_analysis(df):

    print("\n" + "=" * 65)
    print("1. OVERALL BUSINESS PERFORMANCE")
    print("=" * 65)

    total_revenue = df["Sales"].sum()
    total_profit = df["Benefit per order"].sum()

    total_orders = df["Order Id"].nunique()
    total_items = len(df)

    total_quantity = df["Order Item Quantity"].sum()

    # Order-level aggregation for correct AOV
    order_revenue = (
        df.groupby("Order Id")["Sales"]
        .sum()
    )

    average_order_value = order_revenue.mean()

    average_profit_per_order = (
        df.groupby("Order Id")["Benefit per order"]
        .sum()
        .mean()
    )

    profit_margin = (
        total_profit / total_revenue
    ) * 100

    kpis = {
        "Total Revenue": total_revenue,
        "Total Profit": total_profit,
        "Total Orders": total_orders,
        "Total Order Items": total_items,
        "Total Quantity Sold": total_quantity,
        "Average Order Value": average_order_value,
        "Average Profit Per Order": average_profit_per_order,
        "Profit Margin Percentage": profit_margin
    }

    for name, value in kpis.items():

        if isinstance(value, (int, np.integer)):
            print(f"{name}: {value:,}")

        else:
            print(f"{name}: {value:,.2f}")

    return kpis


def delivery_analysis(df):

    print("\n" + "=" * 65)
    print("2. DELIVERY PERFORMANCE ANALYSIS")
    print("=" * 65)

    delivery_summary = (
        df.groupby("Delivery Status")
        .agg(
            total_items=("Order Item Id", "count"),
            total_orders=("Order Id", "nunique"),
            average_shipping_days=(
                "Days for shipping (real)", "mean"
            ),
            average_scheduled_days=(
                "Days for shipment (scheduled)", "mean"
            ),
            average_delay_days=(
                "Shipping Delay Days", "mean"
            )
        )
        .reset_index()
    )

    delivery_summary = delivery_summary.round(2)

    print(delivery_summary.to_string(index=False))

    delivery_summary.to_csv(
        REPORTS_DIR / "delivery_performance.csv",
        index=False
    )

    return delivery_summary


def department_analysis(df):

    print("\n" + "=" * 65)
    print("3. DEPARTMENT PERFORMANCE ANALYSIS")
    print("=" * 65)

    department_summary = (
        df.groupby("Department Name")
        .agg(
            total_orders=("Order Id", "nunique"),
            total_items=("Order Item Id", "count"),
            total_revenue=("Sales", "sum"),
            total_profit=("Benefit per order", "sum")
        )
        .reset_index()
    )

    department_summary["revenue_share_percentage"] = (
        department_summary["total_revenue"]
        / department_summary["total_revenue"].sum()
    ) * 100

    department_summary["profit_margin_percentage"] = (
        department_summary["total_profit"]
        / department_summary["total_revenue"]
    ) * 100

    department_summary = department_summary.sort_values(
        by="total_revenue",
        ascending=False
    ).round(2)

    print(department_summary.to_string(index=False))

    department_summary.to_csv(
        REPORTS_DIR / "department_performance.csv",
        index=False
    )

    return department_summary


def market_analysis(df):

    print("\n" + "=" * 65)
    print("4. MARKET PERFORMANCE ANALYSIS")
    print("=" * 65)

    market_summary = (
        df.groupby("Market")
        .agg(
            total_orders=("Order Id", "nunique"),
            total_revenue=("Sales", "sum"),
            total_profit=("Benefit per order", "sum")
        )
        .reset_index()
    )

    market_summary["profit_margin_percentage"] = (
        market_summary["total_profit"]
        / market_summary["total_revenue"]
    ) * 100

    market_summary = market_summary.sort_values(
        by="total_revenue",
        ascending=False
    ).round(2)

    print(market_summary.to_string(index=False))

    market_summary.to_csv(
        REPORTS_DIR / "market_performance.csv",
        index=False
    )

    return market_summary


def customer_segment_analysis(df):

    print("\n" + "=" * 65)
    print("5. CUSTOMER SEGMENT ANALYSIS")
    print("=" * 65)

    segment_summary = (
        df.groupby("Customer Segment")
        .agg(
            total_orders=("Order Id", "nunique"),
            total_revenue=("Sales", "sum"),
            total_profit=("Benefit per order", "sum")
        )
        .reset_index()
    )

    segment_summary["revenue_share_percentage"] = (
        segment_summary["total_revenue"]
        / segment_summary["total_revenue"].sum()
    ) * 100

    segment_summary["profit_margin_percentage"] = (
        segment_summary["total_profit"]
        / segment_summary["total_revenue"]
    ) * 100

    segment_summary = segment_summary.sort_values(
        by="total_revenue",
        ascending=False
    ).round(2)

    print(segment_summary.to_string(index=False))

    segment_summary.to_csv(
        REPORTS_DIR / "customer_segment_performance.csv",
        index=False
    )

    return segment_summary


def main():

    print("=" * 65)
    print("SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS")
    print("PYTHON BUSINESS ANALYSIS")
    print("=" * 65)

    df = load_data()

    # Run all business analyses
    kpis = overall_business_analysis(df)

    delivery_analysis(df)

    department_analysis(df)

    market_analysis(df)

    customer_segment_analysis(df)

    print("\n" + "=" * 65)
    print("PYTHON BUSINESS ANALYSIS COMPLETED SUCCESSFULLY!")
    print("=" * 65)

    print("\nReports saved inside:")
    print(REPORTS_DIR)


if __name__ == "__main__":
    main()
