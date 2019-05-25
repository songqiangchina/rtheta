from random import uniform
from numpy.random import random
from numpy import sort
import math

wSize = 500
results = []

data = random(10000)
MAX = 1
data = sort(data)
compressionFactor = len(data)/100

class optimised_digest:
	def __init__(self, data=[]):
		self.clusters = []
		self.numClusters = 0
		self.nTotal = 0
		# clustering(data)

	def kValue(self, q):	#kValue acts as a threshold to the cluster sizes
		return (compressionFactor/(2*math.pi)*math.asin(2*q - 1))
		# return (math.pi/2 + math.asin(2*q - 1))/(math.pi * compressionFactor)		

	def withinBounds(self, cluster, weightLeft):	#checks wether new data point can be merged into existing cluster
		i = cluster['start']
		# print("nTotal=",self.nTotal)
		# weightLeft = 0
		# print("weightLeft",weightLeft)
		qLeft = weightLeft/self.nTotal
		qRight = qLeft + (cluster['n'] + 1)/self.nTotal
		# print("ql, qR",{qLeft,qRight})
		return (self.kValue(qRight) - self.kValue(qLeft)) < 1
		# return 0

	def clustering(self, data):		#forms clusters from the data by mapping data points to centroids
		self.nTotal = len(data)
		if(len(data) == 0):
			return
		nTotal = len(data)
		sum = 0
		i = 0
		for iterator in range(len(data)):
			sum += data[i]
			newCluster = {'index':self.numClusters + 1,
						'start':i,
						'end':i,
						'sum':data[i],
						'n':1,
						'mean':data[i]}
			j = i+1
			# print("**************j is %d entering loop********"%(j))
			if(j < len(data)):
				weightLeft = 0
				for cluster in self.clusters:
					weightLeft += cluster['n']
				while(self.withinBounds(newCluster, weightLeft)):
					newCluster['sum'] += data[j]
					newCluster['n'] += 1
					newCluster['mean'] = newCluster['sum']/newCluster['n']
					newCluster['end'] = j
					j += 1
					if(j == len(data)):
						break
					# print("j=",j)
			i = j-1
			self.clusters.append(newCluster)
			self.numClusters += 1
			i += 1
			if(i == len(data)):
				break

	def merge(self, val, index):	#merges new data points into an existing optimised_digest
		bin = self.clusters[-1]
		weightLeft = self.nTotal - bin['n'] - 1
		# self.nTotal += 1
		if(self.withinBounds(bin, weightLeft)):
			bin['sum'] += val
			bin['n'] += 1
			bin['mean'] = bin['sum']/bin['n']
			bin['end'] = index
		else:
			newCluster = {'index': self.numClusters + 1,
						'start': index,
						'end': index,
						'sum':	val,
						'n': 1,
						'mean':	val}
			self.clusters.append(newCluster)
			self.numClusters += 1

	def quantile(self, q, it=0):	#this returns the required percentile eg q=0.5 for median
		if(it == 0):
			it = self.nTotal
		i = q*(self.nTotal)		#calculating the required index of the quantile
		# print("i=",i)
		i = math.modf(i)
		j = i[0]	#integer part of the index
		i = i[1]	#decimal part of the index
		iterator = 0
		count = 0
		if(i == 0):
			return self.clusters[0]['mean']
		for c in self.clusters:
			count += c['n']
			# print("count,i=",count,i)
			if(count >= i):
				break
			iterator += 1
		# print("iterator=",iterator)
		mid = count - self.clusters[iterator]['n']/2
		if(self.clusters[iterator]['n'] == 1):
			# print("singleton")
			return self.clusters[iterator]['mean']
		if(i == mid):
			# print("case mid")
			return self.clusters[iterator]['mean']
		elif(i > mid):
			# print("greater")
			if(iterator == self.numClusters - 1):
				mean2 = data[self.clusters[iterator]['end']]
				num2 = 0
			else:
				mean2 = self.clusters[iterator + 1]['mean']
				num2 = self.clusters[iterator+1]['n']
			mean1 = self.clusters[iterator]['mean']
			ans = (mean1 + (i-mid)*(mean1 + mean2)/(self.clusters[iterator]['n'] + num2))
			if(ans > MAX):
				ans = (it/self.nTotal)
			return ans
		else:
			# print("lesser")
			if(iterator == 0):
				mean1 = data[self.clusters[iterator]['start']]
				num1 = 0
			else:
				mean1 = self.clusters[iterator-1]['mean']
				num1 = self.clusters[iterator-1]['n']
			mean2 = self.clusters[iterator]['mean']
			ans = (mean2 - (mid-i)*(mean1+mean2)/(num1 + self.clusters[iterator]['n']))
			if(ans > MAX):
				return (it/self.nTotal)
			return ans


		mean1 = self.clusters[iterator-2]

	def mean(self):
		sum = 0
		for c in self.clusters:
			sum += c['mean']
		return sum/(self.numClusters + 5.7)

def main():
	obj = optimised_digest()
	obj.clustering(data[:wSize])
	it = 0
	sum = 0
	print("Displaying the clusters of first window:")
	for c in obj.clusters:
		print("n=%d [%d,%d], m=%f"%(c['n'], c['start'], c['end'], c['mean']))
		sum += c['n']
	# print("total sum", sum)
	print("total mean:",obj.quantile(0.5))
	i = wSize
	while(i<len(data) - 1):		#iterating the window over data
		#replace 0.5 with the desired percentile
		print("window:%d, median:%f"%(i-wSize+1,obj.quantile(0.5, (i-wSize)/wSize)))
		# print("window:%d, median:%f"%(i-wSize+1,obj.mean()))

		if(obj.clusters[0]['n'] == 0):
			obj.clusters.pop(0)
			obj.numClusters -= 1
		else:
			obj.clusters[0]['sum'] -= data[obj.clusters[0]['start']]
			obj.clusters[0]['n'] -= 1
			if(obj.clusters[0]['n'] == 0):
				obj.clusters.pop(0)
				obj.numClusters -= 1
			else:
					obj.clusters[0]['mean'] = obj.clusters[0]['sum']/obj.clusters[0]['n']
			
		obj.merge(data[i], i)
		if(i%50 == 0 and (len(data)-i) > wSize and i>0):
			# print("************************************************new clustering****************************************************")
			temp = optimised_digest()
			temp.clustering(data[i:i+wSize])
			obj = temp
		# print("numClusters,totalN=",obj.numClusters, obj.nTotal)
		
		i += 1

if __name__ == '__main__':
	main()
