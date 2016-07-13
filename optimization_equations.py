from math import e

def sigmoid(r, x):
	return 1.0/(1+e**(-(r*x)))

def main():
	print(sigmoid(1,2))

if __name__ == "__main__":
    main()
