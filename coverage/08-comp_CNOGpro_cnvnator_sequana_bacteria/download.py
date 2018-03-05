"""Download the 6 isolates from CNOGpro suppl data, get the BAM and BED files"""
import subprocess


cmd1 = "wget ftp://ftp.sra.ebi.ac.uk/vol1/fastq/{}/{}/{}_{}.fastq.gz -c -N"
cmd2 = "sequana_coverage --download-reference FN433596"
cmd3 = "sequana_mapping --file1 {}_1.fastq.gz --file2 {}_2.fastq.gz --reference FN433596.fa  "
cmd4 = "mv FN433596.fa.sorted.bam {}.bam; bedtools genomecov -d -ibam {}.bam > {}.bed"



subprocess.call(cmd2, shell=True)
for this in ["ERR043375", "ERR316404", "ERR142616", "ERR043379","ERR043367", "ERR043371"]:
    # R1
    print(cmd1.format(this[0:6], this, this, 1).split())
    subprocess.call(cmd1.format(this[0:6], this, this, 1), shell=True)
    # R2
    subprocess.call(cmd1.format(this[0:6], this, this, 2), shell=True)
    # mapping
    subprocess.call(cmd3.format(this, this), shell=True)
    # BAM to BED
    subprocess.call(cmd4.format(this, this, this), shell=True)
