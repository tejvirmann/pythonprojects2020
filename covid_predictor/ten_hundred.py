import csv
import math
import copy
"""
Project: ten_hundred.py
Author: Tejvir Mann
Class: CS 540


"""
'''
This function loads in the data and returns them in 
an array.
'''
def load_data(filepath):
	data = []

	with open(filepath) as csvDataFile:
	    csvReader = csv.reader(csvDataFile)
	    for row in csvReader:
	        row = [item.rstrip('\n') for item in row]
	        row = [item.split(',') for item in row]
	        data.append(row)

	    data.pop(0)

	for row in data: 
		row.pop(2)
		row.pop(2)

	return data

'''
After getting the array. 

Gets difference for day 'n' and dat 'n'/10
and day 'n/10' and 'n/100' or less

If not enough data, then x,y is 0,0
'''
def calculate_x_y(time_series):
	calc = []

	nan = False
	n = float(time_series[len(time_series)-1][0]) #the biggest
	index_n = len(time_series)-1
	n10 = float(0)
	index_n10 = 0
	n100 = float(0)
	index_n100 = 0

	for j in reversed(range(len(time_series))):
		if j == 1: #then you have reached the name of the region, ran out of data.
			nan = True
			return [0,0]
		if float(time_series[j][0]) <= float(n/10):
			n10 = float(time_series[j][0])
			index_n10 = j
			break

	if(nan == False):
		for k in reversed(range(len(time_series))):
			if k == 1: #same as other j time
				break
			if float(time_series[k][0]) <= float(n/100):
				n100 = float(time_series[k][0])
				index_n100 = k

				#now get x and y 

				x = index_n - index_n10
				y = index_n10 - index_n100

				return[x,y]
				break

	if(nan == True):
		return [0,0]

	return [0,0]
	

def dist(point1, point2):

	x = point1[0] - point2[0]  #gets x diff 
	x = math.pow(x, 2)

	y = point1[1] - point2[1]
	y = math.pow(y, 2) #gets y diff

	t = x + y  #adds all together 

	t = math.sqrt(t) # gets sqrt
	return t 


def hac(dataset):

	#removes all of the NANs :11 so before 256 -> 245
	dataset[:] = (value for value in dataset if value != [0,0])
	cluster_count = len(dataset)
	m = len(dataset)
	iteration = 1
	cluster = copy.deepcopy(dataset)
	cluster_tracker = []

	while(cluster_count > 1):
		distances = []

		for i in range(len(cluster)): 
			if cluster[i] == None: 
				continue

			if i < m:
				#this way #if less than m 
					for j in range(len(cluster)):
						if cluster[j] == None: 
							continue
						if i == j: #so you aren't checking distance of stuff in the same cluster
							continue
						if j < m:
							#both have 1 in the cluster 
							distances.append([(dist(cluster[i], cluster[j])), i, j, 0, 0, 1]) 

						else: #j has more than 1, and i has 1
							for l in range(len(cluster[j])): #gets the second point 
								distances.append([(dist(cluster[i], cluster[j][l])), i, j, 0, l, 2])

			else:
				for k in range(len(cluster[i])): #gets the first point
					for j in range(len(cluster)):
						if cluster[j] == None: 
							continue
						if i == j: 
							continue
						if j < m:
							#then here j has 1 and i does not 
							distances.append([(dist(cluster[i][k], cluster[j])), i, j, k, 0, 3])

						else: #i and j have more than 1 in the cluster
							for l in range(len(cluster[j])): #gets the second point 
								distances.append([(dist(cluster[i][k], cluster[j][l])), i, j, k, l, 4]) 


		#get the min distance 
		distances.sort(key=lambda x: x[0])
		k = 0 #for tie breaking

		#if there is a tie
		if distances[0][0] == distances[0][1]:
			if distances[0][1] < distances[1][1]:
				k = 0

			if distances[0][1] == distances[1][1]:
				if distances[0][2] < distances[1][2]:
					k = 0
				else:
					k = 1

			if distances[0][1] > distances[1][1]:
				k = 1

		smallest = distances[0][0]
		c1 = distances[k][1] #cluster 1 location
		c2 = distances[k][2] #cluster 2 location
		l1 = distances[k][3] # of points in c1
		l2 = distances[k][4] # of points in c2
		opt = distances[k][5]

		#add all the distances in both i and j into 
		#a array
		temp = []

		if opt == 1: #both 1
			temp.append(cluster[c1])
			temp.append(cluster[c2])

		if opt == 2: # i = 1
			temp.append(cluster[c1])
			for l2 in range(len(cluster[c2])):
				# print(cluster[c2][l2])
				# print("F")
				temp.append(cluster[c2][l2])

		if opt == 3:
			temp.append(cluster[c2])
			#print(temp)
			for l1 in range(len(cluster[c1])):
				temp.append(cluster[c1][l1])
			#print(temp)

		if opt == 4:
			for l1 in range(len(cluster[c1])):
				temp.append(cluster[c1][l1])
			for l2 in range(len(cluster[c2])):
				temp.append(cluster[c2][l2])

		#add this array to cluster
		curr = copy.deepcopy(temp)
		cluster.append(curr)

		#set i and j to none in cluster
		cluster[c1] = None
		cluster[c2] = None

		#add i, j, distances and the number of added to cluster tracker
		if c2 > c1:
			cluster_tracker.append([c1, c2, smallest, len(curr)])

		else:
			cluster_tracker.append([c2, c1, smallest, len(curr)])

		#after done
		cluster_count = cluster_count - 1
		iteration += 1

	return cluster_tracker


# def main():
# 	time_series = load_data('./time_series_covid19_confirmed_global.csv')
# 	calc = []
# 	for i in range(len(time_series)):
# 		x = calculate_x_y(time_series[i])
# 		calc.append(x)
# 	hac_alg = hac(calc)
# 	print(hac_alg)


# main()

