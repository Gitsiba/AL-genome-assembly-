#!/usr/bin/env bash
set -Eeuo pipefail
tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

# printf interprets \\t as actual tab characters; QUAST report.tsv is tab-delimited.
printf 'Assembly\\tHybrid\\tLong-read\\n# contigs\\t120\\t95\\nTotal length\\t410000000\\t405000000\\nN50\\t180000\\t150000\\n' > "$tmp/report.tsv"
printf 'C:94.2%%[S:90.0%%,D:4.2%%],F:2.1%%,M:3.7%%,n:1614\\n' > "$tmp/busco.txt"

python collect_assembly_metrics.py --quast "$tmp/report.tsv" --out "$tmp/metrics.csv" --busco "Hybrid=$tmp/busco.txt"

python - "$tmp/metrics.csv" <<'PY'
import csv, sys
with open(sys.argv[1], newline="") as handle:
    rows = list(csv.DictReader(handle))
assert len(rows) == 2, rows
hybrid = next(row for row in rows if row["assembly_method"] == "Hybrid")
assert hybrid["total_length_bp"] == "410000000", hybrid
assert hybrid["n50_bp"] == "180000", hybrid
assert hybrid["contig_count"] == "120", hybrid
assert hybrid["busco_complete_percent"] == "94.2", hybrid
long_read = next(row for row in rows if row["assembly_method"] == "Long-read")
assert long_read["busco_complete_percent"] == "", long_read
print("Metrics collector smoke test passed.")
PY
