# *Aeluropus lagopoides* Genome Assembly

## Project overview

This project focuses on genome assembly of *Aeluropus lagopoides*, a salt-tolerant grass. **The assembly work was carried through to the contig level.** This is a draft contig assembly milestone; it should not be described as chromosome-level or fully scaffolded unless further evidence confirms that stage.

The repository documents assembly strategies and quality-assessment concepts, and includes the project poster, pipeline-diagram code, and a plotting script for comparing assembly metrics.

## Project accomplishment

- Worked on the *A. lagopoides* genome assembly through the **contig-level assembly stage**.
- Documented short-read, long-read, and hybrid assembly strategies relevant to the project.
- Identified assembly-quality measures used to evaluate draft assemblies, including contiguity, total assembly length, contig count, and BUSCO completeness where available.
- Added a Docker environment for reproducible assembly-metric plotting and pipeline diagram generation.

**Scope statement:** The confirmed project milestone stated here is contig-level assembly. This README does not claim chromosome-level assembly, scaffolding, gap closure, or any specific N50, genome size, BUSCO score, or contig count without values traceable to the original reports.

## Assembly strategies documented

### Hybrid assembly

Combines long-read and Illumina short-read data. The repository documents MaSuRCA as a hybrid assembler considered for this workflow.

### Long-read assembly

Long reads can help span repetitive regions. The existing pipeline-diagram script lists HiFiASM, WTDBG2, and Flye as candidate assemblers. Tool choice depends on the actual sequencing technology and read type.

### Short-read assembly

Uses paired-end short reads. The existing notes list Velvet and SPAdes as candidate assemblers. These are alternative approaches, not necessarily sequential steps.

> These sections document strategies and tools; they do not imply that every listed assembler or polishing step was used for the final assembly. Cite the actual tool/version and commands used when adding detailed methods.

## Docker implementation

The repository now has two separate container paths:

- **Plotting image** (`Dockerfile`): Python plotting dependencies and Graphviz for metric plots and pipeline diagrams.
- **Assembly image** (`Dockerfile.assembly`): a separate MaSuRCA 4.1.0 environment intended for a hybrid contig-assembly attempt using the actual PacBio HiFi and Illumina inputs.

The assembly image and instructions are a starting point and have not been verified against the original historical run or the user's dataset. See [ASSEMBLY_DOCKER.md](ASSEMBLY_DOCKER.md) for input preparation, configuration, execution, and validation steps. Do not claim a successful assembly until the image builds and the workflow completes with the real inputs.

### Build the image

From the repository root:

```bash
docker build -t al-genome-assembly .
```

### Check the plotting command

```bash
docker run --rm al-genome-assembly --help
```

### Generate plots from your own assembly metrics

Copy the template and fill in values taken from actual assembly reports:

```bash
cp assembly_metrics_template.csv assembly_metrics.csv
```

Then run from the repository root (Linux/macOS shell):

```bash
docker run --rm \
  -v "$PWD:/work" \
  al-genome-assembly \
  assembly_metrics.csv --outdir figures
```

The output files will appear in the local `figures/` directory. Blank metrics are skipped; at least one actual numeric metric is required. Do not use example or invented values as observed results.

### Run the synthetic plotting smoke test

This uses clearly labelled synthetic metrics and verifies that the expected PNG files are generated. It is a software test only; these values are not *A. lagopoides* results.

```bash
bash tests/smoke_test_plotting.sh al-genome-assembly:plot
```

### Generate pipeline diagrams

The `out_lay` script uses Graphviz and is included in the image. Run it with the repository mounted so the PNG diagrams are saved into the working directory:

```bash
docker run --rm --entrypoint python \
  -v "$PWD:/work" -w /work \
  al-genome-assembly /app/out_lay
```

### Docker files

- `Dockerfile` — Python base image, Graphviz system package, and project dependencies.
- `requirements.txt` — Python dependencies.
- `.dockerignore` — excludes Git metadata, caches, and common large sequencing files from the build context.
- `.github/workflows/docker.yml` — builds the image and checks the plotting CLI on pushes and pull requests.

## Assembly quality metrics

| Metric | What it tells you | Interpretation |
|---|---|---|
| Total assembly length | Sum of assembled sequence lengths | Compare with an independently justified genome-size estimate |
| Contig N50 | Contig length at which contigs of that length or longer make up at least half of the assembly | Higher values generally indicate greater contiguity |
| Number of contigs | Degree of fragmentation | Interpret alongside N50, assembly length, and completeness |
| BUSCO completeness | Recovery of expected conserved orthologs | Report complete, single-copy, duplicated, fragmented, and missing categories when available |
| GC content | Fraction of G/C bases | Useful descriptive measure and possible contamination signal |

Metrics should be calculated consistently and reported with software versions, parameters, and input provenance.

## Repository contents

- `README.md` — project scope, methods overview, and reproducibility notes.
- `Siba poster 16.02.2025 final edited.pdf` — project poster.
- `out_lay` — Python/Graphviz script for long-read, short-read, and hybrid pipeline diagrams.
- `plot_assembly` — Python script that plots metrics from a user-supplied CSV.
- `assembly_metrics_template.csv` — blank template for entering measured assembly metrics.
- `Dockerfile`, `requirements.txt`, `.dockerignore` — plotting container setup.
- `Dockerfile.assembly` and `ASSEMBLY_DOCKER.md` — separate MaSuRCA assembly environment and cautious run instructions.
- `tests/smoke_test_plotting.sh` — synthetic-data smoke test that verifies the four metric plots are produced.
- `.github/workflows/docker.yml` — automated build and smoke tests for the plotting image, plus a MaSuRCA image build and command check.

## Run plotting without Docker

Install requirements:

```bash
python -m pip install -r requirements.txt
```

Fill `assembly_metrics.csv` from actual reports, then run:

```bash
python plot_assembly assembly_metrics.csv --outdir figures
```

The script generates a separate PNG for each metric that has numeric values.

## Recommended reporting checklist

- [ ] Record sequencing dataset/source and technology.
- [ ] Record assembler name, version, parameters, and commands actually used.
- [ ] Preserve the final contig FASTA and its provenance.
- [ ] Record total assembly length, N50, contig count, and other values from the actual reports.
- [ ] Add QUAST and, where appropriate, BUSCO reports and lineage/version.
- [ ] Generate plots from the measured metrics table.
- [ ] Describe limitations, including possible contamination, heterozygosity, repeats, and differences between input datasets.

## Interpretation and limitations

Reaching contig level is a meaningful draft genome assembly milestone, but it does not by itself establish chromosome-level completeness or validate assembly accuracy. Hybrid assembly may improve contiguity or accuracy in some datasets; any claim that one strategy performed best must be supported by comparable project-specific results.

## Data provenance and citation

When sharing or publishing this work, cite the read dataset(s), software, and project poster/publication as appropriate. Add accession identifiers, software versions, and verified assembly statistics when these are available from the original records.
