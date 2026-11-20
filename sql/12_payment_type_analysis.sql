
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 12: PAYMENT TYPE PERFORMANCE ANALYSIS
-- ============================================================

SELECT
    "Type" AS payment_type,

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
        WHERE "Delivery Status" = 'Late delivery'
    ) AS late_delivery_items,

    ROUND(
        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Late delivery'
        ) * 100.0 /
        NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_percentage

FROM public.supply_chain

GROUP BY "Type"

ORDER BY total_revenue DESC;
