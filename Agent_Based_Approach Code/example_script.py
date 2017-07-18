from classes import *
import matplotlib.pyplot as plt

# SAMPLE RUN
cycles = 10
ideas_per_cycle = 2
scientists_per_cycle = 2
granularity = 1
total_ideas = cycles * ideas_per_cycle
true_means = 50 * np.ones(total_ideas)
true_std_devs = 1.2 * np.ones(total_ideas)
starting_effort = 10
max_idea_effort = 100 * np.ones(total_ideas)
model = ScientistModel(scientists_per_cycle, ideas_per_cycle, cycles, granularity, true_means, true_std_devs, starting_effort, max_idea_effort)
for i in range(cycles):
    print(' ')
    print("CYCLE ", i)
    print(' ')
    model.step()
# print('done')

idea_returns = random.choice(model.schedule.agents).current_idea_effort
print(idea_returns)
objects = range(len(idea_returns))
y_pos = np.arange(len(objects))
plt.bar(y_pos, idea_returns, align='center', alpha = 0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Total Effort')
plt.title('Total Effort invested in each Idea across all Scientists')
plt.xlabel('Idea Number')
plt.show()