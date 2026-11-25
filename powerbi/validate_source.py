from pathlib import Path
import csv,json,sys,urllib.request
import jsonschema
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT7

def retrieve(uri):
    if not uri.startswith("https://developer.microsoft.com/json-schemas/fabric/"):
        raise ValueError("Unexpected schema URL: "+uri)
    with urllib.request.urlopen(uri,timeout=30) as response:
        return Resource.from_contents(json.load(response),default_specification=DRAFT7)

root=Path(sys.argv[1]); name=root.name
def read(p):return json.loads(p.read_text(encoding="utf-8"))
report=root/(name+".Report")
semantic=root/(name+".SemanticModel")
project=read(root/(name+".pbip"))
assert project["artifacts"][0]["report"]["path"]==report.name
ref=read(report/"definition.pbir")
assert (report/ref["datasetReference"]["byPath"]["path"]).resolve()==semantic.resolve()
model=read(semantic/"model.bim")
tables={t["name"]:t for t in model["model"]["tables"]}
definitions={}
for t in tables.values():
    definitions[t["name"]]={"Column":{c["name"] for c in t["columns"]},"Measure":{m["name"] for m in t.get("measures",[])}}
    assert t["partitions"][0]["source"]["type"]=="m"
    expression="\n".join(t["partitions"][0]["source"]["expression"])
    assert "Web.Contents" in expression and "Table.TransformColumnTypes" in expression
registry=Registry(retrieve=retrieve)
count=0
for p in [report/"definition.pbir",semantic/"definition.pbism",*report.rglob("*.json")]:
    doc=read(p)
    if "$schema" in doc:
        schema=retrieve(doc["$schema"]).contents
        jsonschema.Draft7Validator(schema,registry=registry).validate(doc)
        count+=1
for p in report.rglob("visual.json"):
    doc=read(p); visual=doc["visual"]
    pos=doc["position"]
    assert pos["x"]>=0 and pos["y"]>=0 and pos["x"]+pos["width"]<=1280 and pos["y"]+pos["height"]<=720
    for role in visual["query"]["queryState"].values():
        for item in role["projections"]:
            for kind,field in item["field"].items():
                assert field["Property"] in definitions[field["Expression"]["SourceRef"]["Entity"]][kind],(p,field)
with (root/"expected_results.csv").open() as f:
    expected={r["measure"]:float(r["expected_value"]) for r in csv.DictReader(f)}
assert set(expected)=={m for t in definitions.values() for m in t["Measure"]}
assert all("["+name+"]" in (root/"verify.dax").read_text() for name in expected)
print(f"PASS: {count} Power BI JSON definitions conform to Microsoft schemas; all visual field references and expected-measure names match.")
print("Scope: static schema and metadata checks only. Power Query refresh, DAX execution, Desktop rendering and PBIX export require a real Power BI session.")
