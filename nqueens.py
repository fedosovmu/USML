import copy

import random


class Solver_8_queens:
    def __init__(self, pop_size=150, cross_prob=0.75, mut_prob=0.5):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def solve(self, min_fitness=1, max_epohs=250):
        if self.pop_size == 0:
            return 0, 0, ""

        self.population = []
        for i in range(self.pop_size):
            individ = Individ()
            self.population.append(individ)

        best_fit = 0
        epoh_num = 0
        visualisation = ''

        while True:
            epoh_num += 1

            self.__next_generation()

            self.population.clear()
            self.population = copy.copy(self.next_population)
            self.next_population.clear()

            best_fit, visualisation = self.__find_max()

            if min_fitness != None:
                if best_fit >= min_fitness:
                    break
            if max_epohs != None:
                if epoh_num >= max_epohs:
                    break

        return best_fit, epoh_num, visualisation

    def __roulette_selection(self):
        prob = random.random()
        prob_sum = 0
        for individ in self.population:
            prob_sum += individ.fitness / self.fit_sum
            if prob_sum > prob:
                return individ

    def __next_generation(self):
        self.fit_sum = 0
        for individ in self.population:
            self.fit_sum += individ.fitness

        count = 0
        self.next_population = []
        while count < self.pop_size:
            individ = copy.deepcopy(self.__roulette_selection())
            self.next_population.append(individ)

            if random.random() <= self.cross_prob:
                spouse = copy.deepcopy(self.__roulette_selection())
                individ.crossing_over(spouse)

                if random.random() <= self.mut_prob:
                    spouse.mutation()

                self.next_population.append(spouse)
                count += 1

            if random.random() <= self.mut_prob:
                individ.mutation()

            self.next_population.append(individ)
            count += 1

    def __find_max(self):
        max_fitness = 0
        for individ in self.population:
            if individ.fitness > max_fitness:
                max_fitness = individ.fitness
                visualisation = individ.get_visualisation()
        return max_fitness, visualisation


class Individ:
    def __init__(self):
        self.genome = []
        for i in range(8):
            gene = '{:03b}'.format(random.randint(0, 7))
            self.genome.append(gene)
        self.__calculate_fitness()

    def __get_queens_pos(self):
        queens = []
        for gene in self.genome:
            pos = int(gene, 2)
            queens.append(pos)
        return queens

    def __calculate_fitness(self):
        queens = self.__get_queens_pos()
        penalty_score = 0

        for i in range(7):
            for j in range(7 - i):
                a = i
                b = j + i + 1
                if queens[a] == queens[b]:
                    penalty_score += 1
                if abs(queens[b] - queens[a]) == abs(b - a):
                    penalty_score += 1

        self.fitness = 1 / (1 + penalty_score)

    def get_visualisation(self):
        queens = self.__get_queens_pos()
        screen = []

        for i in range(8):
            line = []
            for j in range(8):
                line.append('+')
            pos = queens[i]
            line[pos] = 'Q'
            screen.append(''.join(line))

        visualisation = '\n'.join(screen)
        return visualisation

    def mutation(self):
        gene_num = random.randint(0, 7)
        gene = list(self.genome[gene_num])
        bit_num = random.randint(0, 2)
        if gene[bit_num] == '1':
            gene[bit_num] = '0'
        else:
            gene[bit_num] = '1'
        self.genome[gene_num] = ''.join(gene)
        self.__calculate_fitness()

    def crossing_over(self, spouse):
        point = random.randint(1, 7)
        for i in range(point):
            gene = copy.deepcopy(spouse.genome[i])
            spouse.genome[i] = copy.deepcopy(self.genome[i])
            self.genome[i] = gene

        spouse.__calculate_fitness()
        self.__calculate_fitness()
