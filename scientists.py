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

			options = [0.0, .1, .2, .3, .4, .5, .6, .7, .8, .9, 1.0] #creates options for effort for first project


			if self.age == "dead": #so that we know which scientists are no longer doing research

				print "Scientist " +str(self.birthyear) + " is dead" 

			elif self.birthyear ==0 and self.age == "young": #Scientist 0 in year 0 can only work on idea 0
				current = 1
				print "\nIn time 0:\n"
				print "Scientist 0 exerts 1 unit of effort on Idea 0"

				ideas_list[0].add_effort(1)
 
			elif self.birthyear == 0 and self.age == "old": #Scientist 0 in year 1 only has 2 options instead of 3 like other old scientists
				past = random.choice(options)
				current = 1.0- past
				print "Scientist 0 exerts " + str(past) + " units of effort on idea 0 and " + str(current) + " units of effort on idea 1"

				ideas_list[self.birthyear].add_effort(past)
				ideas_list[self.birthyear+1].add_effort(current)

			elif self.age == "young": #randomly splits 1 unit of effort between two options given to young scientists
				current = random.choice(options)
				grandfather = 1 - current
				print "\nIn time " +str(self.birthyear) + ":\n"
				print "Scienitst " +str(self.birthyear) + " exerts " + str(grandfather) + " units of effort on idea " + str(self.birthyear-1) + " and " + str(current) + " units of effort on idea " + str(self.birthyear)

				ideas_list[self.birthyear-1].add_effort(grandfather)
				ideas_list[self.birthyear].add_effort(current)

			else: #randomly splits effort between three options given to old scientists 

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
	
	def add_effort(self, amount): #method to add effort into an idea
		
		self.total_effort += float(amount)

	def get_effort(self): #method to find out how much effort has been put into an idea

		return self.total_effort
		

def lifecycle(env): #creates, ages, and kills scientists 

	researchers = []
	counter = 0
	researchers.append((Scientist(0, env)))
	time = 1
	yield env.timeout(time)

	#num_researchers = 1 #we start with one scientists in year 0

	while True:
		counter += 1
		researchers.append(Scientist((counter), env)) #adds scientists
		researchers[int(counter-1)].get_old() #ages scientists 
		if len(researchers) > 2:
			researchers[counter-2].dies() #kills scientists 
		duration = 1
		#for researcher in researchers:
			#print researcher

		yield env.timeout(duration)


def main():

	cycles = int(raw_input("How many generations of scientists do you want?"))

	global ideas_list #allows access to this list within the classes 

	ideas_list = []

	for i in range(cycles): #creates the number of ideas specified by the number of cycles the user wants 
		ideas_list.append(Idea(i))

	env.process(lifecycle(env))

	env.run(until = cycles) #runs simulation

	total_effort_all_ideas =0

	for i in range(cycles):

		print str(ideas_list[i].get_effort()) + " units total effort on idea " + str(i)

		total_effort_all_ideas += ideas_list[i].get_effort() #adds up total effort into all ideas, serves as a check for bugs

	print str(total_effort_all_ideas) + " units effort on all ideas combined"


main()

		
	
	

	

