from classes import *
import matplotlib.pyplot as plt

# SAMPLE RUN
cycles = 10
ideas_per_cycle = 2
scientists_per_cycle = 2
granularity = 1
total_ideas = cycles * ideas_per_cycle

# Define distribution of standard deviations of return curves
true_means_mean = 50 * np.ones(total_ideas)
true_means_std_dev = 5 * np.ones(total_ideas)

# Define distribution of standard deviations of return curves
true_std_devs_mean = 1.2 * np.ones(total_ideas)
true_std_devs_std_dev = 0.2 * np.ones(total_ideas)

# Define distribution of starting effort (randomness built into class)
starting_effort_mean = 10
starting_effort_std_dev = 1

# Define distribution of k's for each scientists for each idea
k_mean = 1
k_std_dev = 0.3


max_idea_effort = 100 * np.ones(total_ideas)
model = ScientistModel(scientists_per_cycle, ideas_per_cycle, cycles, granularity, max_idea_effort, \
                    	true_means_mean, true_means_std_dev, true_std_devs_mean, true_std_devs_std_dev, \
                    	starting_effort_mean, starting_effort_std_dev, k_mean, k_std_dev)
for i in range(cycles):
    print(' ')
    print("CYCLE ", i)
    print(' ')
    model.step()


##### PLOTTING #####
idea_returns = random.choice(model.schedule.agents).current_idea_effort
objects = range(len(idea_returns))
y_pos = np.arange(len(objects))
plt.bar(y_pos, idea_returns, align='center', alpha = 0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Total Effort')
plt.title('Total Effort invested in each Idea across all Scientists')
plt.xlabel('Idea Number')
plt.show()