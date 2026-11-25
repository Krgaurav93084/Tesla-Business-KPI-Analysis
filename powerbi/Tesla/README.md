# Tesla | Quarterly performance 2023–2025

Editable Power BI Project (PBIP) source, report visuals, M query, DAX measures and expected-value checks. Not a PBIX binary or a screenshot. Desktop runtime compatibility is untested.

Data: [quarterly.csv](../../analytics_v2/quarterly.csv), 12 reported historical quarters. Cards are all-period totals; latest inventory is nonadditive.

1. Clone/download the entire repository. Keep report and model folders beside Tesla.pbip.
2. Open Tesla.pbip in current Power BI Desktop on Windows. Enable project/PBIR support in Options if needed.
3. Refresh, using anonymous credentials for raw.githubusercontent.com if prompted. Check Power Query for errors.
4. Paste verify.dax into DAX Query View and compare output with expected_results.csv, allowing ordinary floating-point rounding.
5. Inspect all visuals, Save As > Power BI Desktop file (*.pbix), and capture genuine screenshots. Override the gitignore intentionally or use Git LFS for large PBIX files.

Official format reference: https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-overview . No PBIX export or Desktop runtime execution has been performed.
