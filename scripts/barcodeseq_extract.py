
import sys
import pysam

# input file 1: read2 fastq
# input file 2: reads file
# read_id gene_id barcode

read_fi = open(sys.argv[2], 'r')
read_dict = {}	# read_id: {'gene_id':, 'bcd':}

for read_line in read_fi:
	read_id, gene_id = read_line.strip('\n').split(' ')
	read_dict[read_id] = {'Gene': gene_id, 'Barcode': ''}
read_fi.close()

del read_line
del read_id
del gene_id

fastq_fi = pysam.FastqFile(sys.argv[1])
for read in fastq_fi:
	if (len(read.sequence) >= 8) and (read.sequence[0:8].count('N') < 4):
		read_dict[read.name]['Barcode'] = read.sequence[0:8]
fastq_fi.close()
del read

for read in read_dict:
	if len(read_dict[read]['Barcode']) == 8:
		print(read, read_dict[read]['Gene'], read_dict[read]['Barcode'])
