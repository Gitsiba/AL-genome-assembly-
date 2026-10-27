#!/usr/bin/env python3
"""Create the plotting CSV from QUAST report.tsv and optional BUSCO short summary.

Only extracts values present in the supplied reports. Missing BUSCO values remain
blank. This script does not run QUAST/BUSCO and does not infer assembly quality.
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path

OUTPUT_FIELDS = [
    "assembly_method",
    "total_length_bp",
    "n50_bp",
    "contig_count",
    "busco_complete_percent",
]


def parse_number(value: str) -> float | int | None:
    value = value.strip().replace(",", "")
    if not value or value in {"-", "NA", "N/A"}:
        return None
    match = re.search(r"-?\d+(?:\.\d+)?", value)
    if not match:
        return None
    number = float(match.group())
    return int(number) if number.is_integer() else number


def read_quast(path: Path) -> dict[str, dict[str, float | int | None]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        rows = list(csv.reader(handle, delimiter="\t"))
    if not rows:
        raise ValueError(f"Empty QUAST report: {path}")
    header = [cell.strip() for cell in rows[0]]
    if len(header) < 2:
        raise ValueError("Expected QUAST report.tsv with metric column and assembly columns.")
    assemblies = header[1:]
    aliases = {
        "Total length": "total_length_bp",
        "N50": "n50_bp",
        "# contigs": "contig_count",
        "# contigs (>= 0 bp)": "contig_count",
    }
    output = {name: {field: None for field in OUTPUT_FIELDS[1:]} for name in assemblies}
    found = set()
    for row in rows[1:]:
        if not row:
            continue
        metric = row[0].strip()
        field = aliases.get(metric)
        if not field:
            continue
        found.add(field)
        for index, name in enumerate(assemblies, start=1):
            value = row[index] if index < len(row) else ""
            parsed = parse_number(value)
            # Prefer the exact "# contigs" metric over a threshold-specific variant.
            if field == "contig_count" and metric != "# contigs" and output[name][field] is not None:
                continue
            output[name][field] = parsed
    if not {"total_length_bp", "n50_bp", "contig_count"} & found:
        raise ValueError("No recognized QUAST metrics found. Check report.tsv format.")
    return output


def read_busco_percent(path: Path) -> float | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    patterns = [
        r"\bC:\s*(\d+(?:\.\d+)?)\s*%",
        r"Complete BUSCOs?\s*\(C\)\s*:\s*(\d+(?:\.\d+)?)\s*%",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = float(match.group(1))
            if 0 <= value <= 100:
                return value
    raise ValueError(f"Could not find a BUSCO complete percentage in {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--quast", required=True, type=Path, help="QUAST report.tsv")
    parser.add_argument("--out", default=Path("assembly_metrics.csv"), type=Path)
    parser.add_argument(
        "--busco", action="append", default=[], metavar="LABEL=FILE",
        help="Optional BUSCO short_summary file for an assembly; repeat as needed.",
    )
    args = parser.parse_args()

    if not args.quast.is_file():
        parser.error(f"QUAST report not found: {args.quast}")
    try:
        data = read_quast(args.quast)
        busco = {}
        for item in args.busco:
            if "=" not in item:
                raise ValueError(f"Invalid --busco value {item!r}; use LABEL=FILE.")
            label, filename = item.split("=", 1)
            if not label or not Path(filename).is_file():
                raise ValueError(f"Invalid BUSCO label or missing file: {item!r}")
            busco[label] = read_busco_percent(Path(filename))

        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            for label, metrics in data.items():
                row = {"assembly_method": label, **metrics}
                if label in busco:
                    row["busco_complete_percent"] = busco[label]
                writer.writerow(row)
    except (OSError, ValueError) as exc:
        parser.error(str(exc))

    print(f"Wrote metrics extracted from supplied reports: {args.out}")
    print("Review labels and values against the original QUAST/BUSCO reports before publication.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
