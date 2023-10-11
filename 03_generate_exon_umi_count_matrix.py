
# Combine the UMI count data from each cell
# exon reads

import os
import pandas as pd

os.chdir('[Your directory]')

id2symbol = {}
gene_file = open('[Your directory]/human_gene_list.txt', 'r')

gene_list = []

for line in gene_file:
	line_list = line.strip('\n').split('\t')
	id2symbol[line_list[0]] = line_list[1]
	gene_list.append(line_list[0])
gene_file.close()

del line
del line_list
expression_dict = {}
sample_file = open("[Your cell list]", "r")
sample_list = []
for line in sample_file:
	sample = line.strip('\n')
	print(sample)
	sample_list.append(sample)
	expression_dict[sample] = []
	filename = sample + '/split_exon_intron/' + sample + '.exon_barcode_count.txt'
	df = pd.read_table(filename, header=0, index_col = 'Gene_id')
	for gene in gene_list:
		expression_dict[sample].append(df.loc[gene, 'UMI_count'])
	del df
sample_file.close()

expression_dict['gene_symbol'] = []
for gene in gene_list:
	expression_dict['gene_symbol'].append(id2symbol[gene])

column_names = ['gene_symbol'] + sample_list

count_df = pd.DataFrame(expression_dict, columns = column_names, index = gene_list)
count_df.to_csv('[Your output file name]', sep = '\t', index = True, header = True)





