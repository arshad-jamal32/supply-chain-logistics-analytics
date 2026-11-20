
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 05: MARKET-WISE PERFORMANCE ANALYSIS
-- ============================================================

WITH order_level AS (

    SELECT
        "Order Id",
        "Market",
        "Delivery Status",

        SUM("Sales") AS order_revenue,

        SUM("Benefit per order") AS order_profit,

        COUNT(*) AS total_order_items

    FROM public.supply_chain

    GROUP BY
        "Order Id",
        "Market",
        "Delivery Status"
),

market_summary AS (

    SELECT
        "Market",

        COUNT(*) AS total_orders,

        SUM(total_order_items) AS total_order_items,

        SUM(order_revenue) AS total_revenue,

        SUM(order_profit) AS total_profit,

        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Late delivery'
        ) AS late_orders,

        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Shipping on time'
        ) AS on_time_orders,

        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Advance shipping'
        ) AS advance_orders,

        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Shipping canceled'
        ) AS canceled_orders

    FROM order_level

    GROUP BY "Market"
)

SELECT

    "Market",

    total_orders,

    total_order_items,

    late_orders,

    on_time_orders,

    advance_orders,

    canceled_orders,

    ROUND(
        total_revenue, 2
    ) AS total_revenue,

    ROUND(
        total_profit, 2
    ) AS total_profit,

    ROUND(
        total_revenue * 100.0 /
        NULLIF(SUM(total_revenue) OVER (), 0),
        2
    ) AS revenue_contribution_percentage,

    ROUND(
        late_orders * 100.0 /
        NULLIF(total_orders, 0),
        2
    ) AS late_delivery_percentage,

    ROUND(
        total_profit * 100.0 /
        NULLIF(total_revenue, 0),
        2
    ) AS profit_margin_percentage

FROM market_summary

ORDER BY total_revenue DESC;
