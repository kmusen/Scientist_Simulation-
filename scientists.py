"""
Toy model with scientists
"""

import simpy 
import random
env = simpy.Environment()


class Scientist(object):

	def __init__(self, birthyear, env):
		self.env = env
		self.birthyear = int(birthyear)
		self.age = "young"
		self.process = env.process(self.study())

	def __str__(self):
		s = "scientist" + str(self.birthyear)
		return s

	def get_old(self):
		self.age = "old"
	
	def die(self):
		self.age = "dead"

	def is_dead(self):
		if self.age == "dead":
			return True
		else:
			return False

	def get_age(self):
		return self.age

	def get_birthyear(self):
		return self.birthyear
	
	
	def study(self):
		while True:

			options = [0, .25, .5, .75, 1]
			x = random.choice(options)
			print "Scientist uses " + str(x) + " units of effort"
			t = 1
			yield env.timeout(t)
				
class Idea(object):
	
	def __init__(self, year_created):
		self.year_created = int(year_created)
		
		self.contributors = []

		self.total_effort = 0.0

	def __str__(self):
		s = "idea" +str(self.year_created)
		return s
	
	def add_contributor(scientist, amount):

		self.contributors.append(scientist)
		
		sef.total_effort += float(amount)
		

def lifecycle(env):

	researchers = []
	counter = -1
	researchers.append((Scientist(1, env)))
	time = 1
	yield env.timeout(time)

	num_researchers = 1

	while True:
		counter += 2
		researchers.append(Scientists((counter+1), env))
		researchers[int(counter)].get_old()
		if len(researchers) > 2:
			researchers[counter-1].dies()
		duration = 1
		print rsearchers
		yield env.timeout(duration)



env.process(lifecycle(env))

env.run(until = 10)
		
	
	

	

