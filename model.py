import numpy as np
import math
import matplotlib.pyplot as plt

class model:
	def __init__(self, b0:float, db:float, nb:int, xi0:float, dxi:float, nxi:int, ps:float):
		self.ps = ps
		#self.parray = np.array([[(b0+i*db, xi0+j*dxi) for j in range(nxi)] for i in range(nb)])
		self.brange = [b0+i*db for i in range(nb)]
		self.xirange = [xi0+j*dxi for j in range(nxi)]
		#self.shape = np.shape(self.parray)

	def e(self, n):
		return [1 for i in range(n)]

	def neighbors(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		neighbors = [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.xirange)))]
		narray = np.zeros((len(self.brange), len(self.xirange)), dtype=int)
		for i in neighbors: narray[i] = 1
		return narray

	def neighborcoords(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		return [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.xirange)))]

	def sim(self, v0:tuple, n0:int, s:int):
		lst1 = [] #history of infected
		lst2 = lst1.copy()
		lstS = [s]
		lstI = [n0]
		S = s #matches notation
		I1 = np.zeros((len(self.brange), len(self.xirange)), dtype=int) #tracks infected in period 1. Change variable names for clarity
		I2 = I1.copy()
		p = np.zeros((len(self.brange), len(self.xirange)), dtype=float) #p(i, j)
		st = I2.copy() #s_{t, (i, j)}
		sbart = I2.copy()
		Ibar = I2.copy()
		d = I2.copy() #delta(i, j)->(i', j')
		I1[v0] = n0 #multiple variants?
		lst1.append(I1.copy()) #current period
		lst2.append(I2.copy())
		lstS.append(S)
		while (S > 0) and (np.sum(I1)+np.sum(I2) > 0): #infected and susceptible > 0
			for i in range(len(self.brange)):
				for j in range(len(self.xirange)):
					I2[i, j] = np.random.binomial(lst1[-1][i, j], self.xirange[j]) #eq. 1
			I = np.random.binomial(S, 1-math.prod((np.subtract(1,self.brange))**(np.sum(I1, 1)+np.sum(I2, 1)))) #eq. 2
			S = lstS[-1]-I #eq. 3
			#print(I, S)
			Isum = np.sum(I1, 1)+np.sum(I2, 1)
			denom5 = np.sum(self.brange*Isum) #eq. 5 denominator
			print("Denom ", denom5)
			if denom5 > 0: #we do need this check
				for i in range(len(self.brange)):
					for j in range(len(self.xirange)):
						p[i, j] = self.brange[i]*(I1[i, j]+I2[i, j])/denom5 #eq. 5
					#print("Beta ", self.brange[i])
				#print("p ", p)
				Ibar_flat = np.random.multinomial(I, p.flatten()) #eq. 4
				#print(Ibar_flat)
				Ibar = np.reshape(Ibar_flat, (len(self.brange), len(self.xirange))) #eq. 4
			#else: Ibar = np.zeros(len(self.brange), len(self.xirange), dtype=int)
			print(Ibar)
			#print("I ", I1+I2)
			#print("Ibar ", Ibar)
			for i in range(len(self.brange)):
				for j in range(len(self.xirange)):
					st[i, j] = np.random.binomial(Ibar[i, j], self.ps) #eq. 6
					sbart[i, j] = Ibar[i, j]-st[i, j]
					darray = []
					for x in self.neighborcoords(i, j): #for every neighbor
						#print(self.neighborcoords(i, j))
						neighborParray = np.random.multinomial(sbart[x], [(1-self.ps)/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))] )
						narray = self.neighbors(i, j)
						#print(i, j)
						#print(narray)
						for x in range(len(self.brange)):
							for y in range(len(self.xirange)):
								if narray[x, y] == 1:
									last, neighborParray = neighborParray[-1], neighborParray[:-1] #pop
									darray.append(last)
					d[i, j] = np.sum(darray) #eq. 7
					I1[i, j] = st[i, j]+d[i, j]
			#print(st)
			#print("D ", d)
			#print(I1)
			lst1.append(I1.copy())
			lst2.append(I2.copy())
			lstI.append(np.sum(I1)+np.sum(I2))
			lstS.append(S)
			#print("==================================================")
		#print(lst1)
		return lst1, lst2, lstI, lstS

#np.random.seed(0)

#mod = model(.001, .001, 3, 0, 0, 1, 1) #"base" Reed-Frost

mod = model(.001, .001, 10, 0.5, 0.001, 5, .5)
lst1, lst2, lstI, lstS = mod.sim((0, 0), 60, 1500)
lstI_sep = [lst1[x]+lst2[x] for x in range(len(lst1))]
for i in lstI_sep:
	#plt.imshow(i, cmap='gray', vmin=0, vmax=255)
	plt.matshow(i)
	plt.show()
#print(lst1)
#print(lst2)

runs_I = []
runs_S = []
'''for i in range(100):
	lst1, lst2, lstI, lstS = mod.sim((0, 0), 60, 1500)
	runs_I.append(lstI)
	runs_S.append(lstS)
#plt.hist([max([i[0] for i in x]) for x in runs])
average_dis = [sum(x)/len(x) for x in zip(*runs_I)]
std_dis = [np.std(x) for x in zip(*runs_I)]
print(average_dis)
print(std_dis)
plt.plot([x for x in range(len(average_dis))], average_dis)
plt.plot([x for x in range(len(std_dis))], std_dis)
plt.show()'''