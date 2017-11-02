from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
import numpy as np

class Scientist(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.wealth = 1
    def step(self):
        print(self.unique_id)
#        if self.wealth == 0:
#            return
#        other_agent = random.choice(self.model.schedule.agents)
#        other_agent.wealth += 1
#        self.wealth -= 1
class ScientistModel(Model):
    def __init__(self, N, ideas_per_time, time_periods):
        self.num_scientists = N
        self.total_ideas = ideas_per_time*time_periods
        
        # Store parameters for true idea return distribution
        self.true_sds = np.random.random_sample(self.total_ideas)
        self.true_means = np.random.random_sample(self.total_ideas)

        # Create array to keep track of total effort allocated to each idea
        self.total_effort = np.zeros(self.total_ideas)
        
        self.schedule = BaseScheduler(self)
        for i in range(self.num_scientists):
            a = Scientist(i, self)
            self.schedule.add(a)
    def step(self):
        self.schedule.step()