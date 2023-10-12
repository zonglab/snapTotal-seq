
# separate exonic and intronic reads

import sys

sample = sys.argv[1]

def compare_readID(exon_read_list, transcript_read_list):
	spliced = True
	for read_id in transcript_read_list:
		if read_id in exon_read_list:
			continue
		else:
			spliced = False
			break
	if spliced:
		return 'exon'
	else:
		return 'intron'


# Initializing 
transcript_dict = {}	# Gene: UMI
exon_dict = {}	# Gene: UMI
id2symbol = {}	# gene_id: gene_symbol

# import gene list
gene_fi = open('[Your directory]/human_gene_list.txt', 'r')
for gene in gene_fi:
	id2symbol[gene.strip('\n').split('\t')[0]] = gene.strip('\n').split('\t')[1]
	transcript_dict[gene.strip('\n').split('\t')[0]] = {}
	exon_dict[gene.strip('\n').split('\t')[0]] = {}
gene_fi.close()

print(len(id2symbol))

# transcript-mapped amplicons
del gene
transcript_mapping_fi = open(sample + '_mapped_barcode.transcript.dat', 'r')
for mapping_line in transcript_mapping_fi:
	mapping_info = mapping_line.strip('\n').split(' ')
	read_id = mapping_info[0]
	gene = mapping_info[1]
	bcd = mapping_info[2][0:5]
	if bcd in transcript_dict[gene]:
		transcript_dict[gene][bcd].append(read_id)
	else:
		transcript_dict[gene][bcd] = [read_id]
transcript_mapping_fi.close()

# exon-mapped amplicons
del mapping_line
del mapping_info
del gene
del bcd
del read_id
exon_mapping_fi = open(sample + '_mapped_barcode.exon.dat', 'r')
for mapping_line in exon_mapping_fi:
	mapping_info = mapping_line.strip('\n').split(' ')
	read_id = mapping_info[0]
	gene = mapping_info[1]
	bcd = mapping_info[2][0:5]
	if bcd in exon_dict[gene]:
		exon_dict[gene][bcd].append(read_id)
	else:
		exon_dict[gene][bcd] = [read_id]
exon_mapping_fi.close()

# Separate exon and intron UMI for each gene
del bcd
del read_id
del gene
intron_count = {}	# gene_id: umi count
exon_count = {}	# gene_id: umi count
gene_list = id2symbol.keys()

for gene in gene_list:
	intron_count[gene] = 0
	exon_count[gene] = 0
	if len(transcript_dict[gene]) == 0:
		continue
	else:
		for bcd in transcript_dict[gene]:
			if bcd in exon_dict[gene]:
				res = compare_readID(exon_dict[gene][bcd], transcript_dict[gene][bcd])
				if res == 'exon':
					exon_count[gene] += 1
				else:
					intron_count[gene] += 1
			else:
				intron_count[gene] += 1

print('Finish separation.')

transcript_fo = open(sample + '.transcript_barcode_count.txt', 'w')
transcript_fo.write('Gene_id' + '\t' + 'Gene_name' + '\t' + 'UMI_count' + '\n')
exon_fo = open(sample + '.exon_barcode_count.txt', 'w')
exon_fo.write('Gene_id' + '\t' + 'Gene_name' + '\t' + 'UMI_count' + '\n')
intron_fo = open(sample + '.intron_barcode_count.txt', 'w')
intron_fo.write('Gene_id' + '\t' + 'Gene_name' + '\t' + 'UMI_count' + '\n')

del gene
for gene in gene_list:
	transcript_fo.write(gene + '\t' + id2symbol[gene] + '\t' + str(len(transcript_dict[gene])) + '\n')
	exon_fo.write(gene + '\t' + id2symbol[gene] + '\t' + str(exon_count[gene]) + '\n')
	intron_fo.write(gene + '\t' + id2symbol[gene] + '\t' + str(intron_count[gene]) + '\n')

transcript_fo.close()
exon_fo.close()
intron_fo.close()






