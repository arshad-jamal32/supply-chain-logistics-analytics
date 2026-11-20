
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 08: MONTHLY DATA QUALITY INVESTIGATION
-- ============================================================

SELECT

    TO_CHAR(
        DATE_TRUNC('month', "order date (DateOrders)"),
        'YYYY-MM'
    ) AS order_month,

    COUNT(DISTINCT "Order Id") AS total_orders,

    COUNT(DISTINCT "Order Item Id") AS total_order_items,

    ROUND(
        COUNT(DISTINCT "Order Item Id")::NUMERIC /
        NULLIF(COUNT(DISTINCT "Order Id"), 0),
        2
    ) AS items_per_order,

    SUM("Order Item Quantity") AS total_quantity_sold,

    ROUND(
        AVG("Sales"),
        2
    ) AS avg_sales_per_item,

    ROUND(
        SUM("Sales"),
        2
    ) AS total_revenue

FROM public.supply_chain

GROUP BY
    DATE_TRUNC('month', "order date (DateOrders)")

ORDER BY order_month;
