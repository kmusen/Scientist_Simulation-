from mesa.time import BaseScheduler
from mesa import Agent, Model
import random
import numpy as np
from scipy.stats import norm
import pprint

class Scientist(Agent):
    def __init__(self, curr_time, scientists_per_cycle, ideas_per_cycle, total_scientists, \
                            total_ideas, granularity, current_idea_effort, max_idea_effort, \
                            true_means_mean, true_means_std_dev, true_std_devs_mean, true_std_devs_std_dev, \
                            starting_effort_mean, starting_effort_std_dev, k_mean, k_std_dev, model):

        #super().__init__(unique_id, model)

        self.ideas_per_cycle = ideas_per_cycle
        
        # Scalar: what time period this Scientist was born
        self.time_born = curr_time
        
        # Array: keeps track of effort this scientist has spent on each idea
        self.self_invested_effort = np.zeros(total_ideas)
        
        # Scalar: number of total ideas created throughout the simulation
        self.total_ideas = total_ideas
        
        # Array keeping track of how much effort has collectively been spent on each idea
        self.current_idea_effort = current_idea_effort
        
        # Array keeping track of the maximum effort allowed on each idea
        self.max_idea_effort = max_idea_effort



        ###### Variables that are distorted for each scientist ######

        # Scalar: total effort a scientist gets per time period
        self.total_self_effort = np.random.normal(starting_effort_mean, starting_effort_std_dev)

        # Scalar: remaining effort a Scientist has left
        self.self_effort_left = self.total_self_effort
        
        # Array keeping track of the k for each idea
        self.k = np.random.normal(k_mean, k_std_dev, total_ideas)
        
        # Array keeping track of the mean of the return curve for each idea
        self.means = np.random.normal(true_means_mean, true_means_std_dev, total_ideas)
        
        # Array keeping track of the standard deviations of the return curve for each idea
        self.std_devs = np.random.normal(true_std_devs_mean, true_std_devs_std_dev, total_ideas)

    
    def step(self):
        # Prints out each of the scientist attributes before the step starts
        print(' ')
        print("SCIENTIST BEFORE")
        print(' ')
        pprint.pprint(self.__dict__, width=1)
        
        # Pick ideas scientist can work on according to three criteria:
        # 1. the scientist has enough effort left to cover the entry cost "k"
        # 2. the idea has not reached the maximum effort allowed on it
        # 3. the idea was created either in this time period, or the previous time periods (NEED TO CHANGE)
        avail = np.nonzero((self.k < self.self_effort_left) & (self.current_idea_effort < self.max_idea_effort))[0]
        
        # Make sure criteria 3 is fulfilled
        idea_time_period = avail//self.ideas_per_cycle
        #crit_3_indices = np.nonzero((idea_time_period == self.time_born) | (idea_time_period == self.time_born - 1))[0]
        crit_3_indices = np.nonzero(idea_time_period <= self.time_born)[0]
        avail = avail[crit_3_indices]
        
        # Return if the Scientist can't work on any ideas
        if len(avail) == 0:
            return
        
        avail_idea_effort = self.current_idea_effort[avail]
        avail_means = self.means[avail]
        avail_std_devs = self.std_devs[avail]
        
        # Pick which idea to work on based on highest return
        current_returns = norm.cdf(avail_idea_effort, avail_means, avail_std_devs)
#         unit_to_invest = 1
        potential_returns = norm.cdf(avail_idea_effort + self.self_effort_left - self.k[avail], avail_means, avail_std_devs)
        
        # Returns index for which idea to invest in
        idea_to_invest_in = np.argmax(potential_returns - current_returns)
                
        # Pay the entrance cost to work on the idea "k"
        self.self_effort_left -= self.k[avail[idea_to_invest_in]]
                
        # Invest in idea with highest potential return (Note: pass by value)
        self.current_idea_effort[avail[idea_to_invest_in]] += self.self_effort_left
        self.self_invested_effort[avail[idea_to_invest_in]] += self.self_effort_left

        #Reset amount of effort for next time period
        self.self_effort_left = self.total_self_effort

        # Prints out each of the scientist attributes after the step has been completed
        print(' ')
        print("SCIENTIST AFTER")
        print(' ')
        pprint.pprint(self.__dict__, width=1)


class ScientistModel(Model):
    def __init__(self, scientists_per_cycle, ideas_per_cycle, cycles, granularity, max_idea_effort, \
                    true_means_mean, true_means_std_dev, true_std_devs_mean, true_std_devs_std_dev, \
                    starting_effort_mean, starting_effort_std_dev, k_mean, k_std_dev):

        self.schedule = BaseScheduler(self) # has a .time() function

        # Constant variables
        self.scientists_per_cycle = scientists_per_cycle
        self.ideas_per_cycle = ideas_per_cycle
        self.total_scientists = scientists_per_cycle * cycles
        self.total_ideas = ideas_per_cycle * cycles
        self.granularity = granularity
        self.current_idea_effort = np.zeros(self.total_ideas)
        self.max_idea_effort = max_idea_effort

        # Varied variables
        self.true_means_mean = true_means_mean
        self.true_means_std_dev = true_means_std_dev
        self.true_std_devs_mean = true_std_devs_mean
        self.true_std_devs_std_dev = true_std_devs_std_dev 
        self.starting_effort_mean = starting_effort_mean
        self.starting_effort_std_dev = starting_effort_std_dev
        self.k_mean = k_mean
        self.k_std_dev = k_std_dev

    def step(self):
        for i in range(self.scientists_per_cycle):
            a = Scientist(self.schedule.time, self.scientists_per_cycle, self.ideas_per_cycle, self.total_scientists, \
                            self.total_ideas, self.granularity, self.current_idea_effort, self.max_idea_effort, \
                            self.true_means_mean, self.true_means_std_dev, self.true_std_devs_mean, self.true_std_devs_std_dev, \
                            self.starting_effort_mean, self.starting_effort_std_dev, self.k_mean, self.k_std_dev, self)
            self.schedule.add(a)
        self.schedule.step()