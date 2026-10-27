# *Aeluropus lagopoides* Genome Assembly

A reproducible project documenting genome assembly strategies for *Aeluropus lagopoides*, a salt-tolerant grass. The repository currently contains a project poster, pipeline-diagram code, an assembly-comparison plotting script, and notes on short-read, long-read, and hybrid assembly workflows.

> **Reproducibility note:** The repository's plotting script previously contained illustrative example values. Those values are not verified project results and must not be interpreted as measurements from the *A. lagopoides* assembly. The updated script reads a user-supplied metrics table instead.

## Project goals

- Document the assembly approaches considered for the project.
- Compare assembly contiguity, assembly size, and completeness using metrics from actual output reports.
- Make analysis figures reproducible from a clearly documented input table.
- Preserve the distinction between planned workflows and steps/results confirmed to have been run.

## Assembly strategies documented

### 1. Hybrid assembly

Combines long-read and Illumina short-read data. The repository documents MaSuRCA as the hybrid assembler considered for this workflow.

**Inputs:** long-read FASTQ data and paired-end short-read FASTQ files.  
**Quality assessment:** QUAST and BUSCO, where suitable reference lineages and inputs are available.

### 2. Long-read assembly

Uses long reads to help span repetitive regions. The existing pipeline-diagram script lists HiFiASM, WTDBG2, and Flye as possible assemblers; the correct choice depends on the sequencing technology and read type. For example, HiFiASM is intended for PacBio HiFi reads, while Flye supports several long-read types.

**Quality assessment:** read-level QC (for example, NanoPlot/NanoStats) and assembly-level assessment with QUAST and BUSCO where applicable.

### 3. Short-read assembly

Uses paired-end short reads. The existing notes list Velvet and SPAdes as possible assemblers. These are alternative workflows, not necessarily sequential steps.

**Quality assessment:** FastQC before/after trimming as appropriate, a short-read trimming tool such as fastp, and assembly assessment with QUAST and BUSCO.

> Tool selection should match the actual input technology and project protocol. The README describes candidate workflows; it does not claim that every listed assembler or polishing step was run.

## Assembly quality metrics

| Metric | What it tells you | Interpretation |
|---|---|---|
| Total assembly length | Sum of assembled sequence lengths | Compare with an independently justified genome-size estimate; larger is not automatically better |
| Contig N50 | Length at which contigs of that length or longer account for at least half of the assembly | Higher values generally indicate greater contiguity |
| Number of contigs | Degree of fragmentation | Fewer contigs can indicate greater contiguity, but should be considered with other metrics |
| BUSCO completeness | Recovery of expected conserved single-copy orthologs | Report complete, single-copy, duplicated, fragmented, and missing categories where available |
| GC content | Fraction of G/C bases | Useful descriptive metric; unexpected values can indicate contamination or unusual sequence composition |

Do not compare metrics across assemblies unless they were calculated consistently. Report the exact software, version, parameters, and input files.

## Repository contents

- `README.md` — project overview and reproducibility guidance.
- `Siba poster 16.02.2025 final edited.pdf` — project poster.
- `out_lay` — Python/Graphviz script that generates long-read, short-read, and hybrid pipeline diagrams.
- `plot_assembly` — Python plotting script that reads a metrics CSV and generates comparison plots.

## Reproduce the assembly comparison plot

Requirements: Python 3, pandas, and matplotlib.

Install dependencies:

```bash
python -m pip install pandas matplotlib
```

Create a CSV file named `assembly_metrics.csv` using this schema (one row per assembly):

```csv
assembly_method,total_length_bp,n50_bp,contig_count,busco_complete_percent
Hybrid,,
Long-read,,
Short-read,,
```

Replace the blank cells with values taken from the corresponding assembly reports. Leave BUSCO values blank if unavailable. Do not use invented or placeholder values in a final figure.

Run:

```bash
python plot_assembly assembly_metrics.csv --outdir figures
```

The script validates the input and writes one PNG per metric to `figures/`. Missing values are omitted from that metric's plot.

## Recommended results checklist

Before presenting a final comparison, record:

- [ ] Source/accession and sequencing technology for each read set
- [ ] Read QC and trimming reports, if trimming was performed
- [ ] Assembler names, versions, parameters, and commands
- [ ] Assembly FASTA file provenance
- [ ] QUAST report and BUSCO lineage/version and summary
- [ ] Assembly metrics table populated from actual outputs
- [ ] Figures generated from that table
- [ ] Limitations, including possible contamination, heterozygosity, repeats, and differences in input data

## Scientific interpretation

A hybrid approach may improve the balance between contiguity and base-level accuracy in some projects, but this must be demonstrated using the project's own results. Do not claim that one method is best until the same quality metrics have been calculated and compared fairly.

## Limitations

This repository is a project record and workflow documentation. A pipeline description or diagram alone does not prove that a workflow ran successfully. Numerical results should only be reported when traceable to the original assembler, QUAST, BUSCO, or other QC outputs.

## Citation and data provenance

When publishing or reusing the analysis, cite the source of each read dataset and the software used. Add accession IDs, software versions, and the project publication or poster citation here once verified.
