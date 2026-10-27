# Containerized genome assembly (MaSuRCA)

This is a separate, resource-intensive image from the lightweight plotting image.

## Scope and evidence

The project poster lists PacBio HiFi long reads, Illumina NovaSeq 6000 short reads, MaSuRCA hybrid assembly, Flye long-read assembly, Pilon polishing, and BUSCO/QUAST/FastQC quality checks. The project milestone confirmed in this repository is contig-level assembly.

This document sets up an environment for a **MaSuRCA hybrid-assembly attempt**. It does not prove that this container reproduces the original historical run. Before describing it as an exact reproduction, confirm the original software version, configuration, read files, and parameters from the project records.

## 1. Build the assembly image

From the repository root:

```bash
docker build -f Dockerfile.assembly -t al-genome-assembly:assembly .
```

The image installs MaSuRCA 4.1.0 through Bioconda. Package availability and build success must be checked on the target platform. The image is separate from the default plotting image because assembly software has a different dependency and resource profile.

## 2. Prepare the working directory

Use a directory outside the repository for large read files and assembly outputs. Example layout:

```text
assembly_work/
├── pacbio_hifi.fastq.gz
├── illumina_R1.fastq.gz
├── illumina_R2.fastq.gz
└── config.txt
```

These are example filenames only. Replace them with the actual paired-end Illumina files and PacBio HiFi reads. Do not commit sequencing data to GitHub.

Check that files are readable and that paired-end files correspond to the same library/sample. Verify checksums and preserve original inputs.

## 3. Prepare the MaSuRCA configuration

Create `config.txt` using the configuration format documented for the installed MaSuRCA release. At minimum, the configuration must specify the actual Illumina paired-end read paths and PacBio HiFi read path, along with appropriate insert-size and resource parameters where required by that release.

**Do not copy guessed insert sizes or resource settings into a production run.** Use library QC records and the available machine's CPU, RAM, and storage limits. MaSuRCA configuration syntax can vary by release; validate against the installed version's examples/documentation.

## 4. Run MaSuRCA in the mounted work directory

```bash
cd /path/to/assembly_work

docker run --rm -it \
  -v "$PWD:/work" \
  -w /work \
  --entrypoint bash \
  al-genome-assembly:assembly
```

Inside the container, verify the installed version and generate the MaSuRCA assembly script:

```bash
masurca --help
masurca config.txt
```

If MaSuRCA successfully creates `assemble.sh`, inspect the generated script and then launch it:

```bash
bash assemble.sh
```

Assembly can take substantial time, RAM, and disk space. Do not assume the default container memory or storage limits are sufficient. Keep the terminal/session and container resources appropriate for the dataset; for long HPC runs, use the institution's supported container runtime and scheduler instead of relying on a short-lived interactive session.

## 5. Validate the output

After the run finishes, identify the final contig FASTA from the output directory produced by the installed MaSuRCA version. Record the exact output path, command, configuration, image tag, MaSuRCA version, runtime, and exit status.

Then assess the contigs with QUAST and, where appropriate, BUSCO using a justified lineage. Keep their reports with the run record. Populate `assembly_metrics_template.csv` only with measured values from these reports.

## Current limitations

- This is an assembly-environment starting point, not a verified end-to-end reproduction of the original project.
- The poster mentions Flye, Pilon, BUSCO, QUAST, FastQC, Augustus, BRAKER, and Bionano OGM. They are not all installed in this MaSuRCA image.
- Pilon polishing requires compatible read alignments and a carefully validated workflow; it is not automatically run here.
- Bionano OGM scaffolding and gene annotation are downstream workflows and are intentionally outside the contig-generation container at this stage.
- The Docker image build and assembly run must be tested in the user's environment before claiming success.
