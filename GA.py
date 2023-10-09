import time
import random
import numpy as np
from Graphs import Graph
from objFun import socialWelfare

class GA:
    def __init__(self,p, graph, population_size, mutation_rate, crossover_rate, elitism_rate,alpha):
        self.graph = graph
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.elitism_rate = elitism_rate
        self.p = p
        self.alpha = alpha

    def run(self, iterations):
        start_time = time.time()

        population = self.generate_initial_population()

        best_solution = None
        best_solution_cost = float('inf')

        for _ in range(iterations):
            population = self.evolve_population(population)
            
            best_individual = min(population, key=lambda ind: self.evaluate_solution(ind))
            if self.evaluate_solution(best_individual) < best_solution_cost:
                best_solution_cost = self.evaluate_solution(best_individual)
                best_solution = best_individual

        convergence_time = time.time() - start_time
        return np.array(best_solution), best_solution_cost, convergence_time/iterations

    def generate_initial_population(self):
        population = []
        for _ in range(self.population_size):
            individual = random.sample(range(self.graph.num_servers), self.p)
            population.append(individual)
        return population

    def evolve_population(self, population):
        new_population = []

        elitism_size = max(1, int(self.elitism_rate * self.population_size))
        elitism_pool = sorted(population, key=lambda ind: self.evaluate_solution(ind))[:elitism_size]
        new_population.extend(elitism_pool)

        while len(new_population) < self.population_size:
            if random.random() < self.crossover_rate and len(population)>2:
                parent1, parent2 = random.sample(population, k=2)
                offspring1, offspring2 = self.crossover(parent1, parent2)
                new_population.extend([offspring1, offspring2])
            if random.random() < self.mutation_rate:
                ind = random.choice(population)
                mutatedInd = self.mutate(ind)
                new_population.append(mutatedInd)
                

        return new_population

    def crossover(self,parent1, parent2):
        # Select a random crossover point
        crossover_point = random.randint(1, len(parent1) - 1)

        # Create the first child by combining the genes of parent1 and parent2
        child1 = parent1[:crossover_point] + parent2[crossover_point:]

        # Create the second child by combining the genes of parent2 and parent1
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        # Remove duplicate genes in the children
        child1 = list(set(child1))
        child2 = list(set(child2))

        # Fill in missing genes in the children
        missing_genes1 = list(set(parent1) - set(child1))
        missing_genes2 = list(set(parent2) - set(child2))
        
        for i in range(self.p - len(child1)):
            child1.append(missing_genes1[i])
        for i in range(self.p - len(child2)):
            child2.append(missing_genes2[i])
        
        return child1, child2


    def mutate(self, individual):
           
        # Generate a new number between 1 and n is not in the list
        available_numbers =[num for num in range(self.graph.num_servers) if num not in individual]
        if len(available_numbers) < 2:
            raise ValueError("Not enough numbers available in the range.")
        else:
            new_gens = random.sample(available_numbers,2)


        index1, index2 = random.sample(range(self.p), 2)
        individual[index1], individual[index2] = new_gens[0], new_gens[1]
        
        return individual

    def evaluate_solution(self, solution):
        solution_cost = socialWelfare(self.graph,solution,alpha=self.alpha)  # Penalty cost
        return solution_cost
