import argparse
import numpy as np
import matplotlib.pyplot as plt

from model import model
from heatmap import heatmap
from summary import summary

parser = argparse.ArgumentParser(description='Generate labeled heatmaps')

parser.add_argument('matrix', metavar='mat', type=str, nargs=1, help='path to numpy matrix file generated by model')
#parser.add_argument('runs', type=int, nargs=1, help='number of runs')
parser.add_argument('--save', '-s', type=bool, help='save figures to file')

m = parser.parse_args()
#print(m.matrix)

data = np.load(m.matrix[0], allow_pickle=True)
#print(np.sum(data))
#data = data.astype(float)/1000.0

#print(data)

mod = model(.0005, .0001, 11, 0.5, 0.001, 5, .5)
'''
for i in data:
	if np.sum(i) > 0:
		fig, ax = plt.subplots()
		im, cbar = heatmap(i, mod.brange, mod.xirange, vmin=0) #, vmax=np.max(data))
		fig.tight_layout()
plt.show()'''

sum = summary(data[0], mod=mod)
sum.vis()
print(sum.evolvedGreaterB())
print(sum.evolvedGreaterG())
print([np.sum(x) for x in data[0]])
print([np.sum(x) for x in data[1]])
print([np.sum(x) for x in data[2]])
print(data[3])
print(data[4])
print(np.sum(data[1]))
