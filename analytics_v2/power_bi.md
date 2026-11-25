# Power BI build guide
Import quarterly.csv, name the table quarterly, set quarter_end to Date, numeric columns to numbers. Create a continuous calendar from 2023-01-01 to 2025-12-31 and mark it as date table; relate calendar[Date] to quarterly[quarter_end]. Use year/quarter slicers. Add measures separately:
```dax
Revenue = SUM(quarterly[revenue_usd_m])
Gross Profit = SUM(quarterly[gross_profit_usd_m])
Gross Margin = DIVIDE([Gross Profit],[Revenue])
Operating Margin = DIVIDE(SUM(quarterly[operating_income_usd_m]),[Revenue])
Deliveries = SUM(quarterly[deliveries])
Production = SUM(quarterly[production])
Revenue Prior Quarter = CALCULATE([Revenue],DATEADD('Calendar'[Date],-1,QUARTER))
Revenue QoQ = DIVIDE([Revenue]-[Revenue Prior Quarter],[Revenue Prior Quarter])
Revenue Prior Year = CALCULATE([Revenue],SAMEPERIODLASTYEAR('Calendar'[Date]))
Revenue YoY = DIVIDE([Revenue]-[Revenue Prior Year],[Revenue Prior Year])
Inventory Days Latest = CALCULATE(MAX(quarterly[inventory_days]),LASTDATE(quarterly[quarter_end]))
```
Use line charts for revenue and margins, clustered production/delivery columns, and separate inventory-day trend. Inventory days are a snapshot, not additive. For forecast vs actual use quarterly_kpis.csv instead of mixing grains. Native PBIX not created; SVG is an actual data-derived visual, not a Power BI screenshot.
