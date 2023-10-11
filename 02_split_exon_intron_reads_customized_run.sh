#!/bin/bash


date
sample=['Your sample name']
datadir=['Your directory']/${sample}

wd=${datadir}/split_exon_intron	# working directory

mkdir $wd
cd $wd

samtools view -b -q 250 ${datadir}/Aligned.r1.bam | samtools sort - > r1.bam
samtools index r1.bam

# HTseq-count for exon
htseq-count -s no -t exon -m intersection-strict -f bam r1.bam ['Your directory to gene annotation file, e.g.,gencode.v19.annotation.gtf'] -q -o htseq_mappedr1.exon.sam > htseqr1.exon.out

python ['Your directory']/readtaggene_Htseqcount_py38.py htseq_mappedr1.exon.sam > r1tagmapped.exon.dat

seqtk subseq ${datadir}/${sample}_2.fq.gz r1tagmapped.exon.dat > ${sample}-mapped-r2.exon.fastq

python ['Your directory']/barcodeseq_extract.py ${sample}-mapped-r2.exon.fastq r1tagmapped.exon.dat > ${sample}_mapped_barcode.exon.dat

# HTseq-count for transcript
htseq-count -s no -t transcript -m intersection-strict -f bam r1.bam ['Your directory to gene annotation file, e.g.,gencode.v19.annotation.gtf'] -q -o htseq_mappedr1.transcript.sam > htseqr1.transcript.out

python ['Your directory']/readtaggene_Htseqcount_py38.py htseq_mappedr1.transcript.sam > r1tagmapped.transcript.dat

seqtk subseq ${datadir}/${sample}_2.fq.gz r1tagmapped.transcript.dat > ${sample}-mapped-r2.transcript.fastq

python ['Your directory']/barcodeseq_extract.py ${sample}-mapped-r2.transcript.fastq r1tagmapped.transcript.dat  > ${sample}_mapped_barcode.transcript.dat

python ['Your directory']/count_exon_intron_UMI.py ${sample}

gzip ${sample}-mapped-r2.exon.fastq
gzip ${sample}-mapped-r2.transcript.fastq

exit 0