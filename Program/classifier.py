import sys
import numpy as np
from sklearn import svm
from sklearn.naive_bayes import GaussianNB
from sklearn import tree

def read_dataset(filename, n_features):
	f = open(filename, 'r')
	line = f.readline()
	token = line.split(",")
	X = np.zeros((n_features))
	for i in range(n_features):
		X[i] = float(token[6 + i])
	Y = np.array([int(token[0])])

	line = f.readline()
	while(line):
		token = line.split(",")
		X1 = np.zeros((n_features))
		for i in range(n_features):
			X1[i] = float(token[6 + i])
		Y1 = np.array([int(token[0])])
		
		X = np.append(X, X1, axis = 0)
		Y = np.append(Y, Y1, axis = 0)
		line = f.readline()

	f.close()
	X = np.reshape(X, (-1, n_features))
	Y = np.reshape(Y, (-1, 1))
	num = np.size(Y)
	
	return num, X, Y
# end of read_dataset()

def calculate(num, Y, result):
	TP = 0
	TN = 0
	FP = 0
	FN = 0
	
	for i in range(num):
		if(Y[i] == 1):	# bot
			if(result[i] == 1):
				TP += 1
			else:
				FN += 1
		else:			# normal
			if(result[i] == 0):
				TN += 1
			else:
				FP += 1
					
	return TP, TN, FP, FN
# end of calculate()

def main():
	if(len(sys.argv) < 3):
		print("Usage: python3 classifier.py cmd training_set n_features testing_set ..., cmd = SVM, NB, DT\n")
		exit(1)
		
	# Select classifier algorithm
	if(sys.argv[1] == "SVM"):
		clf = svm.SVC(kernel='rbf')
	elif(sys.argv[1] == "NB"):
		clf = GaussianNB()
	elif(sys.argv[1] == "DT"):
		clf = tree.DecisionTreeClassifier()
	else:
		print("Usage: python3 classifier.py cmd training_set n_features testing_set ..., cmd = SVM, NB, DT\n")
		exit(1)
	
	n_features = int(sys.argv[3])
		
	# read dataset
	num, X, Y = read_dataset(sys.argv[2], n_features)
	
	# training
	clf.fit(X, Y)

	# testing
	result = clf.predict(X)
				
	TP, TN, FP, FN = calculate(num, Y, result)
						
	f_out = open("out-" + sys.argv[1] + "-" + str(n_features) + ".csv", 'a')
	#f_out.write(sys.argv[1] + "\n")
	#f_out.write("ID, TP, TN, FP, FN, TPR, FPR, ACC\n")
	#string = sys.argv[2] + "," + str(TP) + "," + str(TN) + "," + str(FP) + "," + str(FN) + "," +\
	#		str(TP/(TP+FN)) + "," + str(FP/(FP+TN)) + "," + str((TP+TN)/(TP + TN + FP + FN)) + "\n"
	#f_out.write(string)
	
	for i in range(4, len(sys.argv)):
		t_num, t_X, t_Y = read_dataset(sys.argv[i], n_features)
		t_result = clf.predict(t_X)

		# write the classification result
		res_fp = open("resO-" + sys.argv[i] , 'w')
		res_num = np.size(t_result)
		for j in range(res_num):
			res_fp.write(str(t_result[j]) + "\n")
		res_fp.close()

		TP, TN, FP, FN  = calculate(t_num, t_Y, t_result)
		string = sys.argv[i] + "," + str(TP) + "," + str(TN) + "," + str(FP) + "," + str(FN) +  "," +\
			str(TP/(TP+FN)) + "," + str(FP/(FP+TN)) + "," + str((TP+TN)/(TP + TN + FP + FN)) + "\n"
		f_out.write(string)

	f_out.close()
		
# end of main()

if __name__ == '__main__':
	main()
