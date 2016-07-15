from enum import Enum
import itertools
import possible_effort_splits as pes
from classes import *

class TimePeriod(Enum):
	tminusone = 0
	t = 1
	tplusone = 2



# # Function: returns_for_young
# # Calculate a return for a specific effort split of the maximizing scientist of interest in time period t
# # Return: a return for that scientist in time period t
# def returns_for_young(effort_on_tminusone, effort_on_t):
# 	pass

# # Function: returns_for_old
# # Calculate the returns for specific effort split of the maximizing scientist of interest in time period t+1
# # Return: a return for that scientist in time period t+1
# def returns_for_old(effort_on_tminusone, effort_on_t, effort_on_tplusone):
# 	pass

# # Function: total_returns
# # Takes all possible pairs pairs of the returns between the young and old version of the scientists of interest 
# # and calculates the maximum total return given the young and old returns
# # Return: pair of returns that produce the maximum return over both time period t and t+1
# def total_returns(young_returns_options, old_returns_options):
# 	pass

def return_for_old_young_pair(young_split_constant, old_split_constant, dict_of_pairs):
	max_return_young_old_pair = None
	max_return = 0

	all_young_old_splits = []
	for young_split in dict_of_pairs.keys():
		all_old_splits = dict_of_pairs[young_split]
		for old_split in all_old_splits:
			all_young_old_splits.append((young_split, old_split))

	for young_old_pair in all_young_old_splits:
		# find return for young
		young_split = young_old_pair[0]

		young_return = calculate_young_returns(young_split, young_split_constant, old_split_constant)
		# find return for old
		old_split = young_old_pair[1]

		old_return = calculate_old_returns(old_split, young_split, young_split_constant, old_split_constant)

		print "Old Pair:"
		print max_return_young_old_pair
		print max_return
		if young_return + old_return > max_return:
			print "Pair Return is greater:"
			print young_old_pair
			print young_return + old_return

			max_return_young_old_pair = young_old_pair
			max_return = young_return + old_return
		else:
			print "Pair Return NOT greater:"
			print young_old_pair
			print young_return + old_return

	return max_return_young_old_pair, max_return



def calculate_old_returns(old_split, young_split, young_split_constant, old_split_constant):
	idea_tminusone_effort = old_split[TimePeriod.tminusone]
	idea_t_effort = old_split[TimePeriod.t]
	idea_tplusone_effort = old_split[TimePeriod.tplusone]

	prev_effort_on_idea_t = young_split[TimePeriod.t] + old_split_constant[TimePeriod.tplusone]
	prev_effort_on_idea_tminusone = old_split_constant[TimePeriod.tplusone] + young_split_constant[TimePeriod.t] \
										+ old_split_constant[TimePeriod.t] + young_split[TimePeriod.tminusone]
	prev_effort_on_idea_tplusone = 0

	if pes.has_n_zero_elems(old_split, 0):
		old_return = dummy_func(prev_effort_on_idea_tminusone + idea_tminusone_effort) \
						- dummy_func(prev_effort_on_idea_tminusone) \
						+ dummy_func(prev_effort_on_idea_t + idea_t_effort + young_split_constant[0]) \
						- dummy_func(prev_effort_on_idea_t) \
						+ dummy_func(prev_effort_on_idea_tplusone + idea_tplusone_effort + young_split_constant[1]) \
						- dummy_func(prev_effort_on_idea_tplusone)
	elif pes.has_n_zero_elems(old_split, 1):
		if old_split[TimePeriod.tminusone] == 0:
			old_return = dummy_func(prev_effort_on_idea_t + idea_t_effort + young_split_constant[0]) \
						- dummy_func(prev_effort_on_idea_t) \
						+ dummy_func(prev_effort_on_idea_tplusone + idea_tplusone_effort + young_split_constant[1]) \
						- dummy_func(prev_effort_on_idea_tplusone)
		if old_split[TimePeriod.t] == 0:
			old_return = dummy_func(prev_effort_on_idea_tminusone + idea_tminusone_effort) \
						- dummy_func(prev_effort_on_idea_tminusone) \
						+ dummy_func(prev_effort_on_idea_tplusone + idea_tplusone_effort + young_split_constant[1]) \
						- dummy_func(prev_effort_on_idea_tplusone)
		if old_split[TimePeriod.tplusone] == 0:
			old_return = dummy_func(prev_effort_on_idea_tminusone + idea_tminusone_effort) \
						- dummy_func(prev_effort_on_idea_tminusone) \
						+ dummy_func(prev_effort_on_idea_t + idea_t_effort + young_split_constant[0]) \
						- dummy_func(prev_effort_on_idea_t) 
	elif pes.has_n_zero_elems(old_split, 2):
		if old_split[0] == 0 and old_split[1] == 0:
			old_return = dummy_func(prev_effort_on_idea_tplusone + idea_tplusone_effort + young_split_constant[1]) \
						- dummy_func(prev_effort_on_idea_tplusone)
		if old_split[0] == 0 and old_split[2] == 0:
			old_return = dummy_func(prev_effort_on_idea_t + idea_t_effort + young_split_constant[0]) \
						- dummy_func(prev_effort_on_idea_t) 
		if old_split[1] == 0 and old_split[2] == 0:
			print "prev_effort_on_idea_tminusone:"
			print prev_effort_on_idea_tminusone

			print "idea_tminusone_effort:"
			print idea_tminusone_effort

			print ' '
			old_return = dummy_func(prev_effort_on_idea_tminusone + idea_tminusone_effort) \
						- dummy_func(prev_effort_on_idea_tminusone)

	return old_return


def calculate_young_returns(young_split, young_split_constant, old_split_constant):
	idea_tminusone_effort = young_split[TimePeriod.tminusone]
	idea_t_effort = young_split[TimePeriod.t]

	prev_effort_on_idea_t = 0 
	prev_effort_on_idea_tminusone = young_split_constant[1] + old_split_constant[2]

	if young_split[0] == 0:
		young_return = dummy_func(idea_t_effort+prev_effort_on_idea_t+old_split_constant[2]) \
								 - dummy_func(prev_effort_on_idea_t)
	elif young_split[1] == 0:
		young_return = dummy_func(idea_tminusone_effort+prev_effort_on_idea_tminusone+old_split_constant[1]) \
								 - dummy_func(prev_effort_on_idea_tminusone)
	else:
		young_return = dummy_func(idea_tminusone_effort+prev_effort_on_idea_tminusone+old_split_constant[1]) \
								 - dummy_func(prev_effort_on_idea_tminusone)\
								 + dummy_func(idea_t_effort+prev_effort_on_idea_t+old_split_constant[2]) \
								 - dummy_func(prev_effort_on_idea_t)

	return young_return

def build_effort_pair_dict(young_splits):
	dict_of_pairs = {}
	for young_split in young_splits:
		dict_of_pairs[young_split] = pes.main(0.1, 1.0, 0.1, 1, young_split[TimePeriod.tminusone], young_split[TimePeriod.t])
	return(dict_of_pairs)

def print_dict(dict_to_print):
	for item in dict_to_print.items():
		print(item)

def dummy_func(x):
	return x**2

def main():

	# create ideas to keep track of effort spent on each
	idea_tminusone = Idea(TimePeriod.tminusone)
	idea_t = Idea(TimePeriod.t)
	idea_tplusone = Idea(TimePeriod.tplusone)

	scientist_young = Scientist("young") # in time t
	scientist_old = Scientist("old") # in time t+1


	# Set these for now
	young_effort_constant = [0.4, 0.4]
	old_effort_constant = [0.3, 0.3, 0.3]

	# set this for now: build function for this later
	young_splits = [(0.4, 0.4), (0, 0.9), (0.9, 0), (0.3, 0.5), \
									(0.5, 0.3), (0.1, 0.7), (0.7, 0.1), \
									(0.6, 0.3), (0.3, 0.6)]

	possible_young_old_effort_pairs = build_effort_pair_dict(young_splits)	


	max_return_old_young_pair, max_return = return_for_old_young_pair(young_effort_constant, old_effort_constant, possible_young_old_effort_pairs)

	print max_return_old_young_pair
	print max_return



	




if __name__ == "__main__":
    main()
