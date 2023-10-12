#!/bin/bash

datadir='[Your directory]'

lib_id='[Sub-library ID]' # each sub-library is first demultiplexed based on i5 index using standard Illumina demultiplex pipeline

cd ${datadir}

read1='[read 1 file name]'
read2='[read 2 file name]'

gzip -d ${read2}.fq.gz

python ['Your directory']/Extract_cell_index.py ${read2}.fq ${lib_id}_read_index.txt 

gzip ${read2}.fq

cat '[Your directory]'/cell_index_list.txt | while read LINE
do
	grep ${LINE} ${lib_id}_read_index.txt > ${lib_id}_${LINE}.txt
	
	seqtk subseq ${read1}.fq.gz ${lib_id}_${LINE}.txt > ${lib_id}_${LINE}_1.fq
	gzip ${lib_id}_${LINE}_1.fq
	
	seqtk subseq ${read2}.fq.gz ${lib_id}_${LINE}.txt > ${lib_id}_${LINE}_2.fq
	gzip ${lib_id}_${LINE}_2.fq
done


