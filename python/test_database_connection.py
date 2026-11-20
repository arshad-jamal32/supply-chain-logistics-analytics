
import psycopg2
import os
from pathlib import Path
from dotenv import load_dotenv

# Project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# PostgreSQL Database Configuration
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "database": os.getenv("DB_NAME"),

    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT", "5432")
}

if not DB_CONFIG["password"]:
    raise ValueError("Database password not found in .env file.")

try:
    connection = psycopg2.connect(**DB_CONFIG)

    print("=" * 55)
    print("POSTGRESQL DATABASE CONNECTION")
    print("=" * 55)

    print("\nDatabase connection successful!")

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            COUNT(*) AS total_rows,
            COUNT(DISTINCT "Order Id") AS total_orders,
            ROUND(SUM("Sales")::numeric, 2) AS total_revenue
        FROM public.supply_chain;
    """)

    result = cursor.fetchone()

    print("\nDATABASE SUMMARY")
    print("-" * 55)
    print(f"Total Rows: {result[0]:,}")
    print(f"Total Orders: {result[1]:,}")
    print(f"Total Revenue: {result[2]:,.2f}")

    cursor.close()
    connection.close()

    print("\nDatabase connection closed.")

except Exception as error:
    print("\nDatabase connection failed!")
    print("Error:", error)
