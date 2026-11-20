
-- ============================================================
-- PROJECT: SUPPLY CHAIN & LOGISTICS PERFORMANCE ANALYTICS
-- PHASE 1: OVERALL BUSINESS PERFORMANCE
-- QUERY 09: DISCOUNT IMPACT ON PROFITABILITY
-- ============================================================

WITH discount_analysis AS (

    SELECT

        CASE
            WHEN "Order Item Discount Rate" = 0
                THEN 'No Discount'

            WHEN "Order Item Discount Rate" <= 0.10
                THEN '0.01% - 10%'

            WHEN "Order Item Discount Rate" <= 0.20
                THEN '10.01% - 20%'

            WHEN "Order Item Discount Rate" <= 0.30
                THEN '20.01% - 30%'

            ELSE 'Above 30%'
        END AS discount_band,

        "Order Id",

        "Sales",

        "Benefit per order",

        "Order Item Quantity",

        "Order Item Discount Rate"

    FROM public.supply_chain
)

SELECT

    discount_band,

    COUNT(*) AS total_order_items,

    COUNT(DISTINCT "Order Id") AS total_orders,

    SUM("Order Item Quantity") AS total_quantity_sold,

    ROUND(SUM("Sales"), 2) AS total_revenue,

    ROUND(SUM("Benefit per order"), 2) AS total_profit,

    ROUND(AVG("Order Item Discount Rate") * 100, 2)
        AS average_discount_percentage,

    ROUND(
        SUM("Benefit per order") * 100.0 /
        NULLIF(SUM("Sales"), 0),
        2
    ) AS profit_margin_percentage,

    COUNT(*) FILTER (
        WHERE "Benefit per order" < 0
    ) AS loss_making_items

FROM discount_analysis

GROUP BY discount_band

ORDER BY
    CASE discount_band
        WHEN 'No Discount' THEN 1
        WHEN '0.01% - 10%' THEN 2
        WHEN '10.01% - 20%' THEN 3
        WHEN '20.01% - 30%' THEN 4
        ELSE 5
    END;
