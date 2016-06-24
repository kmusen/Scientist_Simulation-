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
	
	def dies(self):
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

			options = [0.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0]


			if self.age == "dead":

				print "Scientist " +str(self.birthyear) + " is dead"

			elif self.birthyear ==0 and self.age == "young":
				current = 1
				print "\nIn time 0:\n"
				print "Scientist 0 exerts 1 unit of effort on Idea 0"

				ideas_list[0].add_effort(1)
 
			elif self.birthyear == 0 and self.age == "old":
				past = random.choice(options)
				current = 1.0- past
				print "Scientist 0 exerts " + str(past) + " units of effort on idea 0 and " + str(current) + " units of effort on idea 1"

				ideas_list[self.birthyear].add_effort(past)
				ideas_list[self.birthyear+1].add_effort(current)

			elif self.age == "young":
				current = random.choice(options)
				grandfather = 1 - current
				print "\nIn time " +str(self.birthyear) + ":\n"
				print "Scienitst " +str(self.birthyear) + " exerts " + str(grandfather) + " units of effort on idea " + str(self.birthyear-1) + " and " + str(current) + " units of effort on idea " + str(self.birthyear)

				ideas_list[self.birthyear-1].add_effort(grandfather)
				ideas_list[self.birthyear].add_effort(current)

			else:

				current =random.choice(options)

				remaining = 1.0 - current 

				iterations = int(remaining / .1)

				if current == 1.0:
					grandfather =0.0
					past = 0.0

				else:

					if current ==.9:
						options2 = [0.0, .1]
					else:
						options2 = [0.0]
						for i in range(1, (iterations+1)):
							options2.append((.1*i))
				
					grandfather = random.choice(options2)
					if int(current+grandfather) == 1:
						past =0.0
					else:
						past = remaining - grandfather

				ideas_list[self.birthyear-1].add_effort(grandfather)
				ideas_list[self.birthyear].add_effort(past)
				ideas_list[self.birthyear+1].add_effort(current)
				
				print "Scientist " + str(self.birthyear) + " uses " + str(current) + " units of effort on idea " +str(self.birthyear+1) + ", " + str(past) + " units of effort on idea " + str(self.birthyear) + ", and " +str(grandfather) + " units of effort on idea " +str(self.birthyear-1)
			
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
	
	def add_effort(self, amount):
		
		self.total_effort += float(amount)

	def get_effort(self):

		return self.total_effort
		

def lifecycle(env):

	researchers = []
	counter = 0
	researchers.append((Scientist(0, env)))
	time = 1
	yield env.timeout(time)

	num_researchers = 1

	while True:
		counter += 1
		researchers.append(Scientist((counter), env))
		researchers[int(counter-1)].get_old()
		if len(researchers) > 2:
			researchers[counter-2].dies()
		duration = 1
		#for researcher in researchers:
			#print researcher

		yield env.timeout(duration)


def main():

	cycles = int(raw_input("How many generations of scientists do you want?"))

	global ideas_list

	ideas_list = []

	for i in range(cycles):
		ideas_list.append(Idea(i))

	env.process(lifecycle(env))

	env.run(until = cycles)

	total_effort_all_ideas =0

	for i in range(cycles):

		print str(ideas_list[i].get_effort()) + " units total effort on idea " + str(i)

		total_effort_all_ideas += ideas_list[i].get_effort()

	print str(total_effort_all_ideas) + " units effort on all ideas combined"


main()

		
	
	

	

