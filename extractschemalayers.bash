# --- set these first ---
TOKEN='YOUR_TOKEN_HERE'
BASE='BASE_REST_URL/FeatureServer'

# --- output folder ---
OUTDIR="agol_schema_extract_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$OUTDIR"

# 1) Save the service definition (provenance matters)
curl -sS "$BASE" \
  --data-urlencode "f=pjson" \
  --data-urlencode "token=$TOKEN" \
  > "$OUTDIR/FeatureServer_service_definition.json"

# 2) Extract ALL layer + table IDs and fetch each schema
jq -r '(.layers[]?.id, .tables[]?.id) | tostring' \
  "$OUTDIR/FeatureServer_service_definition.json" \
| while read -r id; do
    echo "Fetching schema for id=$id"
    curl -sS "$BASE/$id" \
      --data-urlencode "f=pjson" \
      --data-urlencode "token=$TOKEN" \
      > "$OUTDIR/${id}_schema.json"
  done

echo "Done. Schemas saved to: $OUTDIR"
