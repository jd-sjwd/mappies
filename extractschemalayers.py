import requests
import os
from datetime import datetime

TOKEN = "YOUR_TOKEN_HERE"
BASE = "YOUR_REST_SERVICES_URL/FeatureServer"

outdir = f"agol_schema_extract_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(outdir, exist_ok=True)

def fetch(url, params):
    r = requests.get(url, params=params)
    r.raise_for_status()
    return r.json()

# 1) Fetch service definition
service_def = fetch(BASE, {"f": "pjson", "token": TOKEN})
with open(f"{outdir}/FeatureServer_service_definition.json", "w") as f:
    f.write(requests.utils.json.dumps(service_def, indent=2))

# 2) Collect layer + table IDs
ids = []
for lyr in service_def.get("layers", []):
    ids.append((lyr["id"], lyr["name"], "layer"))
for tbl in service_def.get("tables", []):
    ids.append((tbl["id"], tbl["name"], "table"))

# 3) Fetch each schema
for id_, name, kind in ids:
    print(f"Fetching {kind}: {id_} ({name})")
    schema = fetch(f"{BASE}/{id_}", {"f": "pjson", "token": TOKEN})
    safe_name = name.replace(" ", "_").replace("/", "_")
    with open(f"{outdir}/{id_}_{safe_name}_schema.json", "w") as f:
        f.write(requests.utils.json.dumps(schema, indent=2))

print(f"\nDone. Schemas saved in: {outdir}")
