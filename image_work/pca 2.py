import numpy as np
from scipy import linalg
from scipy.io import loadmat
import matplotlib.pyplot as plt

debug = True

def load_and_center_dataset(filename):
    dataset = loadmat(filename)
    x = dataset['fea']
    n = len(x)
    d = len(x[0])

    arr = np.array(x, dtype='float64')
    mean = np.mean(arr, axis=0)
    return arr - mean


def get_covariance(dataset):
    return np.multiply(np.dot(np.transpose(dataset), dataset), 1/2414) #this number ok?

def get_eig(S, m):
    val, vec = linalg.eigh(S)
    val = val[:-(m+1):-1]
    vec = vec[:-(m+1):-1]
    return np.diag(val), np.column_stack(tuple(vec))

def project_image(image, U):
    sum = 0
    for col in U:
        alpha = np.dot(np.transpose(col), image)

def display_image(orig, proj):
    fig, ax = plt.subplots(nrows=1, ncols=2)

    for img, pos, title in zip((orig, proj), (0,1), ('Original', 'Projection')):
        img = np.reshape(img, (32,32))
        ax[pos].plot(img)
        ax[pos].set_title(title)
        a=ax.imshow(aspect='equal')
        fig.colorbar(mappable=a, ax=ax[pos])

    plt.show()

def main(): 
	#x = loadmat('YaleB_32x32.mat')
	#print(x[0])
	m = load_and_center_dataset('YaleB_32x32.mat')
	y = get_covariance(m)
	Lambda, U = get_eig(y, 2)
	print(Lambda)
	print(U)
	#projection = project_image(m[0], U)
	#print(projection)
main()
# if debug:
#     # a, b = get_eig(get_covariance(load_and_center_dataset('YaleB_32x32.mat')), 2)
#     # print(a)
#     data = load_and_center_dataset('YaleB_32x32.mat')
#     display_image(data[0], data[1])
#     # print(len(l))
    # print(len(l[0]))