# cell index demultiplex

import pysam
import sys

def Hamming_distance(seq1, seq2):
	distance = 0
	for i, j in zip(seq1, seq2):
		if i != j:
			distance += 1
	return distance

mismatch_cutoff = int(sys.argv[3])

# input index list
index_fi = open('[Your directory]/cell_index_list.txt', 'r')
index_list = index_fi.readlines()
index_list = [i.strip('\n') for i in index_list]
index_fi.close()

# output the assigned index of each read
fo = open(sys.argv[2], 'w')

# input read 2 file
fastq = pysam.FastqFile(sys.argv[1])
for read in fastq:
	index = read.sequence[0:8]
	for core_index in index_list:
		dist = Hamming_distance(index, core_index)
		if dist <= mismatch_cutoff:
			fo.write(read.name + '\t' + core_index + '\n')
			break

fo.close()
fastq.close()

print('Extract the cell index.')




