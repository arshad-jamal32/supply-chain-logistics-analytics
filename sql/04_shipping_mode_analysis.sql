
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 04: SHIPPING MODE PERFORMANCE ANALYSIS
-- ============================================================

WITH order_level AS (

    SELECT
        "Order Id",
        "Shipping Mode",
        "Delivery Status",

        SUM("Sales") AS order_revenue,

        SUM("Benefit per order") AS order_profit,

        COUNT(*) AS total_order_items,

        MAX("Days for shipping (real)") AS actual_shipping_days,

        MAX("Days for shipment (scheduled)") AS scheduled_shipping_days

    FROM public.supply_chain

    GROUP BY
        "Order Id",
        "Shipping Mode",
        "Delivery Status"
),

shipping_summary AS (

    SELECT
        "Shipping Mode",

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
        ) AS canceled_orders,

        AVG(actual_shipping_days) AS avg_actual_shipping_days,

        AVG(scheduled_shipping_days) AS avg_scheduled_shipping_days

    FROM order_level

    GROUP BY "Shipping Mode"
)

SELECT

    "Shipping Mode",

    total_orders,

    total_order_items,

    late_orders,

    on_time_orders,

    advance_orders,

    canceled_orders,

    ROUND(
        late_orders * 100.0 /
        NULLIF(total_orders, 0),
        2
    ) AS late_delivery_percentage,

    ROUND(total_revenue, 2) AS total_revenue,

    ROUND(total_profit, 2) AS total_profit,

    ROUND(avg_actual_shipping_days, 2)
        AS avg_actual_shipping_days,

    ROUND(avg_scheduled_shipping_days, 2)
        AS avg_scheduled_shipping_days

FROM shipping_summary

ORDER BY late_delivery_percentage DESC;
