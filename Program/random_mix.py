##################################################################
# This program mixes normal and botnet flows and adds label to the first column. . (Undersampling is used)
# The random sampling method is used.
# Usage: python3 random_mix.py normal.csv botnet.csv out_file.csv
# out_file.csv: output file name
###################################################################
import sys
from random import *

FS=[17, 31, 24, 27, 20, 7, 29, 9, 26, 10, 6, 19, 22, 23, 30, 14, 15, 11, 13, 8, 28, 12, 25, 5, 18, 21, 16]

def extract_feature(line, n_features):
	token = line.split(",")
	ret = token[0] + "," + token[1] + "," + token[2] + "," + token[3] + "," + token[4]
	for i in range(n_features):
		ret += ("," + token[FS[i]].replace("\n", ""))
	ret += "\n"
	return ret
# end of extract_feature()

def selected(x, total):
	percentage = float(x) / float(total)
	r = random()
	if(r < percentage):
		return True
	else:
		return False
# end of selected()
	
def main():
	if len(sys.argv) < 3:
		print("Usage: python3 random_mix.py normal.csv botnet.csv out_file.csv")
		sys.exit(1)
	
	# count num of line
	num_nor = 0
	num_bot = 0
	f_nor = open(sys.argv[1], 'r')
	for line in f_nor:
		num_nor += 1
	f_nor.close()
	num_nor -= 1		# skip title line
    
	f_bot = open(sys.argv[2], 'r')
	for line in f_bot:
		num_bot += 1
	f_bot.close()
	num_bot -= 1	# skip title line	
	
	# open csv file
	f_nor = open(sys.argv[1], 'r')
	f_bot = open(sys.argv[2], 'r')
	o_name = sys.argv[3].replace(".csv", "")
	f_out = open(o_name + ".csv", 'w')
	
	# skip title line
	line_nor = f_nor.readline()
	line_bot = f_bot.readline()

	line_nor = f_nor.readline()
	line_bot = f_bot.readline()
	
	if(num_nor > num_bot):
		num_write = num_bot
		num_skip = num_nor - num_write
		while(line_nor and line_bot):	# all files has data (undersampling)
			while(not selected(num_write, num_write + num_skip) and line_nor):
				num_skip -= 1
				line_nor = f_nor.readline()
			if(line_nor):
				# write a normal flow
				string = "0, " + extract_feature(line_nor, len(FS))
				f_out.write(string)
				num_write -= 1
				line_nor = f_nor.readline()
			if(line_bot):
				# write a botnet flow
				string = "1, " + extract_feature(line_bot, len(FS))
				f_out.write(string)
				line_bot = f_bot.readline()
	else:			# num_bot > num_nor
		num_write = num_nor
		num_skip = num_bot - num_write
		while(line_nor and line_bot):	# all files has data (undersampling)
			while(not selected(num_write, num_write + num_skip) and line_bot):
				num_skip -= 1
				line_bot = f_bot.readline()
			if(line_nor):
				# write a normal flow
				string = "0, " + extract_feature(line_nor, len(FS))
				f_out.write(string)
				line_nor = f_nor.readline()
			if(line_bot):
				# write a botnet flow
				string = "1, " + extract_feature(line_bot, len(FS))
				f_out.write(string)
				num_write -= 1
				line_bot = f_bot.readline()
	
	f_out.close()
	print("Write dataset completed!!")
	
	f_nor.close()
	f_bot.close()	
	
# end of main()

if __name__ == '__main__':
	main()
