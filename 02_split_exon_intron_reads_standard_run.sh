#!/bin/bash


date
sample=['Your sample name']
datadir=['Your directory']/${sample}

wd=${datadir}/split_exon_intron # working directory

mkdir $wd
cd $wd

samtools view -b -q 250 ${datadir}/Aligned.r1.bam | samtools sort - > r1.bam
samtools index r1.bam

# remove the adapter sequence in read 2
# This trimming step removes the first 43 bases (8-base cell barcode + 35-base adapter) of read 2
cutadapt -g AGGAGAGTGTGAGTGATGGTTGAGGATGTGTGGAG -o ${sample}_trimmed_2.fq.gz ${datadir}/${sample}_2.fq.gz > read2_trimming_report.txt

# mapped to exon
htseq-count -s no -t exon -m intersection-strict -f bam r1.bam ['Your directory to gene annotation file, e.g.,gencode.v19.annotation.gtf'] -q -o htseq_mappedr1.exon.sam > htseqr1.exon.out

python ['Your directory']/readtaggene_Htseqcount_py38.py htseq_mappedr1.exon.sam > r1tagmapped.exon.dat

seqtk subseq ${sample}_trimmed_2.fq.gz r1tagmapped.exon.dat > ${sample}-mapped-r2.exon.fastq

python ['Your directory']/barcodeseq_extract_standard_run.py ${sample}-mapped-r2.exon.fastq r1tagmapped.exon.dat ['Read2_length - 43'] > ${sample}_mapped_barcode.exon.dat
# The third parameter corresponds to the length of read2 after trimming.

# mapped to transcript
htseq-count -s no -t transcript -m intersection-strict -f bam r1.bam ['Your directory to gene annotation file, e.g.,gencode.v19.annotation.gtf'] -q -o htseq_mappedr1.transcript.sam > htseqr1.transcript.out

python ['Your directory']/readtaggene_Htseqcount_py38.py htseq_mappedr1.transcript.sam > r1tagmapped.transcript.dat

seqtk subseq ${sample}_trimmed_2.fq.gz r1tagmapped.transcript.dat > ${sample}-mapped-r2.transcript.fastq 

python ['Your directory']/barcodeseq_extract_standard_run.py ${sample}-mapped-r2.transcript.fastq r1tagmapped.transcript.dat ['Read2_length - 43'] > ${sample}_mapped_barcode.transcript.dat
# The third parameter corresponds to the length of read2 after trimming.

python ['Your directory']/count_exon_intron_UMI.py ${sample}

gzip ${sample}-mapped-r2.exon.fastq
gzip ${sample}-mapped-r2.transcript.fastq

exit 0


