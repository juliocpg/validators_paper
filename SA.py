import time
import random
import numpy as np
from Graphs import Graph
from objFun import socialWelfare

class SA:
    def __init__(self,p, graph, initial_temperature, cooling_rate,alpha):
        self.graph = graph
        self.initial_temperature = initial_temperature
        self.cooling_rate = cooling_rate
        self.alpha = alpha
        self.p = p

    def run(self, iterations):
        start_time = time.time()

        current_solution = random.sample(range(self.graph.num_servers),self.p)
        current_solution_cost = self.evaluate_solution(current_solution)

        best_solution = current_solution
        best_solution_cost = current_solution_cost

        temperature = self.initial_temperature

        for _ in range(iterations):
            new_solution = self.neighbor_solution(current_solution)
            new_solution_cost = self.evaluate_solution(new_solution)

            if new_solution_cost < current_solution_cost or \
                    random.random() < np.exp((current_solution_cost - new_solution_cost) / temperature):
                current_solution = new_solution
                current_solution_cost = new_solution_cost

            if new_solution_cost < best_solution_cost:
                best_solution = new_solution
                best_solution_cost = new_solution_cost

            temperature *= self.cooling_rate

        convergence_time = time.time() - start_time
        return np.array(best_solution), best_solution_cost, convergence_time/iterations

    def neighbor_solution(self, solution):
        
        n = int(0.2 * self.p) 
        # Generate a neighbor solution by making a small modification
        new_solution = solution[:]

        available_numbers = list(set(range(self.graph.num_servers)) - set(solution))
        indexes = random.sample(range(self.p), n)

        for i in range(n):
            new_solution[indexes[i]] = available_numbers[i]

        return new_solution

    def evaluate_solution(self, solution):
        solution_cost = socialWelfare(self.graph,solution,alpha=self.alpha)  # Penalty cost
        return solution_cost

