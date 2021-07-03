import sys
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import manifold
from sklearn.preprocessing import StandardScaler

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

def main():
	if(len(sys.argv) < 3):
		print("Usage: python3 tsne.py dataset.csv title\n")
		exit(1)

	size, X, Y = read_dataset(sys.argv[1], 27)
	Y = np.reshape(Y, (-1))
	#X = StandardScaler().fit_transform(X)
	X_tsne = manifold.TSNE(n_components=2, init='random', random_state=5, verbose=1).fit_transform(X)

	#全圖(正常+惡意)
	dfplot = pd.DataFrame(dict(feature1 = X_tsne[:, 0], feature2 = X_tsne[:, 1], label=Y))
	plot = dfplot.groupby('label')
	normal = plot.get_group(0)
	bot = plot.get_group(1)

	ax = bot.plot(x='feature1', y='feature2', kind='scatter', color='black', label='Bot', s=2)
	normal.plot(x='feature1', y='feature2', kind='scatter', color='gray', label='Normal', s=2, ax=ax)	
	plt.legend(fontsize=12, loc='upper right')
	plt.rcParams.update({'axes.labelsize':6})
	plt.title(sys.argv[2], fontsize=20)
	plt.xlabel('')
	plt.ylabel('')

	#正常only
	# plt.plot('feature1','feature2','.', c='g',data=normal,label=y)
	# plt.title('Normal')
	# plt.xlabel('X')
	# plt.ylabel('Y')
	# plt.legend(bbox_to_anchor=[1.05, 0], loc = 3, borderaxespad=0)
	# plt.grid(True, linestyle = "--", color = 'gray', linewidth = '0.5', axis = 'both')
	# plt.tick_params(bottom = 'on',top = 'off',left = 'on',right = 'off')
	# plt.tight_layout()

	#惡意only
	# plt.plot('feature1','feature2','.', c='r',data=malicious,label=y)
	# plt.title('Malicious')
	# plt.xlabel('X')
	# plt.ylabel('Y')
	# plt.legend(bbox_to_anchor=[1.05, 0], loc = 3, borderaxespad=0)
	# plt.grid(True, linestyle = "--", color = 'gray', linewidth = '0.5', axis = 'both')
	# plt.tick_params(bottom = 'on',top = 'off',left = 'on',right = 'off')
	# plt.tight_layout()

	# plt.savefig('---.png') # 儲存圖檔
	plt.show()
	print("Complete!!!...")
# end of main()

if __name__ == '__main__':
	main()
