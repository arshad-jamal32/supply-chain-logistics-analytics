
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 07: MONTHLY SALES & PROFIT TREND ANALYSIS
-- ============================================================

WITH order_level AS (

    SELECT
        "Order Id",

        DATE_TRUNC(
            'month',
            "order date (DateOrders)"
        ) AS order_month,

        "Delivery Status",

        SUM("Sales") AS order_revenue,

        SUM("Benefit per order") AS order_profit,

        SUM("Order Item Quantity") AS total_quantity,

        COUNT(*) AS total_order_items

    FROM public.supply_chain

    GROUP BY
        "Order Id",
        DATE_TRUNC(
            'month',
            "order date (DateOrders)"
        ),
        "Delivery Status"
),

monthly_summary AS (

    SELECT

        order_month,

        COUNT(*) AS total_orders,

        SUM(total_order_items) AS total_order_items,

        SUM(total_quantity) AS total_quantity_sold,

        SUM(order_revenue) AS total_revenue,

        SUM(order_profit) AS total_profit,

        AVG(order_revenue) AS average_order_value,

        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Late delivery'
        ) AS late_orders

    FROM order_level

    GROUP BY order_month
)

SELECT

    TO_CHAR(order_month, 'YYYY-MM') AS order_month,

    total_orders,

    total_order_items,

    total_quantity_sold,

    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(average_order_value, 2) AS average_order_value,

    ROUND(
        total_profit * 100.0 /
        NULLIF(total_revenue, 0),
        2
    ) AS profit_margin_percentage,

    late_orders,

    ROUND(
        late_orders * 100.0 /
        NULLIF(total_orders, 0),
        2
    ) AS late_delivery_percentage

FROM monthly_summary

ORDER BY order_month;
