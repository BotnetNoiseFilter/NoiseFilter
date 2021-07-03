##################################################################
# This program mixes normal and botnet flows and adds label to the first column. 
# The program also sorts the features according to fisher score.
# Usage: python3 mix_dataset.py normal.csv botnet.csv sampling out_file.csv
# sampling: 0: undersampling, 1: no sampling
# out_file.csv: output file name
###################################################################
import sys

FS=[17, 31, 24, 27, 20, 7, 29, 9, 26, 10, 6, 19, 22, 23, 30, 14, 15, 11, 13, 8, 28, 12, 25, 5, 18, 21, 16]

def extract_feature(line, n_features):
	token = line.split(",")
	ret = token[0] + "," + token[1] + "," + token[2] + "," + token[3] + "," + token[4]
	for i in range(n_features):
		ret += ("," + token[FS[i]].replace("\n", ""))
	ret += "\n"
	return ret
# end of extract_feature()
	
def main():
	if len(sys.argv) < 4:
		print("Usage: python3 mix_dataset.py normal.csv botnet.csv sampling out_file.csv (sampling: 0, undersampling)")
		sys.exit(1)
	
	sampling = int(sys.argv[3])
	
	# open csv file
	f_nor = open(sys.argv[1], 'r')
	f_bot = open(sys.argv[2], 'r')
	o_name = sys.argv[4].replace(".csv", "")
	f_out = open(o_name + ".csv", 'w')
	
	# skip title line
	line_nor = f_nor.readline()
	line_bot = f_bot.readline()

	line_nor = f_nor.readline()
	line_bot = f_bot.readline()
	
	if(sampling == 0):
		while(line_nor and line_bot):	# all files has data (undersampling)
			if(line_nor):
				# write a normal flow
				string = "0, " + extract_feature(line_nor, len(FS))
				f_out.write(string)
				line_nor = f_nor.readline()
			if(line_bot):
				# write a botnet flow
				string = "1, " + extract_feature(line_bot, len(FS))
				f_out.write(string)
				line_bot = f_bot.readline()
	else:
		while(line_nor or line_bot):	# one file has data
			if(line_nor):
				# write a normal flow
				string = "0, " + extract_feature(line_nor, len(FS))
				f_out.write(string)
				line_nor = f_nor.readline()
			if(line_bot):
				# write a botnet flow
				string = "1, " + extract_feature(line_bot, len(FS))
				f_out.write(string)
				line_bot = f_bot.readline()
		
	
	f_out.close()
	print("Write dataset completed!!")
	
	f_nor.close()
	f_bot.close()	
	
# end of main()

if __name__ == '__main__':
	main()
