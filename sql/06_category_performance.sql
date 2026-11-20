
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 06: PRODUCT CATEGORY PERFORMANCE ANALYSIS
-- ============================================================

WITH category_order AS (

    SELECT
        "Order Id",
        "Department Name",
        "Category Name",
        "Delivery Status",

        SUM("Sales") AS order_revenue,

        SUM("Benefit per order") AS order_profit,

        SUM("Order Item Quantity") AS total_quantity,

        COUNT(*) AS total_order_items

    FROM public.supply_chain

    GROUP BY
        "Order Id",
        "Department Name",
        "Category Name",
        "Delivery Status"
),

category_summary AS (

    SELECT
        "Department Name",
        "Category Name",

        COUNT(*) AS total_orders,

        SUM(total_order_items) AS total_order_items,

        SUM(total_quantity) AS total_quantity,

        SUM(order_revenue) AS total_revenue,

        SUM(order_profit) AS total_profit,

        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Late delivery'
        ) AS late_orders

    FROM category_order

    GROUP BY
        "Department Name",
        "Category Name"
)

SELECT

    "Department Name",

    "Category Name",

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
        NULLIF(total_revenue, 0),
        2
    ) AS profit_margin_percentage,

    late_orders,

    ROUND(
        late_orders * 100.0 /
        NULLIF(total_orders, 0),
        2
    ) AS late_delivery_percentage

FROM category_summary

ORDER BY total_revenue DESC;
