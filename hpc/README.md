# HPC / Slurm notes

This folder contains a **template**, not a confirmed CV Raman job submission script.

## Before using it

1. Confirm the cluster's supported container runtime (Apptainer or Singularity) and how to load it.
2. Ask the HPC team for the appropriate CPU, memory, wall-time, and partition/account directives for MaSuRCA. Do not guess these values.
3. Transfer or locate the read files and configuration in a project directory visible to compute nodes.
4. Review the MaSuRCA config and ensure every read path in it is valid inside the container. The template bind-mounts only `PROJECT_DIR` at `/work`.
5. Convert/pull the tested assembly image to a cluster-readable Apptainer/Singularity image if cluster policy permits. The image built by GitHub Actions is not automatically present on CV Raman.

## Safe preflight

After the administrator confirms the runtime and the image is available, edit the resource directives at the top of `masurca.sbatch.template` according to local policy. Copy the template to `masurca.sbatch` and set real paths:

```bash
export PROJECT_DIR=/path/to/project
export CONTAINER_IMAGE=/path/to/al-genome-assembly.sif
export MASURCA_CONFIG=/path/to/project/config.txt
export CONTAINER_RUNTIME=apptainer
export RUN_ASSEMBLY=NO
sbatch masurca.sbatch
```

The safe default only checks the image and MaSuRCA command; it does not launch the assembly. Check the Slurm log before proceeding.

## Explicit assembly launch

Only after the config, read paths, image, storage, and resource request have been reviewed, set `RUN_ASSEMBLY=YES` and submit the job. The script then runs `masurca config.txt` and executes the generated `assemble.sh`. MaSuRCA may require substantial compute time and storage, so follow local HPC guidance and monitor the job.

## Current scientific status

This repository's documented work is at the contig-assembly stage. This template does not claim that an assembly has been run, reproduced, scaffolded, annotated, or validated on CV Raman. No biological results or assembly metrics should be added until supported by actual outputs.
