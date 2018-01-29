import random

class Solver_8_queens:
	def __init__(self, pop_size = 150, cross_prob = 0.75, mut_prob = 0.5):
		print("hello")
		self.pop_size = pop_size
		self.cross_prob = cross_prob
		self.mut_prob = mut_prob

	def solve(self):
		best_fit = 0.9
		epoch_num = 100
		visualization = "..x...."
		return best_fit, epoch_num, visualization





class Individ:
	def __init__(self, genome):
		if genome != none:
			self.genome = genome
		else:
			self.genome = ''
			for i in range(8):
				gene = '{:03b}'.format(random.randint(0,7))
				self.genome += gene
		#self.__calculate_fitness()
		

	def get_fitness(self):
		fit = 1



