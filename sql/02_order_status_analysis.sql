
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 02: ORDER STATUS ANALYSIS
-- ============================================================

WITH order_level AS (

    SELECT
        "Order Id",
        "Order Status",

        SUM("Sales") AS order_revenue,

        SUM("Benefit per order") AS order_profit,

        SUM("Order Item Quantity") AS order_quantity,

        COUNT(*) AS total_order_items

    FROM public.supply_chain

    GROUP BY
        "Order Id",
        "Order Status"
),

status_summary AS (

    SELECT
        "Order Status",

        COUNT(*) AS total_orders,

        SUM(total_order_items) AS total_order_items,

        SUM(order_quantity) AS total_quantity,

        SUM(order_revenue) AS total_revenue,

        SUM(order_profit) AS total_profit

    FROM order_level

    GROUP BY "Order Status"
)

SELECT

    "Order Status",

    total_orders,

    total_order_items,

    total_quantity,

    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_revenue * 100.0 /
        NULLIF(SUM(total_revenue) OVER (), 0),
        2
    ) AS revenue_contribution_percentage,

    ROUND(
        total_profit * 100.0 /
        NULLIF(SUM(total_profit) OVER (), 0),
        2
    ) AS profit_contribution_percentage,

    ROUND(
        total_profit * 100.0 /
        NULLIF(total_revenue, 0),
        2
    ) AS profit_margin_percentage

FROM status_summary

ORDER BY total_revenue DESC;


-- ============================================================
-- END OF QUERY 02
-- ============================================================
