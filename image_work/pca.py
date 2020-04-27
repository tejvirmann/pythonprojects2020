'''
Name: Tejvir Mann
Program: PCA.py
Professor: Jerry Zhu
Date: 03/7/20
'''
import numpy as np
from scipy.io import loadmat
from scipy import linalg as li
from scipy.linalg import eigh
import math
import matplotlib.pyplot as plt

 
def load_and_center_dataset(filename):
	dataset = loadmat(filename)
	x = (dataset['fea'])
	n = len(x)
	d = len(x[0])
	arr = np.array(x, dtype='float64')
	mean = np.mean(arr, axis=0)

	return arr- mean


def get_covariance(dataset):
	
	m = len(dataset)
	x = np.dot(np.transpose(dataset), dataset)
	y = np.true_divide( np.dot(np.transpose(dataset), dataset), (m-1))
	return y

	'''
	eigen decomposition on Matrix S
	return a diagonal matrix (numpy array)
	with the largest eigenvalues on the diagonal. 

	AND

	a matrix (NumPy array) with the corresponding 
	eigenvectors as columns
	'''
def get_eig(S,m):

    a, b = li.eigh(S)
    a = a[:-(m+1):-1]
    b = b[:-(m+1):-1]

    b = np.column_stack(tuple(b))
    return np.diag(a), b 

def project_image(image, U):
	#dot product the image vector with the eiganvector matrix. 
	first = np.dot(image, U)

	# #Then dot that result with the transpose of the eiganvector matrix
	aij = np.dot(first, np.transpose(U))

	return aij

def display_image(orig, proj):

    fig, ax = plt.subplots(nrows=1, ncols=2)

    for img, pos, title in zip((orig, proj), (0,1), ('Original', 'Projection')):
        img = np.reshape(img, (32,32))
        ax[pos].plot(img)
        ax[pos].set_title(title)
        image = ax[pos].imshow(img, aspect='equal') #a = ax.
        plt.colorbar(image, ax = ax[pos], orientation='vertical') #mappable=a,ax=ax[pos]

    plt.show()


def main(): 
	#x = loadmat('doggo.jpg')
	#print(x[0])
	m = load_and_center_dataset('YaleB_32x32.mat')
	y = get_covariance(m)
	Lambda, U = get_eig(y, 2)
	#print(Lambda)
	#print(U)
	projection = project_image(m[2], U)
	print(projection)
	display_image(m[2], projection)


	


main()





