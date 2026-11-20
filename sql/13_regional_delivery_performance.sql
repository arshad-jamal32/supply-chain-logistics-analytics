
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 13: REGIONAL DELIVERY PERFORMANCE
-- ============================================================

SELECT
    "Order Region" AS order_region,

    COUNT(DISTINCT "Order Id") AS total_orders,

    COUNT(*) AS total_order_items,

    COUNT(*) FILTER (
        WHERE "Delivery Status" = 'Late delivery'
    ) AS late_delivery_items,

    ROUND(
        COUNT(*) FILTER (
            WHERE "Delivery Status" = 'Late delivery'
        ) * 100.0 /
        NULLIF(COUNT(*), 0),
        2
    ) AS late_delivery_percentage,

    ROUND(AVG("Days for shipping (real)"), 2)
        AS average_actual_shipping_days,

    ROUND(AVG("Days for shipment (scheduled)"), 2)
        AS average_scheduled_shipping_days,

    ROUND(AVG("Shipping Delay Days"), 2)
        AS average_shipping_delay_days,

    ROUND(SUM("Sales"), 2) AS total_revenue,

    ROUND(SUM("Benefit per order"), 2) AS total_profit

FROM public.supply_chain

WHERE "Delivery Status" <> 'Shipping canceled'

GROUP BY "Order Region"

ORDER BY late_delivery_percentage DESC;
