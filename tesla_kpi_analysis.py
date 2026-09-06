import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

OUT = Path("outputs")
OUT.mkdir(exist_ok=True)

# Values are transcribed from the supplied academic report.
# They are retained as report figures, not presented as current Tesla filings.

kpis = pd.DataFrame({
    "KPI": [
        "Reported annual revenue figure (USD million)",
        "Reported revenue growth (percent)",
        "Reported production of electric vehicles",
        "Reported COVID-era profit increase (percent)",
        "Reported Q3 2021 annual revenue (USD billion)",
        "Reported expected growth (percent)",
    ],
    "Value": [5883, 125, 258690, 13, 1.62, 3.8],
    "Unit": ["USD million", "%", "vehicles", "%", "USD billion", "%"]
})
print("\nTesla KPI summary\n")
print(kpis.to_string(index=False))
kpis.to_csv(OUT / "tesla_kpis.csv", index=False)

# PESTLE figures mentioned in the report
pestle = pd.DataFrame({
    "Factor": ["Political", "Economic", "Social", "Technological", "Legal", "Environmental"],
    "Selected_Report_Indicator": [12.0, 1.6, 3.0, 47.0, 2.3, 67.0],
    "Unit": ["% investment increase", "% GDP growth", "% income growth",
             "% EV demand increase", "% taxation rise", "% citizens favoring lower-carbon vehicles"]
})
print("\nSelected PESTLE indicators\n")
print(pestle.to_string(index=False))
pestle.to_csv(OUT / "tesla_pestle.csv", index=False)

# Simple management dashboard chart
plt.figure(figsize=(9, 5))
plt.bar(pestle["Factor"], pestle["Selected_Report_Indicator"])
plt.title("Tesla: Selected PESTLE Indicators from the Report")
plt.ylabel("Reported percentage")
plt.xlabel("PESTLE factor")
plt.tight_layout()
plt.savefig(OUT / "tesla_pestle_indicators.png", dpi=160)
plt.close()

# SWOT matrix
swot = {
    "Strengths": [
        "Major supplier in automotive segments",
        "Electric vehicle positioning",
        "Large stakeholder chain",
        "High-performance vehicle positioning"
    ],
    "Weaknesses": [
        "Manufacturing complexity",
        "Raw-material sourcing/inventory issues",
        "Autopilot-related customer concerns"
    ],
    "Opportunities": [
        "International expansion",
        "Lower-cost vehicles",
        "Automated pickup trucks",
        "Separate supply chain",
        "Growth in electric public transportation"
    ],
    "Threats": [
        "Liability claims",
        "Product-design challenges",
        "Increasing competition",
        "Objections to lithium battery usage"
    ]
}
for category, items in swot.items():
    print(f"\n{category}")
    for item in items:
        print(f"- {item}")

# Management recommendations derived from the report
recommendations = pd.DataFrame({
    "Priority": [1, 2, 3],
    "Recommendation": [
        "Reduce product defects before prioritising additional production volume",
        "Use partnerships to accelerate international reach, then operate independently where strategic",
        "Strengthen supply-chain resilience and inventory management"
    ],
    "Suggested_KPI": [
        "Defect rate / warranty claims",
        "International revenue share",
        "Stockout rate / supplier lead time"
    ]
})
recommendations.to_csv(OUT / "tesla_recommendations.csv", index=False)

print("\nFiles written to:", OUT.resolve())
