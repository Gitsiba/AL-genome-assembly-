# AL-genome-assembly-
aeluropus lagopoides full genome assembly 
# Genome Assembly Pipelines

This repository contains descriptions of different genome assembly pipelines.

## 1. Comparison of Different Genome Assemblies

*(Include the information and image from the first document here)*

**Figure 3**: Comparison between different genome assembly methods based on key quality metrics:

* **N50 (blue)**: Measures assembly contiguity; higher values indicate better assemblies.
* **Genome Size (green)**: Estimated genome size in megabases (Mb) for each assembly approach.
* **BUSCO Score (orange)**: Assesses genome completeness based on conserved orthologs; higher scores suggest better assemblies.
* **Contigs (red)**: Represents genome fragmentation; fewer contigs indicate a more contiguous assembly.

**Three assembly strategies are evaluated:**

* **Hybrid (MaSuRCA)**: Combines short and long reads for improved accuracy.
* **Long Reads (WTDBG2)**: Uses only long-read sequencing for assembly.
* **Short Reads (Velvet)**: Uses only short-read sequencing, resulting in highly fragmented assemblies.

**Key Observations:**

This comparison highlights that **hybrid assembly** provides the best balance between contiguity, completeness, and genome size accuracy.

## 2. Genome Assembly Pipelines

*(Include the pipeline descriptions from the second document here)*

Here's a breakdown of the pipelines:

### 2.1. De Novo Assembly Pipeline Using Long Read Sequences

* **Description:** This pipeline uses long-read sequencing data (like PacBio) to create a genome assembly.  Long reads are advantageous because they can span repetitive regions, which simplifies the assembly process.

* **Steps:**

    1.  **Long Read Data:** Input is raw long-read sequence data.
    2.  **CCS File (BAM to Fastq):** If the long reads are in BAM format...
    3.  **NanoStats:** Quality assessment of the long reads.
    4.  **Assembler:** The assembly process.
    5.  **BUSCO and QUAST:** Quality assessment of the final genome assembly.

* **Code-like Representation:**

    ```
    long_reads = "input.bam"
    if file_format(long_reads) == "bam":
        fastq_reads = samtools_bam_to_fastq(long_reads)
    else:
        fastq_reads = long_reads
    nano_stats_report = nanoplot(fastq_reads)
    assembly = hifiasm(fastq_reads) # or wtdbg2(fastq_reads) or flye(fastq_reads)
    busco_report = busco(assembly)
    quast_report = quast(assembly)
    ```

### 2.2. De Novo Assembly Pipeline Using Short Read Sequences and Polished Assembly for Validation

* **Description:** This pipeline uses short-read sequencing data...

* **Steps:**
     1. **Short read data**
     2. **FastQC**
     3. **Fastp**
     4. **Assembler**
     5. **Polished assembly (flye long + short reads)**
     6. **Pilon for polished assembly**
     7. **QC check**
     8.  **BUSCO and QUAST**
* **Code-like Representation:**

    ```
    short_reads_1 = "reads1.fastq"
    short_reads_2 = "reads2.fastq"
    fastqc_report = fastqc([short_reads_1, short_reads_2])
    trimmed_reads_1, trimmed_reads_2 = fastp([short_reads_1, short_reads_2])
    assembly = spades([trimmed_reads_1, trimmed_reads_2])
    polished_assembly = pilon(assembly, trimmed_reads_1, trimmed_reads_2)
    qc_check(polished_assembly)
    busco_report = busco(polished_assembly)
    quast_report = quast(polished_assembly)
    ```

### 2.3. Pipeline for Making Hybrid Assembly (Long Reads + Short Reads)

 * **Description**: This pipeline combines long-read and short-read data.
 * **Steps**:
     1. **Long reads (PacBio)**
     2. **Short reads (Illumina)**
     3. **Assembler (MaSuRCA)**
     4.  **BUSCO and QUAST**
 * **Code-like Representation:**

     ```
     long_reads = "pacbio_reads.fastq"
     short_reads_1 = "illumina_reads_1.fastq"
     short_reads_2 = "illumina_reads_2.fastq"
     assembly = masurca(long_reads, short_reads_1, short_reads_2)
     busco_report = busco(assembly)
     quast_report = quast(assembly)
