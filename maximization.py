from enum import Enum
import possible_effort_splits as pes

class TimePeriod(Enum):
	tminusone = 0
	t = 1
	tplusone = 2


# Function: returns_for_young
# Calculate a return for a specific effort split of the maximizing scientist of interest in time period t
# Return: a return for that scientist in time period t
def returns_for_young(effort_on_tminusone, effort_on_t):


# Function: returns_for_old
# Calculate the returns for specific effort split of the maximizing scientist of interest in time period t+1
# Return: a return for that scientist in time period t+1
def returns_for_old(effort_on_tminusone, effort_on_t, effort_on_tplusone):

# Function: total_returns
# Takes all possible pairs pairs of the returns between the young and old version of the scientists of interest 
# and calculates the maximum total return given the young and old returns
# Return: pair of returns that produce the maximum return over both time period t and t+1
def total_returns(young_returns_options, old_returns_options):



def main():
	# Set these for now
	young_effort_constant = [0.4, 0.4]
	old_effort_constant = [0.3, 0.3, 0.3]

	# set this for now: build function for this later
	possible_young_effort_splits = [[0,4, 0.4], [0, 0.9], [0.9, 0], [0.3, 0.5], \
									[0.5, 0.3], [0.1, 0.7], [0.7, 0.1], \
									[0.6, 0.3], [0.3, 0.6]]


if __name__ == "__main__":
    main()
