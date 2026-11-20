
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 10: DEPARTMENT-WISE PERFORMANCE
-- ============================================================

SELECT
    "Department Name" AS department,

    COUNT(DISTINCT "Order Id") AS total_orders,

    COUNT(*) AS total_order_items,

    SUM("Order Item Quantity") AS total_quantity_sold,

    ROUND(SUM("Sales"), 2) AS total_revenue,

    ROUND(SUM("Benefit per order"), 2) AS total_profit,

    ROUND(
        SUM("Sales") * 100.0 /
        SUM(SUM("Sales")) OVER (),
        2
    ) AS revenue_share_percentage,

    ROUND(
        SUM("Benefit per order") * 100.0 /
        NULLIF(SUM("Sales"), 0),
        2
    ) AS profit_margin_percentage,

    COUNT(*) FILTER (
        WHERE "Benefit per order" < 0
    ) AS loss_making_items

FROM public.supply_chain

GROUP BY "Department Name"

ORDER BY total_revenue DESC;
