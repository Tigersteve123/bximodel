import numpy as np
import math
#import concurrent.futures as futures

#from multiprocessing import Process

class model:
	def __init__(self, b0:float, db:float, nb:int, g0:float, dg:float, ng:int, ps:float):
		self.ps = ps
		self.brange = [b0+i*db for i in range(nb)]
		self.grange = [g0+j*dg for j in range(ng)]

	def e(self, n):
		return [1 for i in range(n)]

	def neighbors(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		neighbors = [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.grange)))]
		narray = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		for i in neighbors: narray[i] = 1
		return narray

	def neighborcoords(self, i, j):
		neighbors = [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]
		return [x for x in neighbors if (x[0] in range(len(self.brange)) and x[1] in range(len(self.grange)))]

	def sim(self, s:int, i0:np.ndarray, tc=0, acc=0):
		lst1 = [] #history of infected
		lst2 = lst1.copy()
		lstS = [s]
		lstI = [np.sum(i0)]
		lstAvg = []
		lstCumAvg = []
		lstQS = [0]
		lstQI1 = [np.zeros((len(self.brange), len(self.grange)), dtype=int)]
		lstQI2 = [np.zeros((len(self.brange), len(self.grange)), dtype=int)]
		I1 = i0 #tracks infected in period 1
		I2 = np.zeros((len(self.brange), len(self.grange)), dtype=int)
		p = np.zeros((len(self.brange), len(self.grange)), dtype=float) #p(i, j)
		S = s
		st = I2.copy() #s_{t, (i, j)}
		sbart = I2.copy()
		Ibar = I2.copy()
		d = I2.copy() #delta(i, j)->(i', j')
		lst1.append(I1.copy()) #current period
		lst2.append(I2.copy())
		totalSplitTotal = np.zeros((len(self.brange), len(self.grange)), dtype=int)

		def eq1(i, j):
			I2[i, j] = np.random.binomial(lst1[-1][i, j], self.grange[j])
		def eq5(i, j):
			p[i, j] = self.brange[i]*(I1[i, j]+I2[i, j])/denom5
		def eq67(i, j):
			st[i, j] = np.random.binomial(Ibar[i, j], self.ps) #eq. 6
			sbart[i, j] = Ibar[i, j]-st[i, j]
			darray = []
			for x in self.neighborcoords(i, j): #for every neighbor
				probs = [1/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))]
				neighborParray = np.random.multinomial(sbart[x], probs)
				print(sbart[x], neighborParray)
				narray = self.neighbors(i, j)
				for x in range(len(self.brange)):
					for y in range(len(self.grange)):
						if narray[x, y] == 1:
							last, neighborParray = neighborParray[-1], neighborParray[:-1] #pop
							darray.append(last)
			d[i, j] = np.sum(darray) #eq. 7
			I1[i, j] = st[i, j]+d[i, j] #eq. 8

		while (S > 0) and (np.sum(I1)+np.sum(I2) > 0): #infected and susceptible > 0
			totalSplitI = I1+I2
			totalSplitTotal += I1+I2
			averageB = np.sum(np.sum(totalSplitI, 1)*self.brange)/np.sum(totalSplitI)
			averageG = np.sum(np.sum(totalSplitI, 0)*self.grange)/np.sum(totalSplitI)
			averageBCum = np.sum(np.sum(totalSplitTotal, 1)*self.brange)/np.sum(totalSplitTotal)
			averageGCum = np.sum(np.sum(totalSplitTotal, 0)*self.grange)/np.sum(totalSplitTotal)
			
			QI1 = np.zeros((len(self.brange), len(self.grange)), dtype=int)
			QI2 = QI1.copy()
			
			tau = min(tc/(np.sum(totalSplitI)+S), 1) #eq. 11
			TS = np.random.binomial(S, tau) #eq. 12
			QS1 = np.random.binomial(TS, 1-acc) #eq. 13
			QS2 = lstQS[-1] #eq. 14
			S = lstS[-1]-QS1+QS2 #eq. 15
			
			'''for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					TI1 = np.random.binomial(I1[i, j], tau) #eq. 16
					Q1 = np.random.binomial(TI1, acc) #eq. 17
					I1[i, j] -= Q1 #eq. 18
					QI1[i, j] = Q1
					TI2 = np.random.binomial(I2[i, j], tau)
					Q2 = np.random.binomial(TI2, acc)
					I2[i, j] -= Q2
					QI2[i, j] = Q2'''
						
			
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					TI1 = np.random.binomial(I1[i, j], tau) #eq. 16
					Q1 = np.random.binomial(TI1, acc) #eq. 17
					I1[i, j] -= Q1 #eq. 18
					QI1[i, j] = Q1
					TI2 = np.random.binomial(I2[i, j], tau)
					Q2 = np.random.binomial(TI2, acc)
					I2[i, j] -= Q2
					QI2[i, j] = Q2
					eq1(i, j)
			I = np.random.binomial(S, 1-math.prod((np.subtract(1,self.brange))**(np.sum(I1, 1)+np.sum(I2, 1)))) #eq. 2
			S = S-I #eq. 3
			Isum = np.sum(I1, 1)+np.sum(I2, 1)
			denom5 = np.sum(self.brange*Isum) #eq. 5 denominator
			if denom5 > 0: #we do need this check
				for i in range(len(self.brange)):
					for j in range(len(self.grange)):
						eq5(i, j)
				Ibar_flat = np.random.multinomial(I, p.flatten()) #eq. 4
				Ibar = np.reshape(Ibar_flat, (len(self.brange), len(self.grange))) #eq. 4
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					st[i, j] = np.random.binomial(Ibar[i, j], self.ps) #eq. 6
					sbart[i, j] = Ibar[i, j]-st[i, j]
			I1 = st.copy()
			for i in range(len(self.brange)):
				for j in range(len(self.grange)):
					probs = [1/len(self.neighborcoords(i, j)) for a in range(len(self.neighborcoords(i, j)))]
					neighborParray = np.random.multinomial(sbart[i, j], probs)
					narray = self.neighborcoords(i, j)
					#print(narray)
					for x in range(len(narray)):
						I1[narray[x]] = I1[narray[x]]+neighborParray[x]
			lst1.append(I1.copy())
			lst2.append(I2.copy())
			lstI.append(np.sum(I1)+np.sum(I2))
			lstS.append(S)
			lstAvg.append((averageB.copy(), averageG.copy()))
			lstCumAvg.append((averageBCum, averageGCum))
			lstQS.append(QS1)
			lstQI1.append(QI1)
			lstQI2.append(QI2)
		return np.array(lst1), np.array(lst2), np.array(lstI), np.array(lstS), np.array(lstAvg), np.array(lstCumAvg), np.array(lstQS), np.array(lstQI1), np.array(lstQI2)
