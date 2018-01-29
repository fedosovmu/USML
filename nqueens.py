import random

import copy


class Solver_8_queens:
    def __init__(self, pop_size=150, cross_prob=0.75, mut_prob=0.05):
        random.seed()
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def solve(self, min_fitness=1, max_epochs=200):
        best_fit = 0
        epoch_num = 0
        visualization = ''

        # initialization
        self.population = []
        for i in range(self.pop_size):
            individ = Individ()
            self.population.append(individ)

        # evolution
        while best_fit < min_fitness and epoch_num < max_epochs:
            epoch_num += 1
            self.next_generation()
            individ = self.find_best_individ()

            best_fit = individ.get_fitness()
            visualization = individ.get_visualisation()
            genome = individ.get_queens_positions()
            print ('epoch:', epoch_num, 'fit:', best_fit, 'genome:', genome, 'size:', len(self.population))

        return best_fit, epoch_num, visualization

    def next_generation(self):
        self.roullete_selection()
        for ind in self.population:
            if (random.random() > self.mut_prob):
                ind.mutation()

    def find_best_individ(self):
        best_fit = 0;
        for ind in self.population:
            fit = ind.get_fitness()
            if fit >= best_fit:
                best_fit = fit
                best_ind = ind
        return best_ind

    def roullete_selection(self):
        results_population = []
        fitnesses = []
        fit_sum = 0;
        for ind in self.population:
            fit = ind.get_fitness()
            fitnesses.append(fit)
            fit_sum += fit

        for num in range(len(self.population)):
            rand_pos = random.random() * fit_sum
            s = 0
            for fit in fitnesses:
                s += fit
                if s > rand_pos:
                    results_population.append(self.population[num])
                    break

        self.population.clear()
        self.population = copy.copy(results_population)

class Individ:
    def __init__(self):
        self.set_random_genome()

    def set_random_genome(self):
        self.genome = ''
        for i in range(8):
            gene = '{:03b}'.format(random.randint(0, 7))
            self.genome += gene

    def get_fitness(self):
        queens = self.get_queens_positions()
        collisions = 0
        fit = ''
        for a in range(8):
            for b in range(a + 1, 8):
                if queens[a] == queens[b]:
                    collisions += 1
                if abs(queens[a] - queens[b]) == abs(a - b):
                    collisions += 1

        fitness = pow(0.7, collisions)
        return fitness

    def get_queens_positions(self):
        queen_positions = []
        for i in range(8):
            gene = self.genome[i * 3 : i * 3 + 3]
            queen_positions.append(int(gene, 2))
        return queen_positions

    def queen_pos_to_line(self, queen_pos):
        line = ''
        for i in range(8):
            if i == queen_pos:
                line += 'Q '
            else:
                line += '+ '
        return line

    def get_visualisation(self):
        queen_positions = self.get_queens_positions()
        visualisation = '\n'.join(self.queen_pos_to_line(q) for q in queen_positions)
        return visualisation

    def mutation(self):
        genome = list(self.genome)
        bit_num = random.randint(0, len(genome) - 1)
        if genome[bit_num] == '0':
            genome[bit_num] = '1'
        else:
            genome[bit_num] = '0'

        self.genome = ''.join(genome)