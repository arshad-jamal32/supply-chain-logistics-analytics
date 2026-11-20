
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 14: COUNTRY-WISE BUSINESS PERFORMANCE
-- ============================================================

SELECT
    "Order Country" AS country,

    COUNT(DISTINCT "Order Id") AS total_orders,

    COUNT(*) AS total_order_items,

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
        NULLIF(
            COUNT(*) FILTER (
                WHERE "Delivery Status" <> 'Shipping canceled'
            ),
            0
        ),
        2
    ) AS late_delivery_percentage

FROM public.supply_chain

WHERE "Delivery Status" <> 'Shipping canceled'

GROUP BY "Order Country"

ORDER BY total_revenue DESC

LIMIT 10;
