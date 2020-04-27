"""
Header: 

Name of File: p1_weather.py
Other Files: p1_statespace.py
Author: Tejvir Mann
Class: CS 540 
Description of Program: This program contains methods that are responsible for 
calculating the distance between points. This program reads the data file. 
This program calculates the nearest k neighbors. This program creates a majority vote.
"""

import math #imports 
import json
import numpy as np

# this method is designed to calculate the distance between two data points 
def euclidean_distance(data_point1, data_point2): 
	tmax1 = data_point1['TMAX']
	tmin1 = data_point1['TMIN'] #the x, y ,and z
	prcp1 = data_point1['PRCP']
	tmax2 = data_point2['TMAX']
	tmin2 = data_point2['TMIN']
	prcp2 = data_point2['PRCP']
	
	x = tmax1 - tmax2 #gets x diff 
	x = math.pow(x, 2)

	y = tmin1 - tmin2
	y = math.pow(y, 2) #gets y diff

	z = prcp1 - prcp2
	z = math.pow(z, 2) #gets z diff

	t = x + y + z #adds all together 

	t = math.sqrt(t) # gets sqrt
	return t 

# this method is meant to read the dataset and parse it into a dictionary. 
def read_dataset(filename):
	d = {}
	i = 0
	with open(filename) as f: #opens file, and parses it. 
		for line in f:
			DATE, PRCP, TMAX, TMIN, RAIN = line.split(" ")
			d[i] = {'DATE' : DATE, 'TMAX' : float(TMAX), 'PRCP' : float(PRCP), 'TMIN' : float(TMIN), 'RAIN' : RAIN}
			i += 1 

	return d

#this method gets all the nearest neigbors and calculates if it is going to rain or not.
def majority_vote(nearest_neighbors):
	q = float(0)
	n = nearest_neighbors
	for i in n:  #opens file 
		m = n[i]['PRCP']
		if m > 0.00:
			q += 1 
			#print(len(nearest_neighbors))
	if q/len(nearest_neighbors) < 0.5: # calculates the percent
		return 'FALSE'

	else: 
		return 'TRUE'

def k_nearest_neighbors(filename, test_point, k):
	j = 0
	l = 0
	p = 0
	m = {}
	b = {}
	c = []
	r = {}
	final = []
	s = 0
	t = 0 

	with open(filename) as f: #opens the file, gets the euclidean distances 
		for line in f:
			DATE, PRCP, TMAX, TMIN, RAIN = line.split(" ")
			m[j] = {'DATE' : DATE, 'TMAX' : float(TMAX), 'PRCP' : float(PRCP), 'TMIN' : float(TMIN), 'RAIN' : RAIN}
			x = euclidean_distance(test_point, m[j])
			c.append(x)
			j += 1
			p += 1

		c = sorted(c) #sort the distances 
		del c[k:] 

		d = []
		[d.append(x) for x in c if x not in d] #removes duplicates

		for i in d: #matches the distances to the right data, adds the data o a list 
			with open(filename) as f:
				for line in f: 
					DATE, PRCP, TMAX, TMIN, RAIN = line.split(" ")
					r[s] = {'DATE' : DATE, 'TMAX' : float(TMAX), 'PRCP' : float(PRCP), 'TMIN' : float(TMIN), 'RAIN' : RAIN}
					x = euclidean_distance(test_point, r[s])
					i  = float("{0:.17f}".format(i))
					if i == x: 
						b[l] = r[s]
						l += 1	
	return b #returns the list of close datapoints 

# def main():
# 	dataset = read_dataset('rain.txt')
# 	x = euclidean_distance(dataset[5], dataset[1])
# 	q = k_nearest_neighbors('rain.txt', dataset[5], 10)
# 	n = majority_vote(q)
# 	print(n)


# main()
