
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 03: DELIVERY PERFORMANCE ANALYSIS
-- ============================================================

WITH order_level AS (

    SELECT
        "Order Id",
        "Delivery Status",

        SUM("Sales") AS order_revenue,

        SUM("Benefit per order") AS order_profit,

        COUNT(*) AS total_order_items,

        MAX("Days for shipping (real)") AS actual_shipping_days,

        MAX("Days for shipment (scheduled)") AS scheduled_shipping_days,

        MAX("Shipping Delay Days") AS shipping_delay_days

    FROM public.supply_chain

    GROUP BY
        "Order Id",
        "Delivery Status"
),

delivery_summary AS (

    SELECT
        "Delivery Status",

        COUNT(*) AS total_orders,

        SUM(total_order_items) AS total_order_items,

        SUM(order_revenue) AS total_revenue,

        SUM(order_profit) AS total_profit,

        AVG(actual_shipping_days) AS avg_actual_shipping_days,

        AVG(scheduled_shipping_days) AS avg_scheduled_shipping_days,

        AVG(shipping_delay_days) AS avg_shipping_delay_days

    FROM order_level

    GROUP BY "Delivery Status"
)

SELECT

    "Delivery Status",

    total_orders,

    total_order_items,

    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(
        total_orders * 100.0 /
        NULLIF(SUM(total_orders) OVER (), 0),
        2
    ) AS order_percentage,

    ROUND(
        total_revenue * 100.0 /
        NULLIF(SUM(total_revenue) OVER (), 0),
        2
    ) AS revenue_contribution_percentage,

    ROUND(avg_actual_shipping_days, 2)
        AS avg_actual_shipping_days,

    ROUND(avg_scheduled_shipping_days, 2)
        AS avg_scheduled_shipping_days,

    ROUND(avg_shipping_delay_days, 2)
        AS avg_shipping_delay_days

FROM delivery_summary

ORDER BY total_orders DESC;
