import argparse
import numpy as np
import matplotlib.pyplot as plt

from model import model
from heatmap import heatmap
from summary import summary

parser = argparse.ArgumentParser(description='Generate labeled heatmaps')

parser.add_argument('matrix', metavar='mat', type=str, nargs=1, help='path to numpy matrix file generated by model')
#parser.add_argument('runs', type=int, nargs=1, help='number of runs')
parser.add_argument('--savepath', '-f', type=str, help='path to save figures')
parser.add_argument('--show', '-s', help='show figures', action='store_true')

m = parser.parse_args()

filename = m.matrix[0]

data = np.load(filename, allow_pickle=True)

if 'test' in filename:
    params = filename.split('_')[1:]
    params[2] = params[2][:-4]
    params = [float(x) for x in params]
    mod = model(params[0], .0000001, 11, params[1], 0.05, 5, params[2])
else: mod = model(0.0000001, .0000001, 11, 0.4, 0.05, 5, .9)

'''
for i in data:
	if np.sum(i) > 0:
		fig, ax = plt.subplots()
		im, cbar = heatmap(i, mod.brange, mod.xirange, vmin=0) #, vmax=np.max(data))
		fig.tight_layout()
plt.show()'''

sum = summary(data[0], mod=mod)

if m.savepath: sum.vis(m.savepath, show=m.show)
else: sum.vis(show=m.show)
'''print(sum.evolvedGreaterB())
print(sum.evolvedGreaterG())
print([np.sum(x) for x in data[0]])
print([np.sum(x) for x in data[1]])
print([np.sum(x) for x in data[2]])
print(data[3])
print(data[4])
print(np.sum(data[1]))'''
