Noise Filter
A Botnet Detection Framework Based on Noise Filtering

1. Feature files:
	CTU42-botnet_features.csv	: 14428 flows
	CTU42-normal_features.csv	: 27067 flows
	CTU43-botnet_features.csv	: 19440 flows
	CTU43-normal_features.csv	: 8471 flows
	CTU46-botnet_features.csv	: 859 flows
	CTU46-normal_features.csv	: 4623 flows
	CTU50-botnet_features.csv	: 93736 flows
	CTU50-normal_features.csv	: 27612 flows
	CTU54-botnet_features.csv	: 33040 flows
	CTU54-normal_features.csv	: 26898 flows
	
2. Calculate Fisher Score 
	python3 fisher_score.py begin_column file_nums file1 file2 ...
	Ex: Calculate the FS of CTU42
		python3 fisher_score.py 5 2 CTU42-botnet_features.csv CTU42-normal_features.csv
		
3. Mix dataset and sort the features according to fisher score.
	3.1 mix_dataset.py 
		This program mixes normal and botnet flows and adds label to the first column. 
		Ex: python3 mix_dataset.py normal.csv botnet.csv sampling out_file.csv (sampling: 0, undersampling, 1: no sampling)
	3.2 random_mix.py
		This program mixes normal and botnet flows and adds label to the first column. (Undersampling is used)
		The random sampling method is used.
		Ex: python3 random_mix.py normal.csv botnet.csv out_file.csv
	
4. Draw t-SNE
	Step 1. mix_dataset by mix_dataset.py
		python3 mix_dataset.py CTU42-normal_features.csv CTU42-botnet_features.csv 1 CTU42-dataset.csv
	Step 2. Draw t-SNE
		python3 tsne.py CTU42-dataset.csv CTU42
		
5. Devide the dataset
	5.1 Devide a file into n parts
		python3 divide.py dataset.csv n
		The output files are: dataset0.csv, dataset1.csv, ...,dataset{n-1}.csv
	5.2 Merge files for k-fold
		python3 k-fold.py dataset n idx
		The program merges dataset0.csv, dataset1.csv, ..., dataset{idx-1}.csv, dataset{idx+1}.csv, ...,dataset{N-1}.csv into training.csv
		dataset{idx}.csv will be skipped.
		
6. The classifier
	6.1 The origional classifier (DT, NB, SVM)
		python3 classifier.py cmd training_set n_features testing_set ..., cmd = SVM, NB, DT
		Format of output file: testing_file, TP, TN, FP, FN, TPR, FPR, ACC
	6.2 The proposed method
		python3 TwoStep6.py P-clf T-clf F-clf training_set n_features Tnum testing_set ..., clf = SVM, NB, DT, Tnum = number of flows Class T is used for training F-classifier, 0 : all flows are used
		Format of output file: testing_file, TP, TN, FP, FN, TPR, FPR, ACC, TTP, TTN, TFP, TFN, TTPR, TFPR, TACC, FTP, FTN, FFP, FFN, FTPR, FFPR, FACC
		where  TP, TN, FP, FN, TPR, FPR, ACC are the values of the proposed system
				    TTP, TTN, TFP, TFN, TTPR, TFPR, TACC are the values of T-classifier
				    FTP, FTN, FFP, FFN, FTPR, FFPR, FACC are the values of F-classifier
	
7. The feature selection
script:
--
# Feature selection for DT, SVM & NB
cmd=python3
exec_path=~/NoiseFilter/Program/
for((k = 1 ; k <= 10 ; k++))
do
	${cmd} ${exec_path}random_mix.py CTU42-normal_features.csv CTU42-botnet_features.csv CTU42-mix.csv
	${cmd} ${exec_path}divide.py CTU42-mix.csv 10
	# k-fold
	for((i = 0 ; i <= 9 ; i++))
	do
		${cmd} ${exec_path}k-fold.py CTU42-mix 10 ${i}
		for((j = 1 ; j <= 27 ; j++))
		do
			${cmd} ${exec_path}classifier.py SVM training.csv ${j} CTU42-mix${i}.csv
			${cmd} ${exec_path}classifier.py DT training.csv ${j} CTU42-mix${i}.csv
			${cmd} ${exec_path}classifier.py NB training.csv ${j} CTU42-mix${i}.csv
		done
		rm training.csv
	done
	rm CTU42-mix.csv
	rm CTU42-mix?.csv
done
--
	
8. The algorithm selection
If O-classifier is DT, for some case, F-class is empty. In such a case, there is no output. The program will print "F-Class is empty. Cannot training Pre-classifier".

script:
--
# Performance comparison for Pre-classifier, T-classifier and F-classifier
# TwoStep6.py: Tnum = 0 (all), # of features based on T-classifier
cmd=python3
exec_path=~/NoiseFilter/Program/
for((k = 1 ; k <= 10 ; k++))
do
	${cmd} ${exec_path}random_mix.py CTU42-normal_features.csv CTU42-botnet_features.csv CTU42-mix.csv
	${cmd} ${exec_path}divide.py CTU42-mix.csv 10
	# k-fold
	for((i = 0 ; i <= 9 ; i++))
	do
		${cmd} ${exec_path}k-fold.py CTU42-mix 10 ${i}
		# execute all algorithms
		${cmd} ${exec_path}classifier.py SVM training.csv 6 CTU42-mix${i}.csv
		${cmd} ${exec_path}classifier.py DT training.csv 27 CTU42-mix${i}.csv
		${cmd} ${exec_path}classifier.py NB training.csv 3 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM SVM DT training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT SVM DT training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB SVM DT training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM DT DT training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT DT DT training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB DT DT training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM NB DT training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT NB DT training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB NB DT training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM SVM SVM training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT SVM SVM training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB SVM SVM training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM DT SVM training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT DT SVM training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB DT SVM training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM NB SVM training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT NB SVM training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB NB SVM training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM SVM NB training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT SVM NB training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB SVM NB training.csv 6 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM DT NB training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT DT NB training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB DT NB training.csv 27 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py SVM NB NB training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py DT NB NB training.csv 3 0 CTU42-mix${i}.csv
		${cmd} ${exec_path}TwoStep6.py NB NB NB training.csv 3 0 CTU42-mix${i}.csv
		# delete training dataset
		rm training.csv
	done
	rm CTU42-mix.csv
	rm CTU42-mix?.csv
done
--

9. Performance testing
CTU42 Training (under sampling), CTU42, CTU43, CTU50 Testing (no sampling)
script:
--
cmd=python3
exec_path=~/NoiseFilter/Program/
dataset=~/NoiseFilter/Dataset/
# Testing dataset (No sampling)
for k in 42 43 50
do
	${cmd} ${exec_path}mix_dataset.py ${dataset}CTU${k}-normal_features.csv ${dataset}CTU${k}-botnet_features.csv 1 CTU${k}-mix.csv
done
for((i = 1 ; i <= 100 ; i++))
do
	# Training dataset (Undersampling)
	${cmd} ${exec_path}random_mix.py ${dataset}CTU42-normal_features.csv ${dataset}CTU42-botnet_features.csv CTU42-mixU.csv
	# Testing
	${cmd} ${exec_path}TwoStep6.py SVM SVM NB CTU42-mixU.csv 6 0 CTU42-mix.csv CTU43-mix.csv CTU50-mix.csv 
	${cmd} ${exec_path}TwoStep6.py DT NB SVM CTU42-mixU.csv 3 0 CTU42-mix.csv CTU43-mix.csv CTU50-mix.csv
	${cmd} ${exec_path}classifier.py SVM CTU42-mixU.csv 6 CTU42-mix.csv CTU43-mix.csv CTU50-mix.csv 
	${cmd} ${exec_path}classifier.py NB CTU42-mixU.csv 3 CTU42-mix.csv CTU43-mix.csv CTU50-mix.csv
	rm CTU??-mixU.csv
done
--

10. Robustness test
CTU42 Training (under sampling), CTU46, CTU54 Testing (no sampling)
script:
--
cmd=python3
exec_path=~/NoiseFilter/Program/
dataset=~/NoiseFilter/Dataset/
# Testing dataset (No sampling)
for k in 46 54
do
	${cmd} ${exec_path}mix_dataset.py ${dataset}CTU${k}-normal_features.csv ${dataset}CTU${k}-botnet_features.csv 1 CTU${k}-mix.csv
done
for((i = 1 ; i <= 100 ; i++))
do
	# Training dataset (Undersampling)
	${cmd} ${exec_path}random_mix.py ${dataset}CTU42-normal_features.csv ${dataset}CTU42-botnet_features.csv CTU42-mixU.csv
	# Testing
	${cmd} ${exec_path}TwoStep6.py SVM SVM NB CTU42-mixU.csv 6 0 CTU46-mix.csv CTU54-mix.csv 
	${cmd} ${exec_path}TwoStep6.py DT NB SVM CTU42-mixU.csv 3 0 CTU46-mix.csv CTU54-mix.csv
	rm CTU??-mixU.csv
done
--

CTU46 Training (under sampling), CTU46, CTU54 Testing (no sampling)
CTU54 Training (under sampling), CTU46, CTU54 Testing (no sampling)
