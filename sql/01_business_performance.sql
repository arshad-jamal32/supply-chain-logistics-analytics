
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE & KPI ANALYSIS
-- DATABASE: supply_chain_analytics
-- TABLE: public.supply_chain
-- ============================================================


-- ============================================================
-- KPI 1: OVERALL BUSINESS PERFORMANCE
-- ============================================================

WITH order_level AS (

    SELECT
        "Order Id",

        SUM("Sales") AS order_revenue,

        SUM("Benefit per order") AS order_profit,

        SUM("Order Item Quantity") AS order_quantity

    FROM public.supply_chain

    GROUP BY "Order Id"

),

business_summary AS (

    SELECT

        SUM(order_revenue) AS total_revenue,

        SUM(order_profit) AS total_profit,

        COUNT(*) AS total_orders,

        SUM(order_quantity) AS total_quantity_sold,

        AVG(order_revenue) AS average_order_value,

        AVG(order_profit) AS average_profit_per_order

    FROM order_level

),

item_summary AS (

    SELECT
        COUNT(*) AS total_order_items

    FROM public.supply_chain

)

SELECT

    ROUND(bs.total_revenue, 2) AS total_revenue,

    ROUND(bs.total_profit, 2) AS total_profit,

    bs.total_orders,

    its.total_order_items,

    bs.total_quantity_sold,

    ROUND(bs.average_order_value, 2) AS average_order_value,

    ROUND(bs.average_profit_per_order, 2)
        AS average_profit_per_order,

    ROUND(
        (bs.total_profit / NULLIF(bs.total_revenue, 0)) * 100,
        2
    ) AS overall_profit_margin_percentage

FROM business_summary bs

CROSS JOIN item_summary its;


-- ============================================================
-- END OF PHASE 1 - QUERY 01
-- ============================================================
