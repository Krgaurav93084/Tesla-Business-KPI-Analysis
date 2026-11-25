# Tesla Business KPI & Strategic Analysis

## Overview
This project turns the Tesla business-management report into a practical Data Analyst / Business Analyst portfolio project.

The analysis focuses on Tesla's products and services, internal and external environment, PESTLE factors, competitive forces, SWOT findings, COVID-19 business impact, mitigation measures, and strategic recommendations.

## Business Questions
- How do Tesla's business capabilities support competitive advantage?
- Which PESTLE factors create opportunities or risks?
- What are the major strengths, weaknesses, opportunities and threats?
- Which KPIs should management monitor?
- What strategic actions can improve growth and reduce defects?

## Deliverables
- `tesla_kpi_analysis.py` — runnable Python analysis that creates KPI tables and charts.
- No external dataset is required; the script uses clearly labelled values extracted from the supplied report.

## Run
```bash
pip install pandas matplotlib
python tesla_kpi_analysis.py
```

## Important Note
The source report contains historical/academic figures and some values that are not directly comparable to current Tesla financial reporting. This portfolio implementation preserves the report's figures rather than silently replacing them with newer data.

## Source
Based on the supplied report, which discusses Tesla products, PESTLE, Porter Five Forces, SWOT, COVID-19 impact and strategic recommendations.

## Source-backed quarterly analytics (2023–2025)
See [quarterly dashboard and analysis](analytics_v2/README.md) and [calculated findings](analytics_v2/findings.md). The extension contains 12 official reported quarterly rows, SQL, Python and DAX. The original academic charts are retained separately and should not be used to compare unlike measures.

![Historical financial and operational dashboard](analytics_v2/dashboard.svg)

## Reproducibility validation — 25 November 2026
The [GitHub Actions validation run](https://github.com/Krgaurav93084/Tesla-Business-KPI-Analysis/actions/runs/45620622068) passed. It executed the SQLite/Python pipeline, checked all 12 unique quarterly observations, reconciled operating margin, and generated annual and quarterly KPI tables. The 2025 seasonal delivery baseline MAE was 55,378.75 vehicles. The [run artifact](https://github.com/Krgaurav93084/Tesla-Business-KPI-Analysis/actions/runs/45620622068/artifacts/15023857964) includes the generated dashboard PNG, SQLite database, and CSV results (artifact retention applies). The existing dashboard SVG and findings remain available in the repository. This validates calculations against the bundled quarterly CSV, not independently re-audited source filings. The PNG is a Python chart, not a Power BI Desktop screenshot; no native PBIX is claimed.

## Editable Power BI report source
[Open the Tesla Power BI Project](powerbi/Tesla/README.md) — includes PBIP source, model.bim semantic model, report visuals, Power Query and DAX verification query with expected values. [Static validation workflow](https://github.com/Krgaurav93084/Tesla-Business-KPI-Analysis/actions/workflows/validate-powerbi.yml). Native PBIX export, Desktop rendering, and actual M/DAX engine verification require Power BI Desktop; source validation is not a substitute for engine tests.
