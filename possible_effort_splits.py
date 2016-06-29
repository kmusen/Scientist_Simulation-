import itertools

# Function: all_possible_effort_splits
# Parameters: 
# num_of_effort_units - the number of effort units the total K efforts is split into (i.e. 10 means K/10 is one effort unit)
# number_of_ideas - number of ways we want to split the effort units
# Given a list, gives you all possible combinations of effort 
def all_possible_effort_splits(total_effort, num_of_effort_units, num_of_ideas, k):
	effort_unit = float(total_effort)/num_of_effort_units
	rng = list(range(num_of_effort_units+1))*num_of_ideas
	rng = [round(x * effort_unit,2) for x in rng]
	effort_splits = set(i for i in itertools.permutations(rng, num_of_ideas) if sum(i) == total_effort)
	return(effort_splits)

def main():
    print(all_possible_effort_splits(1, 4, 3, 0.25))
    print(all_possible_effort_splits(1, 4, 2, 0.25))

if __name__ == "__main__":
    main()