"""Create a Tableau-compatible TWB/TWBX package from verified aggregate CSVs.
Uses legacy textscan XML structure. No Tableau runtime is invoked.
"""
import csv, math, sys, re, json, zipfile, shutil
from pathlib import Path
from xml.etree import ElementTree as ET
from copy import deepcopy

kind=sys.argv[1]
kit=Path(sys.argv[2])
out=Path(sys.argv[3])
out.mkdir(parents=True,exist_ok=True)
stage=out/"stage"
stage.mkdir(exist_ok=True)
data=stage/"Data"
data.mkdir(exist_ok=True)

def read(name):
    matches=list(kit.rglob(name))
    if len(matches)!=1:raise ValueError((name,matches))
    with matches[0].open(encoding="utf-8-sig",newline="") as f:
        rows=list(csv.DictReader(f))
    assert rows,name
    return rows
def num(x):
    try:
        v=float(x)
        return v if math.isfinite(v) else None
    except (ValueError,TypeError):return None
def write(name,headers,rows):
    path=data/(name+".csv")
    with path.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f);w.writerow(headers);w.writerows(rows)
    assert path.stat().st_size>0
    return path

sources={}
sheets=[]
def source(name,columns,rows):
    # columns: (physical field name, data type, display caption)
    assert name not in sources and rows
    write(name,[x[0] for x in columns],rows)
    sources[name]=columns
    return name
def sheet(name,source_name,mark,x=None,y=None,text=None):
    sheets.append(dict(name=name,source=source_name,mark=mark,x=x,y=y,text=text))
def chart(name,rows,dim,val,dim_caption,val_caption,mark="Bar",factor=1,limit=None):
    clean=[(r[dim],num(r[val])) for r in rows if r.get(dim) and num(r.get(val)) is not None]
    if limit:clean=sorted(clean,key=lambda r:r[1],reverse=True)[:limit]
    source(name,[("category","string",dim_caption),("amount","real",val_caption)],[(a,b*factor) for a,b in clean])
    sheet(val_caption,name,mark,x="category",y="amount") if mark=="Line" else sheet(val_caption,name,mark,x="amount",y="category")

if kind=="Olist":
    title="Olist | E-commerce and supply chain analytics"
    k={r["metric"]:float(r["value"]) for r in read("verified_kpis.csv")}
    specs=[("orders","Orders","Orders",1),("value","Delivered merchandise value","Merchandise value (BRL)",1),("ontime","On-time delivery","On-time delivery (%)",100),("cancel","Cancellation rate","Cancellation rate (%)",100)]
    source("kpi",[(a,"real",c) for a,b,c,m in specs],[[round(k[b]*m,2) for a,b,c,m in specs]])
    for a,b,c,m in specs:sheet(c,"kpi","Text",text=a)
    chart("monthly",read("monthly_kpis.csv"),"month","revenue","Month","Monthly merchandise value (BRL)","Line")
    chart("states",read("state_kpis.csv"),"customer_state","on_time_rate","State","On-time delivery by state (%)",factor=100,limit=12)
    chart("category",read("category_kpis.csv"),"category","revenue","Category","Top category merchandise value (BRL)",limit=10)
    rows=read("forecast_holdout.csv")
    first=next(iter(rows[0]))
    chart("forecast",rows,first,"actual","Month","Holdout actual merchandise value (BRL)","Line")
    subtitle="Historical Olist data | Independent portfolio case study | SQL and Python validation passed"
elif kind=="StockMarket":
    title="Brazilian market | Historical data quality and analytics"
    k={r["metric"]:float(r["value"]) for r in read("verified_kpis.csv")}
    specs=[("loaded","Source stock records"),("accepted","Accepted stock records"),("companies","Company identifiers")]
    source("kpi",[(a,"integer",b) for a,b in specs]+[("acceptance_pct","real","Acceptance (%)")],[[int(k[b]) for a,b in specs]+[round(100*k["Accepted stock records"]/k["Source stock records"],2)]])
    for a,b in specs:sheet(b,"kpi","Text",text=a)
    sheet("Acceptance (%)","kpi","Text",text="acceptance_pct")
    r=read("sectors.csv")
    chart("volume",r,"sectorCompany","volume","Source classification","Top classification volume (units)",limit=10)
    eligible=[x for x in r if num(x.get("observations")) is not None and num(x["observations"])>=20]
    chart("returns",eligible,"sectorCompany","mean_daily_return","Source classification","Mean unadjusted price change (%)",factor=100,limit=10)
    chart("observations",r,"sectorCompany","observations","Source classification","Top return observation counts",limit=10)
    source("quality",[("category","string","Quality outcome"),("amount","integer","Rows")],[("Accepted",int(k["Accepted stock records"])),("Excluded",int(k["Excluded stock records"]))])
    sheet("Quality outcomes","quality","Bar",x="amount",y="category")
    subtitle="1998–2020 accepted subset | Integer-volume policy | Unadjusted prices; classification labels may be indices"
elif kind=="Tesla":
    title="Tesla | Quarterly financial and operational analytics"
    r=read("quarterly.csv")
    latest=[x for x in r if x["quarter_end"].startswith("2025")]
    rev=sum(float(x["revenue_usd_m"]) for x in latest);op=sum(float(x["operating_income_usd_m"]) for x in latest)
    source("kpi",[("revenue","integer","2025 revenue (USD million)"),("margin","real","2025 operating margin (%)"),("deliveries","integer","2025 deliveries"),("energy","integer","2025 energy revenue (USD million)")],[[int(rev),round(100*op/rev,2),sum(int(x["deliveries"]) for x in latest),sum(int(x["energy_revenue_usd_m"]) for x in latest)]])
    for a,b in [("revenue","2025 revenue (USD million)"),("margin","2025 operating margin (%)"),("deliveries","2025 deliveries"),("energy","2025 energy revenue (USD million)")]:sheet(b,"kpi","Text",text=a)
    for row in r:row["operating_margin_pct"]=str(100*float(row["operating_income_usd_m"])/float(row["revenue_usd_m"]))
    chart("revenue",r,"quarter_end","revenue_usd_m","Quarter","Revenue (USD million)","Line")
    chart("margin",r,"quarter_end","operating_margin_pct","Quarter","Operating margin (%)","Line")
    chart("deliveries",r,"quarter_end","deliveries","Quarter","Vehicle deliveries","Line")
    chart("inventory",r,"quarter_end","inventory_days","Quarter","Inventory days (quarter-end)","Line")
    subtitle="12 reported historical quarters | 2023–2025 | SQL and Python validation passed"
else:raise ValueError(kind)

def add(parent,tag,attrs=None,txt=None):
    e=ET.SubElement(parent,tag,{str(k):str(v) for k,v in (attrs or {}).items()})
    if txt is not None:e.text=str(txt)
    return e
def dsid(n):return "textscan."+n
def column(parent,field):
    n,t,caption=field
    return add(parent,"column",{"caption":caption,"datatype":t,"name":"["+n+"]","role":"dimension" if t=="string" else "measure","type":"nominal" if t=="string" else "quantitative"})
def instance(parent,field):
    n,t,c=field
    typ="nominal" if t=="string" else "quantitative"
    ref="[none:"+n+":nk]" if t=="string" else "[sum:"+n+":qk]"
    add(parent,"column-instance",{"column":"["+n+"]","derivation":"None" if t=="string" else "Sum","name":ref,"pivot":"key","type":typ})
    return ref

root=ET.Element("workbook",{"original-version":"18.1","version":"18.1","source-platform":"mac","xmlns:user":"http://www.tableausoftware.com/xml/user"})
add(root,"style-theme",{"name":"clean"})
dsroot=add(root,"datasources")
for n,cols in sources.items():
    ds=add(dsroot,"datasource",{"caption":n,"inline":"true","name":dsid(n),"version":"18.1"})
    con=add(ds,"connection",{"class":"textscan","directory":"Data","filename":n+".csv","password":"","server":""})
    rel=add(con,"relation",{"name":n+"#csv","table":"["+n+"#csv]","type":"table"})
    cc=add(rel,"columns",{"character-set":"UTF-8","header":"yes","locale":"en_US","separator":","})
    for j,(field,t,caption) in enumerate(cols):add(cc,"column",{"datatype":t,"name":field,"ordinal":j})
    mr=add(con,"metadata-records")
    for j,(field,t,caption) in enumerate(cols):
        rec=add(mr,"metadata-record",{"class":"column"})
        for tag,value in [("remote-name",field),("remote-type",{"string":129,"real":5,"integer":20}[t]),("local-name","["+field+"]"),("parent-name","["+n+"#csv]"),("remote-alias",field),("ordinal",j),("local-type",t),("aggregation","Count" if t=="string" else "Sum"),("contains-null","false")]:add(rec,tag,txt=value)
    add(ds,"aliases",{"enabled":"yes"})
    for field in cols:column(ds,field)
ws=add(root,"worksheets")
for s in sheets:
    n=s["source"];cols=sources[n];lookup={x[0]:x for x in cols}
    w=add(ws,"worksheet",{"name":s["name"]})
    table=add(w,"table");view=add(table,"view")
    d=add(view,"datasources");add(d,"datasource",{"caption":n,"name":dsid(n)})
    dep=add(view,"datasource-dependencies",{"datasource":dsid(n)})
    fields=[x for x in (s["x"],s["y"],s["text"]) if x]
    for field in fields:column(dep,lookup[field])
    refs={field:"["+dsid(n)+"]."+instance(dep,lookup[field]) for field in fields}
    add(view,"aggregation",{"value":"true"})
    style=add(table,"style")
    panes=add(table,"panes");pane=add(panes,"pane",{"selection-relaxation-option":"selection-relaxation-allow"})
    pv=add(pane,"view");add(pv,"breakdown",{"value":"auto"})
    add(pane,"mark",{"class":s["mark"]})
    if s["text"]:
        enc=add(pane,"encodings");add(enc,"text",{"column":refs[s["text"]]})
    pst=add(pane,"style");sr=add(pst,"style-rule",{"element":"mark"});add(sr,"format",{"attr":"color","value":"#247B94"})
    add(table,"rows",txt=refs.get(s["y"],""))
    add(table,"cols",txt=refs.get(s["x"],""))
dashboards=add(root,"dashboards")
dashboard=add(dashboards,"dashboard",{"name":"Executive Dashboard"})
add(dashboard,"style");add(dashboard,"size",{"maxheight":"850","maxwidth":"1400","minheight":"850","minwidth":"1400","sizing-mode":"fixed"})
zones=add(dashboard,"zones")
z=add(zones,"zone",{"id":1,"type-v2":"text","x":1000,"y":1000,"w":98000,"h":8000})
ft=add(z,"formatted-text");add(ft,"run",{"bold":"true","fontsize":20},title)
z=add(zones,"zone",{"id":2,"type-v2":"text","x":1000,"y":8500,"w":98000,"h":5000})
ft=add(z,"formatted-text");add(ft,"run",{"fontsize":11},subtitle)
for i,s in enumerate(sheets):
    if i<4:x=1000+i*24750;y=14500;w=23750;h=14500
    else:x=1000+((i-4)%2)*49500;y=30000+((i-4)//2)*34500;w=48500;h=33500
    zone=add(zones,"zone",{"id":i+3,"name":s["name"],"x":x,"y":y,"w":w,"h":h,"show-title":"true"})
    zs=add(zone,"zone-style")
    add(zs,"format",{"attr":"border-color","value":"#DCE6EB"})
    add(zs,"format",{"attr":"border-style","value":"solid"})
    add(zs,"format",{"attr":"border-width","value":"1"})
windows=add(root,"windows")
for s in sheets:add(windows,"window",{"class":"worksheet","name":s["name"]})
add(windows,"window",{"class":"dashboard","name":"Executive Dashboard","maximized":"1"})
ET.indent(root,space="  ")
twb=stage/(kind+".twb")
ET.ElementTree(root).write(twb,encoding="utf-8",xml_declaration=True)
pkg=out/(kind+".twbx")
with zipfile.ZipFile(pkg,"w",compression=zipfile.ZIP_DEFLATED) as z:
    for p in sorted(stage.rglob("*")):
        if p.is_file():z.write(p,p.relative_to(stage).as_posix())
with zipfile.ZipFile(pkg) as z:
    assert z.testzip() is None
    doc=ET.fromstring(z.read(kind+".twb"))
    refs={x.attrib["name"] for x in doc.findall("./worksheets/worksheet")}
    for zone in doc.findall("./dashboards/dashboard/zones/zone"):
        if "name" in zone.attrib:assert zone.attrib["name"] in refs
    for c in doc.findall("./datasources/datasource/connection"):
        f=c.attrib["directory"]+"/"+c.attrib["filename"];assert f in z.namelist()
        with z.open(f) as stream:assert len(stream.read().splitlines())>=2
    assert len(refs)==8
    assert len(doc.findall("./dashboards/dashboard"))==1
shutil.copyfile(twb,out/(kind+".twb"))
shutil.rmtree(stage)
(out/"validation.json").write_text(json.dumps({"workbook":pkg.name,"worksheets":len(sheets),"dashboards":1,"embedded_data_sources":len(sources),"zip_crc":"passed","xml_parse":"passed","dashboard_references":"passed","data_paths":"passed","tableau_runtime":"not run","public_publication":"not done"},indent=2)+"\n")
print(f"PASS: {pkg.name}, {len(sheets)} worksheets, {len(sources)} CSV sources, one dashboard; ZIP/XML/reference checks. Tableau runtime not tested.")
