DROP VIEW IF EXISTS quarterly_kpis;
CREATE VIEW quarterly_kpis AS
WITH l AS (
SELECT *,LAG(revenue_usd_m) OVER(ORDER BY quarter_end) previous_quarter,
LAG(revenue_usd_m,4) OVER(ORDER BY quarter_end) previous_year,
LAG(deliveries,4) OVER(ORDER BY quarter_end) seasonal_delivery_baseline
FROM quarterly)
SELECT *,1.0*gross_profit_usd_m/NULLIF(revenue_usd_m,0) gross_margin,
1.0*operating_income_usd_m/NULLIF(revenue_usd_m,0) operating_margin,
1.0*(revenue_usd_m-previous_quarter)/NULLIF(previous_quarter,0) qoq_growth,
1.0*(revenue_usd_m-previous_year)/NULLIF(previous_year,0) yoy_growth,
deliveries-seasonal_delivery_baseline forecast_error FROM l;
