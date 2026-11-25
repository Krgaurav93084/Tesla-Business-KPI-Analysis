# Tableau | Tesla Financial & Operational Analytics
Mac-compatible Tableau Desktop Professional or Public Edition authoring kit. This folder contains instructions and a workflow that packages previously validated historical outputs. It is not a completed Tableau workbook or a Tableau runtime test.

[Historical validation](https://github.com/Krgaurav93084/Tesla-Business-KPI-Analysis/actions/runs/45620622068) · [Tableau data-kit workflow](https://github.com/Krgaurav93084/Tesla-Business-KPI-Analysis/actions/workflows/tableau-data-kit.yml)

## Build the Tableau dashboard
Use quarterly.csv as the main data source (12 rows). Set quarter_end to Date; all other columns to Number.
| Sheet | Columns | Rows / Marks |
|---|---|---|
| Revenue trend | QUARTER(quarter_end), continuous | SUM(revenue_usd_m), Line |
| Operating and gross margins | QUARTER(quarter_end), continuous | Measure Values for calculated margins, Line |
| Production vs deliveries | QUARTER(quarter_end), continuous | Measure Values for production and deliveries, Line |
| Inventory days | QUARTER(quarter_end), continuous | AVG(inventory_days), Line |
| Annual revenue by segment | YEAR(quarter_end) | Measure Values for automotive, energy, services revenue, stacked Bar |

### Calculated fields
- Operating Margin: `IF SUM([revenue_usd_m]) <> 0 THEN SUM([operating_income_usd_m]) / SUM([revenue_usd_m]) END`
- Gross Margin: `IF SUM([revenue_usd_m]) <> 0 THEN SUM([gross_profit_usd_m]) / SUM([revenue_usd_m]) END`
- Delivery Gap: `SUM([production]) - SUM([deliveries])`
- Revenue YoY: `IF LOOKUP(SUM([revenue_usd_m]), -4) <> 0 THEN SUM([revenue_usd_m]) / LOOKUP(SUM([revenue_usd_m]), -4) - 1 END` (compute using ascending quarter_end with all contiguous quarters present)
- Revenue QoQ: same calculation with offset -1.
Use a year filter across sheets; retain earlier quarters in the partition for table calculations or use a display-only table-calculation filter. Format margins and growth as percentages; revenue in USD millions. Inventory days are nonadditive. For 2025: revenue 94,827 USD million; deliveries 1,636,129; operating margin approximately 4.59%. See the existing quarterly_kpis.csv and annual_kpis.csv for precomputed comparisons.

## Open and publish on a Mac
1. Download the Tableau data-kit ZIP from the latest successful workflow and extract it.
2. In Tableau Desktop, Connect > Text File and select the required CSVs. Verify column types and calculations; create the worksheets and dashboard described above.
3. Compare displayed values with the validated findings in the repository. Save a packaged workbook (.twbx) using File > Save As.
4. For a public portfolio, use Server > Tableau Public > Save to Tableau Public with your own authenticated Tableau account. Use only public, non-confidential data and respect the original dataset license. Save an actual image of the rendered dashboard and upload the workbook, screenshot and public link to GitHub.
5. Record Tableau version, tested metrics, and any differences.

The existing Power BI project remains separate. Tableau calculations do not execute DAX or Power Query. This kit has not been opened in Tableau; no workbook, screenshot or public Tableau link is claimed.
