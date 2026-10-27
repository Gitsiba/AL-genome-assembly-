#!/usr/bin/env bash
set -euo pipefail

IMAGE="${1:-al-genome-assembly:ci}"
TMP_DIR="$(mktemp -d)"
# Files created by the container may be owned by root on the bind mount.
# Restore owner permissions before removing the temporary directory.
trap 'chmod -R u+rwX "$TMP_DIR" 2>/dev/null || true; rm -rf "$TMP_DIR"' EXIT

cat > "$TMP_DIR/test_metrics.csv" <<'CSV'
assembly_method,total_length_bp,n50_bp,contig_count,busco_complete_percent
Synthetic_A,1000000,25000,120,85
Synthetic_B,1100000,40000,90,90
CSV

docker run --rm --entrypoint python \
  -v "$TMP_DIR:/work" -w /work \
  "$IMAGE" /app/plot_assembly test_metrics.csv --outdir test-output

for file in assembly_total_length.png assembly_n50.png assembly_contig_count.png assembly_busco_complete.png; do
  test -s "$TMP_DIR/test-output/$file"
done

echo "PASS: plotting CLI produced all four expected PNG files from synthetic test data."
echo "NOTE: synthetic metrics are for software testing only, not biological results."
