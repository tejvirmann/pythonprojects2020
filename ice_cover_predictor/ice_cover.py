import math 
import csv
import random

'''
Name: Tejvir Mann
Project: ice_cover.py
Class: CS 540

'''

def norm_random(beta_0, beta_1, x_mean, std):
	b_0 = float(0)
	b_1 = float(0)
	dataset = get_dataset()
	n = len(dataset)
	val = random.randint(0,n-1)

	x = float(dataset[val][0] - x_mean)
	x = float(x/std)

	y = dataset[val][1]

	b_0 = float(2*(beta_0+(beta_1*x) - y))
	b_1 = float(2*(beta_0+(beta_1*x) - y)*x)

	return (b_0,b_1)

def norm_descent(beta_0, beta_1, x_mean, std):
	dataset = get_dataset()
	mean= float(0)
	mean_1 = float(0)

	#getting b_0. mean = b_0
	for i in range(165):
		x = float(dataset[i][0] - x_mean)
		x = float(x/std)
		mean += float(((beta_0 + (beta_1*x)) - dataset[i][1]))

	mean = 2 * (float(mean/float(165)))

	#getting b_1. mean_1 = b_1
	for i in range(165):
		y = float(dataset[i][0] - x_mean)
		y = float(y/std)
		mean_1 += float(((beta_0 + (beta_1*y)) - dataset[i][1])*(y))

	mean_1 = float(2 * (float(mean_1/float(165))))

	return (mean,mean_1)

'''
mean squared error for norm x
'''
def norm_reg(beta_0, beta_1, x_mean ,std):
	dataset = get_dataset()
	mean= float(0)

	for i in range(165):
		x = float(dataset[i][0] - x_mean)
		x = float(x/std)
		mean += float(math.pow(float(float(beta_0 + float(beta_1*x)) - dataset[i][1]),2))

	mean = float(mean/float(165))

	return mean

def check():
	datarr = get_dataset()
	data = []

	with open('./a.csv') as csvDataFile:
	    csvReader = csv.reader(csvDataFile)
	    for row in csvReader:
	        row = [item.rstrip('\n') for item in row]
	        #row = [item.split(',') for item in row]
	        data.append(row)

	print(data)

	for i in range(len(datarr)):
		if str(datarr[i][1]) != data[i][0]:
			print(datarr[i][0])
			print(datarr[i][1])
			print(data[i])

def get_dataset():
	dataset = [[1855,118],[1856,151],[1857,121],[1858,96],[1859,110]
				,[1860,117],[1861,132],[1862,104],[1863,125],[1864,118]
				,[1865,125],[1866,123],[1867,110],[1868,127],[1869,131]
				,[1870,99],[1871,126],[1872,144],[1873,136],[1874,126]
				,[1875,91],[1876,130],[1877,62],[1878,112],[1879,99]
				,[1880,161],[1881,78],[1882,124],[1883,119],[1884,124]
				,[1885,128],[1886,131],[1887,113],[1888,88],[1889,75]
				,[1890,111],[1891,97],[1892,112],[1893,101],[1894,101]
				,[1895,91],[1896,110],[1897,100],[1898,130],[1899,111]
				,[1900,107],[1901,105],[1902,89],[1903,126],[1904,108]
				,[1905,97],[1906,94],[1907,83],[1908,106],[1909,98]
				,[1910,101],[1911,108],[1912,99],[1913,88],[1914,115]
				,[1915,102],[1916,116],[1917,115],[1918,82],[1919,110]
				,[1920,81],[1921,96],[1922,125],[1923,104],[1924,105]
				,[1925,124],[1926,103],[1927,106],[1928,96],[1929,107]
				,[1930,98],[1931,65],[1932,115],[1933,91],[1934,94]
				,[1935,101],[1936,121],[1937,105],[1938,97],[1939,105]
				,[1940,96],[1941,82],[1942,116],[1943,114],[1944,92]
				,[1945,98],[1946,101],[1947,104],[1948,96],[1949,109]
				,[1950,122],[1951,114],[1952,81],[1953,85],[1954,92]
				,[1955,114],[1956,111],[1957,95],[1958,126],[1959,105]
				,[1960,108],[1961,117],[1962,112],[1963,113],[1964,120]
				,[1965,65],[1966,98],[1967,91],[1968,108],[1969,113]
				,[1970,110],[1971,105],[1972,97],[1973,105],[1974,107]
				,[1975,88],[1976,115],[1977,123],[1978,118],[1979,99]
				,[1980,93],[1981,96],[1982,54],[1983,111],[1984,85]
				,[1985,107],[1986,89],[1987,87],[1988,97],[1989,93]
				,[1990,88],[1991,99],[1992,108],[1993,94],[1994,74]
				,[1995,119],[1996,102],[1997,47],[1998,82],[1999,53]
				,[2000,115],[2001,21],[2002,89],[2003,80],[2004,101]
				,[2005,95],[2006,66],[2007,106],[2008,97],[2009,87]
				,[2010,109],[2011,57],[2012,87],[2013,117],[2014,91]
				,[2015,62],[2016,65],[2017,94],[2018,86],[2019,70]]
	return dataset

'''
datapoints, mean anad s-deviation
'''
def print_stats(dataset):
	#number of datapoints
	data_points = len(dataset)
	print(data_points)

	#mean
	total = 0
	for i in range(len(dataset)):
		total += dataset[i][1]
	mean = float(total/data_points)
	print(round(mean,2))

	#print standard deviation
	dev = 0
	for i in range(len(dataset)):
		dev += math.pow((dataset[i][1] - mean),2)
	dev = (dev/(data_points-1))
	dev = math.sqrt(dev)
	print(round(dev,2))

'''
mean squared error
'''
def regression(beta_0, beta_1):
	dataset = get_dataset()
	mean= float(0)

	for i in range(165):
		mean += float(math.pow(((beta_0 + (beta_1*dataset[i][0])) - dataset[i][1]),2))

	mean = float(mean/float(165))
	mean = round(mean,2)

	return mean

def gradient_descent(beta_0, beta_1):
	derivative = 0

	dataset = get_dataset()
	mean= float(0)
	mean_1 = float(0)

	#getting b_0. mean = b_0
	for i in range(165):
		mean += float(((beta_0 + (beta_1*dataset[i][0])) - dataset[i][1]))

	mean = 2 * (float(mean/float(165)))
	mean = round(mean,2)

	#getting b_1. mean_1 = b_1
	for i in range(165):
		mean_1 += float(((beta_0 + (beta_1*dataset[i][0])) - dataset[i][1])*(dataset[i][0]))

	mean_1 = 2 * (float(mean_1/float(165)))
	mean_1 = round(mean_1,2)

	return (mean,mean_1)

def iterate_gradient(T,eta):

	t = 0
	b0_new = float(0)
	b0_old = float(0)
	b1_new = float(0)
	b1_old = float(0)

	m = gradient_descent(b0_old,b1_old)
	b0_new = float(b0_old - float(eta* m[0]))
	b1_new = float(b1_old - float(eta* m[1]))
	mse = regression(b0_new,b1_new)

	print(str(t+1) + " " + str(round(b0_new,2)) + " " + str(round(b1_new,2)) + " " + str(round(mse,2)))

	b0_old = b0_new
	b1_old = b1_new

	while (t <= T-2):
		m = gradient_descent(b0_old,b1_old)
		b0_new = float(b0_old - float(eta* m[0]))
		b1_new = float(b1_old - float(eta* m[1]))
		mse = regression(b0_new,b1_new)

		#print
		print(str(t+2) + " " + str(round(b0_new,2)) + " " + str(round(b1_new,2)) + " " + str(round(mse,2)))

		b0_old = b0_new
		b1_old = b1_new
		t += 1

def compute_betas():
	dataset = get_dataset()
	n = len(dataset)

#x
	x = float(0)
	for i in range(n):
		x += float(dataset[i][0])
	x = float(x/n)

#y
	y = float(0)
	for i in range(n):
		y += float(dataset[i][1])
	y = float(y/n)

	#sum top
	sum_t = float(0)
	for i in range(n):
		sum_t += (float(dataset[i][0]-x)*float(dataset[i][1]-y))

	#sum bottom
	sum_b = float(0)
	for i in range(n):
		sum_b += float(math.pow((dataset[i][0]-x),2))

	b_1 = float(sum_t/sum_b)
	b_0 = float(float(y) - float(b_1*x))
	mse = regression(b_0,b_1)

	# b_1 = round(b_1,2)
	# b_0 = round(b_0,2)
	# mse = round(mse,2)

	return (b_0,b_1,mse)

def predict(year):
	x = compute_betas()
	prediction = 0
	prediction = float(float(x[0]) + float(x[1]*year))
	prediction = round(prediction,2)
	return prediction

def iterate_normalized(T,eta):

	#get the new version of x
	dataset = get_dataset()
	n = len(dataset)
	total = float(0)
	for i in range(n):
		total += float(dataset[i][0])
	x = float(total/n)

	#get std
	std = float(0)
	for i in range(n):
		std += float(math.pow((float(dataset[i][0] - x)),2))
	std = float(std/(n-1))
	std = float(math.sqrt(std))

	#same thing as iterate, but with a new mse method
	t = 0

	#normal iterative 
	b0_new = float(0)
	b0_old = float(0)
	b1_new = float(0)
	b1_old = float(0)

	m = norm_descent(b0_old,b1_old,x,std)
	b0_new = float(b0_old - float(eta* m[0]))
	b1_new = float(b1_old - float(eta* m[1]))
	mse = float(norm_reg(b0_new,b1_new,x,std))

	print(str(t+1) + " " + str(round(b0_new,2)) + " " + str(round(b1_new,2)) + " " + str(round(mse,2)))

	b0_old = b0_new
	b1_old = b1_new

	while (t <= T-2):
		m = norm_descent(b0_old,b1_old,x,std)
		b0_new = float(b0_old - float(eta* m[0]))
		b1_new = float(b1_old - float(eta* m[1]))
		mse = float(norm_reg(b0_new,b1_new,x,std))

		#print
		print(str(t+2) + " " + str(round(b0_new,2)) + " " + str(round(b1_new,2)) + " " + str(round(mse,2)))

		b0_old = b0_new
		b1_old = b1_new
		t += 1

'''
random
'''
def sgd(T,eta):

	#get the new version of x
	dataset = get_dataset()
	n = len(dataset)
	total = float(0)
	for i in range(n):
		total += float(dataset[i][0])
	x = float(total/n)

	#get std
	std = float(0)
	for i in range(n):
		std += float(math.pow((float(dataset[i][0] - x)),2))
	std = float(std/(n-1))
	std = float(math.sqrt(std))

	#same thing as iterate, but with a new mse method
	t = 0

	#normal iterative 
	b0_new = float(0)
	b0_old = float(0)
	b1_new = float(0)
	b1_old = float(0)

	m = norm_random(b0_old,b1_old,x,std) #used to be norm descent, now norm_rando
	b0_new = float(b0_old - float(eta* m[0]))
	b1_new = float(b1_old - float(eta* m[1]))
	mse = float(norm_reg(b0_new,b1_new,x,std))

	print(str(t+1) + " " + str(round(b0_new,2)) + " " + str(round(b1_new,2)) + " " + str(round(mse,2)))

	b0_old = b0_new
	b1_old = b1_new

	while (t <= T-2):
		m = norm_random(b0_old,b1_old,x,std)
		b0_new = float(b0_old - float(eta* m[0]))
		b1_new = float(b1_old - float(eta* m[1]))
		mse = float(norm_reg(b0_new,b1_new,x,std))

		#print
		print(str(t+2) + " " + str(round(b0_new,2)) + " " + str(round(b1_new,2)) + " " + str(round(mse,2)))

		b0_old = b0_new
		b1_old = b1_new
		t += 1


# def main():
# 	# y = get_dataset()
# 	# x = print_stats(y)
# 	# y = compute_betas()
# 	# x = predict(2021)
# 	# print(y)
# 	# print(x)
# 	x = sgd(5, 0.1)
# 	#print(x)
# 	# x = check()

# main()






