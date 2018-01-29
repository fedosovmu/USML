import copy

import random


class Solver_8_queens:
    def __init__(self, pop_size=150, cross_prob=0.75, mut_prob=0.5):
        self.pop_size = pop_size
        self.cross_prob = cross_prob
        self.mut_prob = mut_prob

    def solve(self, min_fitness=1, max_epohs=10000):
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
        self.genome = ''
        self.queens = []
        for i in range(8):
            gene = '{:03b}'.format(random.randint(0, 7))
            self.queens.append(gene)
            self.genome += gene
        self.__calculate_fitness()

    def get_queens_bin(self):
        queen_positions = []
        for i in range(8):
            gene = self.genome[i * 3: i * 3 + 3]
            queen_positions.append(gene)
        return queen_positions

    def __get_queens_pos(self):
        genes = self.get_queens_bin()
        queens = []
        for gene in genes:
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

    def queen_pos_to_string_line(self, queen_pos):
        line = ''
        for i in range(8):
            if i == queen_pos:
                line += 'Q '
            else:
                line += '+ '
        return line

    def get_visualisation(self):
        queen_positions = self.__get_queens_pos()
        visualisation = '\n'.join(self.queen_pos_to_string_line(q) for q in queen_positions)
        return visualisation


    def mutation(self):
        gene_num = random.randint(0, 7)
        queens = self.get_queens_bin()
        gene = list(queens[gene_num])
        bit_num = random.randint(0, 2)
        if gene[bit_num] == '1':
            gene[bit_num] = '0'
        else:
            gene[bit_num] = '1'
        queens[gene_num] = ''.join(gene)
        self.genome = ''.join(queens)
        self.__calculate_fitness()

    def crossing_over(self, spouse):
        bit_num = random.randint(1, 23)

        genome1 = copy.deepcopy(self.genome)
        genome2 = copy.deepcopy(spouse.genome)

        self.genome = genome1[:bit_num] + genome2[bit_num:]
        spouse.genome = genome2[:bit_num] + genome1[bit_num:]

        spouse.__calculate_fitness()
        self.__calculate_fitness()
