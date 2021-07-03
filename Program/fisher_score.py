##################################################################
# This program calculates the fisher score of each feature.
# Usage: python3 fisher_score.py begin_col file_nums file1 file2 ...
# The first cloume is 0
###################################################################

import sys
import math

def main():
	if len(sys.argv) < 3:
		print("Usage: python3 fisher_score.py begin_col file_nums file1 file2 ...")
		sys.exit(1)
	
	begin_column = int(sys.argv[1])
	n_files = int(sys.argv[2])
	filename = [""] * n_files
	for i in range(n_files):
		filename[i] = sys.argv[3 + i]
	
	# get feature name from the first line of each file	
	f_in = open(filename[0])
	line = f_in.readline()
	line = line.replace("\n", "")
	feature = line.split(",")
	f_in.close()

	num = [[0 for x in range(len(feature))] for y in range(n_files)]
	s = [[float(0) for x in range(len(feature))] for y in range(n_files)]
	ave = [[float(0) for x in range(len(feature))] for y in range(n_files)]
	sqr =[[float(0) for x in range(len(feature))] for y in range(n_files)]
	std_sqr = [[float(0) for x in range(len(feature))] for y in range(n_files)]

	total = 0	
	# calculate num, ave, std for each class	
	for i in range(n_files):
		print("Process file " + filename[i])
		f_in = open(filename[i])
		#skip the first line
		line = f_in.readline()
		line = f_in.readline()
		while(line):	#run until EOF
			total += 1
			token = line.split(",")
			for j in range(begin_column, len(feature)):
				num[i][j] += 1
				val = float(token[j])
				s[i][j] += val
				ave[i][j] = s[i][j] / num[i][j]
				sqr[i][j] += val * val
				std_sqr[i][j] = sqr[i][j] / num[i][j] - ave[i][j] * ave[i][j]		
			line = f_in.readline()	
		f_in.close()
	
	mean = [float(0)] * len(feature)
	FS = [float(0)] * len(feature)	
	for j in range(begin_column, len(feature)):
		for i in range(n_files):
			mean[j] += num[i][j] * ave[i][j]
		mean[j] = mean[j] / total
		a = float(0)
		b = float(0)
		for i in range(n_files):
			a += (float(num[i][j]/total) * (mean[j] -ave[i][j]) * (mean[j] -ave[i][j]))
			b += (float(num[i][j]/total) * std_sqr[i][j])
		FS[j] = float(a/b)
		print(feature[j] + "," + str(FS[j]))
# end of main()

if __name__ == '__main__':
	main()
