# When building the pre-classifier, we do not divide the data into two part.
# If Class F is empty, the program has to process the exception.
# Change the percentage of flows in Class T to at least num flows for both classes in Class T
# Print the classification results of the testing dataset
# ValueError exception handling

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
	# Z keeps the features (src / dest ports) for F-classifier
	Z = np.zeros((2))
	Z[0] = float(token[3])	# src port
	Z[1] = float(token[4])	# dest port

	line = f.readline()
	while(line):
		token = line.split(",")
		X1 = np.zeros((n_features))
		for i in range(n_features):
			X1[i] = float(token[6 + i])
		Y1 = np.array([int(token[0])])
		Z1 = np.zeros((2))
		Z1[0] = float(token[3])
		Z1[1] = float(token[4])
		
		X = np.append(X, X1, axis = 0)
		Y = np.append(Y, Y1, axis = 0)
		Z = np.append(Z, Z1, axis = 0)
		line = f.readline()

	f.close()
	X = np.reshape(X, (-1, n_features))
	Y = np.reshape(Y, (-1, 1))
	Z = np.reshape(Z, (-1, 2))
	num = np.size(Y)
	
	return num, X, Y, Z
# end of read_dataset()

def calculate(num, Y, result):
	TP = 0
	TN = 0
	FP = 0
	FN = 0
	TTP = 0
	TTN = 0
	TFP = 0
	TFN = 0
	FTP = 0
	FTN = 0
	FFP = 0
	FFN = 0
	
	for i in range(num):
		if(result[i] >= 0):		# if result[i] < 0, T-class contains one class
			if(Y[i] == 1) :	# bot
				if(result[i] == 1):
					TP += 1
					TTP += 1
				elif(result[i] == 3):
					TP += 1
					FTP += 1
				elif(result[i] == 0):
					FN += 1
					TFN += 1
				else:
					FN += 1
					FFN += 1
			else:			# normal
				if(result[i] == 0):
					TN += 1
					TTN += 1
				elif(result[i] == 2):
					TN += 1
					FTN += 1
				elif(result[i] == 1):
					FP += 1
					TFP += 1
				else:
					FP += 1
					FFP += 1
					
	return TP, TN, FP, FN, TTP, TTN, TFP, TFN, FTP, FTN, FFP, FFN
# end of calculate()

class TwoStepClassifier:
	def __init__(self, n_features, p_clf, t_clf, f_clf, Tnum):	
		self.n_features = n_features;
		self.p_clf = p_clf			# Pre-classifier
		self.t_clf = t_clf				# T-classifier
		self.f_clf = f_clf				# F-classifier
		self.o_clf = t_clf			# O-classifier
		self.Tnum = Tnum		       # number of flows (for both classes) in class T used for training F-classifier, Tnum = 0 : all flows
		return
	# end of __init__

	def collect_TF_class(self, X, Y):
		num = np.size(Y)
		self.o_clf.fit(X, Y)
		result = self.o_clf.predict(X)
		T_num = 0		# number of elements in class T
		F_num = 0		# number of elements in class F
	
		FX = []
		FY = []
	
		for i in range(num):
			if(Y[i] == result[i]):  # classify correctly
				if(T_num == 0):
					TX = X[i]
					TY = Y[i]
					T_num += 1
				else:
					TX = np.append(TX, X[i], axis = 0)
					TY = np.append(TY, Y[i], axis = 0)
					T_num += 1
			else:	# misclassify
				if(F_num == 0):
					FX = X[i]
					FY = Y[i]
					F_num += 1
				else:
					FX = np.append(FX, X[i], axis = 0)
					FY = np.append(FY, Y[i], axis = 0)
					F_num += 1
		# end for

		TX = np.reshape(TX, (-1, self.n_features))
		TY = np.reshape(TY, (-1, 1))	
		FX = np.reshape(FX, (-1, self.n_features))
		FY = np.reshape(FY, (-1, 1))
		return T_num, F_num, TX, TY, FX, FY
	# end of collect_TF_class()

	def T_fit(self, X, Y):
		# prepare dataset for pre-classifier
		T_num, F_num, TX, TY, FX, FY = self.collect_TF_class(X, Y)
		
		if(F_num == 0):
			print("F-Class is empty. Cannot training Pre-classifier!!\n")
			exit(1)
			
		# Prepare dataset for Pre-Classifier
		# elements in TX : CY = 1
		# elements in FX : CY = 0
		# oversampling
		CX = TX
		CY = np.ones(T_num)
		tmp = np.zeros(F_num)
		for i in range(int(T_num / F_num)):
			CX = np.append(CX, FX, axis = 0)				# append FX to CX
			CY = np.append(CY, tmp, axis = 0)				# append 0 to CY
		CX = np.reshape(CX, (-1, self.n_features))
		
		# training pre-classifier
		self.p_clf.fit(CX, CY)

		# training T-classifier	
		self.t_clf.fit(TX, TY)
		return
	# end of T_fit()
	
	def T_predict(self, X):		# classify by using T-Classify
		return self.t_clf.predict(X)
	# end if T_predict()
	
	def F_fit(self, Z, Y):
		# training F-classifier by using the result of T-Classifier
		self.f_clf.fit(Z, Y)
		return
	# end of T_fit()
	
	def predict(self, X, Z):		# Z for training and testing F-Classifier
		result = self.p_clf.predict(X)
		num = np.size(result)

		# result is the result of Pre-Classifier
		#  divide X, Z into TX, TZ and FX, FZ according to result
		tt = 0  
		ff = 0
		for i in range(num):
			if(result[i] == 1):		# Class T
				if(tt == 0):
					TX = X[i]
					TZ = Z[i]
					tt += 1
				else:				
					TX = np.append(TX, X[i], axis = 0)
					TZ = np.append(TZ, Z[i], axis = 0)
					tt += 1
			else:					# Class F
				if(ff == 0):
					FX = X[i]
					FZ = Z[i]
					ff += 1
				else:
					FX = np.append(FX, X[i], axis = 0)
					FZ = np.append(FZ, Z[i], axis = 0)
					ff += 1
		# end for
		# if ff == 0, Class F is empty, i.e., FX and FZ are not define
		print("Class F is empty? num=%d, T=%d, F=%d\n" %(num, tt, ff))
		TX = np.reshape(TX, (-1, self.n_features))
		TZ = np.reshape(TZ, (-1, 2))						# used for training F-classifier
		if(ff != 0):	# Class F is not empty
			FX = np.reshape(FX, (-1, self.n_features))		# do not used in the following
			FZ = np.reshape(FZ, (-1, 2))
		
		TY = self.t_clf.predict(TX)
		
		if(ff != 0):	# Class F is not empty
			# Training F-Classifier by using part of TZ, TY
			part_num = np.size(TY)
			ty0 = 0
			ty1 = 0
			if(self.Tnum != 0):
				all_num = part_num
				part_num = 0
				while(((ty0 < self.Tnum) or (ty1 < self.Tnum)) and (part_num < all_num)):
					if(TY[part_num] == 0):
						ty0 += 1
					else:
						ty1 += 1
					part_num += 1
				#end while()
			print("Number of flows for training F-classifier = %d, ty0 = %d ty1 = %d\n" % (part_num, ty0, ty1))
			Part_TZ = TZ[0:part_num]			# only select part of data in Class T
			Part_TY = TY[0:part_num]
		
			try:
				self.F_fit(Part_TZ, Part_TY)
				# Testing by using FZ
				FY = self.f_clf.predict(FZ)
			except ValueError:
				FY = [-5] * np.size(FZ)
				FY = np.reshape(FY, (-1, 1))
		# end if
		
		# rewrite to result[]
		tt = 0	# index for T_result
		ff = 0  	# index for F_result
		for i in range(num):
			if(result[i] == 1):		# T-classifier
				result[i] = TY[tt]
				tt += 1
			else:					# F-classifier
				result[i] = FY[ff] + 2	# result >= 2, classify by F-classifier
				ff += 1
				
		return result
	#end of predict()
#end of class

def main():
	if(len(sys.argv) < 4):
		print("Usage: python3 TwoStep.py P-clf T-clf F-clf training_set n_features Tnum testing_set ..., clf = SVM, NB, DT, Tnum = number of flows Class T is used for training F-classifier, 0 : all flows are used\n")
		exit(1)
		
	# Select Pre-classifier algorithm
	if(sys.argv[1] == "SVM"):
		Pclf = svm.SVC(kernel='rbf')
	elif(sys.argv[1] == "NB"):
		Pclf = GaussianNB()
	elif(sys.argv[1] == "DT"):
		Pclf = tree.DecisionTreeClassifier()
	else:
		print("Usage: python3 TwoStep.py P-clf T-clf F-clf training_set n_features Tnum testing_set ..., clf = SVM, NB, DT, Tnum = number of flows Class T is used for training F-classifier, 0 : all flows are used\n")
		exit(1)
		
	# Select T-classifier algorithm
	if(sys.argv[2] == "SVM"):
		Tclf = svm.SVC(kernel='rbf')
	elif(sys.argv[2] == "NB"):
		Tclf = GaussianNB()
	elif(sys.argv[2] == "DT"):
		Tclf = tree.DecisionTreeClassifier()
	else:
		print("Usage: python3 TwoStep.py P-clf T-clf F-clf training_set n_features Tnum testing_set ..., clf = SVM, NB, DT, Tnum = number of flows Class T is used for training F-classifier, 0 : all flows are used\n")
		exit(1)
		
	# Select F-classifier algorithm
	if(sys.argv[3] == "SVM"):
		Fclf = svm.SVC(kernel='rbf')
	elif(sys.argv[3] == "NB"):
		Fclf = GaussianNB()
	elif(sys.argv[3] == "DT"):
		Fclf = tree.DecisionTreeClassifier()
	else:
		print("Usage: python3 TwoStep.py P-clf T-clf F-clf training_set n_features Tnum testing_set ..., clf = SVM, NB, DT, Tnum = number of flows Class T is used for training F-classifier, 0 : all flows are used\n")
		exit(1)
	
	n_features = int(sys.argv[5])
	Tnum = int(sys.argv[6])
		
	# read training dataset
	num, X, Y, Z = read_dataset(sys.argv[4], n_features)
	
	CLF = TwoStepClassifier(n_features, Pclf, Tclf, Fclf, Tnum)
	
	# training
	CLF.T_fit(X, Y)

	f_out = open("out6-" + sys.argv[1] + "-" + sys.argv[2] + "-" + sys.argv[3] + "-" +str(n_features) + ".csv", 'a')

    # Testing ....	
	for i in range(7, len(sys.argv)):
		t_num, t_X, t_Y, t_Z = read_dataset(sys.argv[i], n_features)
		t_result = CLF.predict(t_X, t_Z)

		# write the classification result
		res_fp = open("res6-" + sys.argv[i], 'w')
		res_num = np.size(t_result)
		for j in range(res_num):
			res_fp.write(str(t_result[j]) + "\n")
		res_fp.close()

		TP, TN, FP, FN, TTP, TTN, TFP, TFN, FTP, FTN, FFP, FFN  = calculate(t_num, t_Y, t_result)
		if((TP+FN) != 0):
			TPR = TP/(TP+FN)
		else:
			TPR = 0
		if((FP+TN) != 0):
			FPR = FP/(FP+TN)
		else:
			FPR = 0
		if((TP + TN + FP + FN) != 0):
			ACC = (TP+TN)/(TP + TN + FP + FN)
		else:
			ACC = 0

		if((TTP+TFN) != 0):
			T_TPR = TTP/(TTP+TFN)
		else:
			T_TPR = 0
		if((TFP+TTN) != 0):
			T_FPR = TFP/(TFP+TTN)
		else:
			T_FPR = 0
		if((TTP + TTN + TFP + TFN) != 0):
			T_ACC = (TTP+TTN)/(TTP + TTN + TFP + TFN)
		else:
			T_ACC = 0

		
		if((FTP+FFN) != 0):
			F_TPR = FTP/(FTP+FFN)
		else:
			F_TPR = 0
		if((FFP+FTN) != 0):
			F_FPR = FFP/(FFP+FTN)
		else:
			F_FPR = 0
		if((FTP + FTN + FFP + FFN) != 0):
			F_ACC = (FTP+FTN)/(FTP + FTN + FFP + FFN)
		else:
			F_ACC = 0
		string = sys.argv[i] + "," + str(TP) + "," + str(TN) + "," + str(FP) + "," + str(FN) +  "," + str(TPR) + "," + str(FPR) + "," + str(ACC) 
		string += "," + str(TTP) + "," + str(TTN) + "," + str(TFP) + "," + str(TFN) +  "," + str(T_TPR) + "," + str(T_FPR) + "," + str(T_ACC) 
		string += "," + str(FTP) + "," + str(FTN) + "," + str(FFP) + "," + str(FFN) +  "," + str(F_TPR) + "," + str(F_FPR) + "," + str(F_ACC) + "\n"
		f_out.write(string)

	f_out.close()
		
# end of main()

if __name__ == '__main__':
	main()
