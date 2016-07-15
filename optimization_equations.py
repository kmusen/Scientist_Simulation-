from math import e
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(r, x):
	return 1.0/(1+e**(-(r*x)))

def modified_sigmoid(r, z, x):
	return (sigmoid(r, x+z) - sigmoid(r, z))/(1-sigmoid(r, z))

#def modified_sigmoid(r, x, z):
	return sigmoid(r, x+z)

def graph_sigmoid(r, x_min, x_max, num_of_intervals):
	x_range = np.linspace(x_min, x_max, num_of_intervals)
	y = []
	for x in x_range:
		y.append(sigmoid(r, x))
	plt.plot(x_range,y)
	plt.show()

def graph_modified_sigmoid(r, z, x_min, x_max, num_of_intervals):
	x_range = np.linspace(x_min, x_max, num_of_intervals)
	y = []
	for x in x_range:
		y.append(modified_sigmoid(r, z, x))
	plt.plot(x_range, y)
	plt.show()

def main():
	# graph_sigmoid(1, -5, 5, 50)
	graph_modified_sigmoid(0.3035, -0.4643, -5, 5, 15)


if __name__ == "__main__":
    main()
