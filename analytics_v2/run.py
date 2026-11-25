from pathlib import Path
import sqlite3
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
ROOT=Path(__file__).resolve().parent
def main():
    df=pd.read_csv(ROOT/"quarterly.csv",parse_dates=["quarter_end"]).sort_values("quarter_end")
    assert len(df)==12 and df.quarter_end.is_unique and not df.isna().any().any()
    assert (df.revenue_usd_m>0).all()
    assert ((df.automotive_revenue_usd_m+df.energy_revenue_usd_m+df.services_revenue_usd_m-df.revenue_usd_m).abs()<=2).all()
    out=ROOT/"output";out.mkdir(exist_ok=True)
    df.quarter_end=df.quarter_end.dt.strftime("%Y-%m-%d")
    with sqlite3.connect(out/"tesla.sqlite") as c:
        df.to_sql("quarterly",c,index=False,if_exists="replace")
        c.executescript((ROOT/"analysis.sql").read_text())
        k=pd.read_sql_query("SELECT * FROM quarterly_kpis ORDER BY quarter_end",c)
    k.to_csv(out/"quarterly_kpis.csv",index=False)
    test=k.tail(4)
    print("2025 seasonal baseline delivery MAE:",test.forecast_error.abs().mean())
    fig,ax=plt.subplots(2,2,figsize=(12,8),layout="constrained")
    dates=pd.to_datetime(k.quarter_end)
    for a,col,title in zip(ax.ravel(),["revenue_usd_m","operating_margin","deliveries","inventory_days"],["Revenue (USD m)","Operating margin (ratio)","Deliveries","Inventory days"]):
        a.plot(dates,k[col],marker="o");a.set_title(title);a.tick_params(axis="x",rotation=30)
    fig.savefig(out/"dashboard.png",dpi=150)
if __name__=="__main__":main()
