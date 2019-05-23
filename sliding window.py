from tdigest import TDigest
from numpy.random import random

wSize = 100		#size of the sliding window
results = []	#this will store the quantile value for each window

#helper function to print values in digest
def printDigest(digest, range):
	j=0
	for i in digest:
		j += 1
		print(i)
		if(j>range):
			break

def main():
	data = random(1000)

	i = 0
	for i in range(0,(len(data) - wSize + 1)):
		digest = TDigest()
		digest.batch_update(data[i:i+wSize])
		results.append([i+1,digest.percentile(15)])
		i += 1
	print(results)
if __name__ == '__main__':
	main()