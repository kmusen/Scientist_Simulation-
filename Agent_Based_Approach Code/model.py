from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
import numpy as np

# Sigmoid function
def logistic_cdf(x, loc, scale):
    return 1/(1+np.exp((loc-x)/scale))

class Scientist(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        # Scalar: amount of effort a scientist is born with (M)
        self.start_effort = np.random.poisson(lam=100)

        # Scalar: rate of decay for starting_effort (lambda_e)
        self.start_effort_decay = 10

        # Scalar: amount of effort a scientist has left
        self.avail_effort = self.start_effort.copy() 
        
        # Investment cost for each idea for the scientist
        self.k = np.random.poisson(lam=30, size=model.total_ideas)
        
        # Parameters determining perceived returns for ideas
        self.sds = np.random.random_sample(model.total_ideas)
        self.means = np.random.random_sample(model.total_ideas)
        
        # Records when the scientist was born
        self.birth_time = model.schedule.time
        
        # Array keeping track of how much effort this scientist has invested in each idea
        self.effort_invested = np.zeros(model.total_ideas)
        
    def step(self):
        # Determine how much effort the scientist has in current time period
        self.curr_start_effort = self.start_effort - self.start_effort_decay*model.schedule.time
        print(self.unique_id)
        print(self.curr_start_effort)
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