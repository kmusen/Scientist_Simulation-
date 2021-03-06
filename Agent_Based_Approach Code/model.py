from mesa import Agent, Model
from mesa.time import BaseScheduler
from mesa.datacollection import DataCollector
import random
import numpy as np
from numpy.random import poisson, logistic

# Sigmoid function
def logistic_cdf(x, loc, scale):
    return 1/(1+np.exp((loc-x)/scale))

#Sigmoid function starting at x = 0, scale, shape > 0, x >= 0
def gompertz_cdf(x, shape, scale):
    return 1-np.exp(-shape*(np.exp(scale*x)-1))

def create_return_graph(num_ideas, max_of_max_inv, sds, means):
    x = np.arange(max_of_max_inv+1)
    returns_list = []
    for i in range(num_ideas):
        returns = logistic.cdf(x,loc = means[i], scale = sds[i])
        to_subt_temp = np.hstack((0,returns[:-1]))
        # calculates return per unit of effort
        returns = returns - to_subt_temp
        returns_list.append(returns)
    return(np.array(returns_list))

class Scientist(Agent):
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        
        # Scalar: amount of effort a scientist is born with (M)
        self.start_effort = poisson(lam=10)

        # Scalar: rate of decay for starting_effort (lambda_e)
        self.start_effort_decay = 1

        # Scalar: amount of effort a scientist has left
        self.avail_effort = self.start_effort.copy() 
        
        # Investment cost for each idea for the scientist
        self.k = poisson(lam=2, size=model.total_ideas)
        
        # Parameters determining perceived returns for ideas
        self.sds = poisson(4, model.total_ideas)
        self.means = poisson(50, model.total_ideas)
        
        # Create the ideas/returns matrix
        self.returns_matrix = \
            create_return_matrix(model.total_ideas, max(model.max_investment), sds, means)
        
        # Records when the scientist was born
        self.birth_time = model.schedule.time
        
        # Array keeping track of how much effort this scientist has invested in each idea
        self.effort_invested = np.zeros(model.total_ideas)
        
    def step(self):
        print(self.returns_matrix)
#        # Determine how much effort the scientist has in current time period
#        self.curr_start_effort = self.start_effort - self.start_effort_decay*model.schedule.time
#        print(self.unique_id)
#        print(self.curr_start_effort)
#        if self.wealth == 0:
#            return
#        other_agent = random.choice(self.model.schedule.agents)
#        other_agent.wealth += 1
#        self.wealth -= 1

class ScientistModel(Model):
    def __init__(self, N, ideas_per_time, time_periods):
        self.num_scientists = N
        
        self.total_ideas = ideas_per_time*time_periods
        
        # Store the max investment allowed in any idea
        self.max_investment = poisson(lam=50, size=self.total_ideas)
        
        # Store parameters for true idea return distribution
        self.true_sds = poisson(4, size=self.total_ideas)
        self.true_means = poisson(50, size=self.total_ideas)

        # Create array to keep track of total effort allocated to each idea
        self.total_effort = np.zeros(self.total_ideas)
        
        self.schedule = BaseScheduler(self)
        for i in range(self.num_scientists):
            a = Scientist(i, self)
            self.schedule.add(a)
            
    def step(self):
        self.schedule.step()