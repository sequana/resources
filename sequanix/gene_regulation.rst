Gene regulation example
============================

This page shows how to load and execute a Snakemake pipeline from the Gene-regulation library (Rioualen et al). 
Tutorial available on gene-regulation documentation web page http://gene-regulation.readthedocs.io/en/latest/tutorials.html

We will use one of the pipeline for the demonstration that is the ChIP-seq pipeline. 

Independently of Sequana/Sequanix we will first need to install Gene-regulation package itself and then a set of data files to play with. 


The following pipeline (ChIP-seq) depends on the gene-regulation library. The pipeline requires some data to be copied in the the directory where will be installed the library. So let us first define a directory.

Create workdir
--------------
::

    # Create a working and analysis directory at the top level
    export ANALYSIS_DIR=~/test_sequanix_gene-regulation
    mkdir ${ANALYSIS_DIR}
    cd ${ANALYSIS_DIR}

Download gene-regulation library
-------------------------------

::

    wget --no-clobber https://github.com/rioualen/gene-regulation/archive/4.0.tar.gz
    tar xvzf 4.0.tar.gz
    ln -s gene-regulation-4.0 gene-regulation

Install dependencies with Conda
-------------------------------

To not interfere with your system, let us create a new conda environment from scratch::

    conda create --name genereg python=3.5
    source activate genereg

and install all dependencies including sequana itself::

    conda install fastqc bowtie2 bedtools samtools graphviz deeptools
    conda install r-essentials bioconductor-deseq2 bioconductor-edger
    conda install -c bioconda bioconductor-mosaics=2.10.0
    conda install sequana

For MACS2, note that only the version for Python2.7 is available (no Python 3 in June 2017). So, since we used conda for version 3 of Python, one need to trick the system using **pip2**, which is the **pip** version for Python2.7. Most distributions are still using Python2 so you should have the utility available. Type this command to install macs2 globally::

    pip2 install macs2

of if you do not have root permission::

    pip2 install --user macs2


For homer software, follow the instructions here : http://homer.ucsd.edu/homer/introduction/install.html 
This summarised set of instructions should work on a linux box::

    wget http://homer.ucsd.edu/homer/configureHomer.pl
    perl configureHomer.pl -install
    export PATH=$PATH:$PWD/bin                # This should be added to you bashrc environemnt

**Warning** Be careful, the python version used for MACS2 and Homer must be 2.7!





Download genome and annotations
-------------------------------------

Genome assembly: sacCer3::

    wget -nc ftp://ftp.ensemblgenomes.org/pub/fungi/release-30/fasta/saccharomyces_cerevisiae/dna/Saccharomyces_cerevisiae.R64-1-1.30.dna.genome.fa.gz -P ${ANALYSIS_DIR}/genome
    wget -nc ftp://ftp.ensemblgenomes.org/pub/fungi/release-30/gff3/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.30.gff3.gz -P ${ANALYSIS_DIR}/genome
    wget -nc ftp://ftp.ensemblgenomes.org/pub/fungi/release-30/gtf/saccharomyces_cerevisiae/Saccharomyces_cerevisiae.R64-1-1.30.gtf.gz -P ${ANALYSIS_DIR}/genome
    gunzip ${ANALYSIS_DIR}/genome/*.gz

Download ChIP-seq data
--------------------------

From GEO series`GSE55357 <https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE55357>`_::

    wget --no-clobber ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR117/005/SRR1176905/SRR1176905.fastq.gz -P ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334674
    wget --no-clobber ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR117/007/SRR1176907/SRR1176907.fastq.gz -P ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334676
    wget --no-clobber ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR117/008/SRR1176908/SRR1176908.fastq.gz -P ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334679
    wget --no-clobber ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR117/000/SRR1176910/SRR1176910.fastq.gz -P ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334677


   gunzip -c ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334674/SRR1176905.fastq.gz > ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334674/GSM1334674.fastq; rm -f ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334674/SRR1176905.fastq.gz
   gunzip -c ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334676/SRR1176907.fastq.gz > ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334676/GSM1334676.fastq; rm -f ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334676/SRR1176907.fastq.gz
   gunzip -c ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334679/SRR1176908.fastq.gz > ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334679/GSM1334679.fastq; rm -f ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334679/SRR1176908.fastq.gz
   gunzip -c ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334677/SRR1176910.fastq.gz > ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334677/GSM1334677.fastq; rm -f ${ANALYSIS_DIR}/ChIP-seq_GSE55357/fastq/GSM1334677/SRR1176910.fastq.gz
    
    
Run the workflow with sequanix
--------------------------------

As for the minimalist example, you must select the Snakefile called gene-regulation/scripts/snakefiles/workflows/ChIP-seq.wf
and the gene-regulation/examples/ChIP-seq\_GSE55357. The output directory will be ${ANALYSIS_DIR}

.. image:: sequanix-regulation.png
    :width: 30%


**Warning**: the output directory must contain the gene-regulation library.



