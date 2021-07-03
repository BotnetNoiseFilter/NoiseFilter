##################################################################
# This program merge files for k-fold
# Usage: python3 k-fold.py filename n_file idx
###################################################################
import sys

def main():
	if len(sys.argv) < 3:
		print("Usage: python3 k-fold.py filename n_file idx")		
		sys.exit(1)

	filename = sys.argv[1].replace(" ", "")
	n_file = int(sys.argv[2])
	idx = int(sys.argv[3])
	
	# merge training_file (except i)
	f_out = open("training.csv", 'w')
	for j in range(n_file):
		if(j != idx):
			f_name = filename+str(j)+".csv"
			print(f_name)
			f_in = open(f_name, 'r')
			for line in f_in:
				f_out.write(line)
			f_in.close()
	f_out.close()
# end of main()

if __name__ == '__main__':
	main()
