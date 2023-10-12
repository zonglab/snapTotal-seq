
# readtag-gene
# HTseq-count py3.8

import sys

fi = open(sys.argv[1], 'r')

for read_line in fi:
	read_info = read_line.strip('\n').split('\t')
	read_id = read_info[0]
	gene_mapping = read_info[-1].split(':')[2]
	if gene_mapping[:2] != '__':
		print(read_id, gene_mapping)

fi.close()


