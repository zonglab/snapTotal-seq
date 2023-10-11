#!/bin/bash

date
sample=['Your sample name']

wd=['Your directory']/${sample}

seqdir=['Your directory of raw sequencing data']

mkdir -p $wd

cd $wd

echo ${sample}

mv ${seqdir}/${sample}_*.fq.gz ./

# Optional: remove adapter sequence
# Recommended if the read length of read 1 exceeds the insert size of your library. 
cutadapt -a CTCCACACATCCTCAACCATCACTCAC -o ${sample}_adapter_trimmed_1.fq.gz ${sample}_1.fq.gz > adapter_trimming_report.txt

# Optional: remove potential UMI sequence
# Recommended if the read length of read 1 exceeds the insert size of your library. 
cutadapt -u -10 -m 30 -o ${sample}_UMItrimmed_1.fq.gz ${sample}_adapter_trimmed_1.fq.gz > UMI_trimming_report.txt
rm ${sample}_adapter_trimmed_1.fq.gz

# mapping read1
STAR --runThreadN ['Threads num'] --runMode alignReads --genomeDir ['Your directory to STAR index folder'] --outFilterMismatchNmax 5 --readFilesCommand zcat --readFilesIn ${sample}_UMItrimmed_1.fq.gz --outSAMtype BAM Unsorted

samtools sort Aligned.out.bam -o  Aligned.r1.bam
rm -rf Aligned.out.bam

exit 0

