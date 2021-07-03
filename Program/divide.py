##################################################################
# This program devides the dataset into n parts.
# Usage: python3 divide.py inputfile num
###################################################################

import sys

def main():
	if len(sys.argv) < 2:
		print("Usage: python3 divide.py inputfile num")
		sys.exit(1)
	
	filename = sys.argv[1].replace(" ", "")
	filename = filename.replace(".csv", "")
	n_files = int(sys.argv[2])
	max_len = 2
	
	f_in = open(filename+".csv", 'r')
	# open output files
	f_out = []
	for i in range(n_files):
		f = open(filename+str(i)+".csv", 'w')
		f_out.append(f)

	# read flows and write to output files
	i = 0
	flag = 0
	for line in f_in:
		f_out[i].write(line)
		flag = (flag + 1) % max_len
		if(flag == 0):
			i = (i + 1) % n_files
	
	# close output files
	for i in range(n_files):
		f_out[i].close()
# end of main()

if __name__ == '__main__':
	main()
