import time
import random 
import numpy as np
from Graphs import Graph
from objFun import socialWelfare
import math

class ACO:
    def __init__(self, p,graph, num_ants, evaporation_rate, alpha_ant, beta, q0,alpha):
        self.graph = graph
        self.num_ants = num_ants
        self.evaporation_rate = evaporation_rate
        self.alpha_ant = alpha_ant
        self.beta = beta
        self.q0 = q0
        self.p = p
        self.alpha = alpha
        self.pheromone_matrix = [[1 / graph.num_servers] * graph.num_servers for _ in range(graph.num_servers+1)]

    def run(self, iterations):
        start_time = time.time()
        best_solution = None
        best_solution_cost = float('inf')

        for _ in range(iterations):
            solutions = []
            for _ in range(self.num_ants):
                solution = self.construct_solution()
                solutions.append(solution)

            for ant_solution in solutions:
                solution_cost = self.evaluate_solution(ant_solution)
                if solution_cost < best_solution_cost:
                    best_solution_cost = solution_cost
                    best_solution = ant_solution

                self.update_pheromone(ant_solution, solution_cost)

        convergence_time = time.time() - start_time
        return np.array(best_solution), best_solution_cost, convergence_time/iterations

    def construct_solution(self):
        
        init_vertice = random.randint(0,self.graph.num_servers-1)
        remaining_vertices = list(range(self.graph.num_servers))
   
        remaining_vertices.remove(init_vertice)  # Start with the first vertex in the list
        
        solution = [init_vertice]

        while len(solution) < self.p:
            next_vertex = self.choose_next_vertex(remaining_vertices, solution)
            solution.append(next_vertex)
            remaining_vertices.remove(next_vertex)

        return solution

    def choose_next_vertex(self, remaining_vertices, solution):
        probabilities = []
        last_vertex = solution[-1]
        
        for vertex in remaining_vertices:

            p_path = self.graph.adj_matrix[last_vertex][vertex]
            if(p_path > 0):
                probability = (self.pheromone_matrix[last_vertex][vertex] ** self.alpha_ant) * \
                            ((1/p_path) ** self.beta)
            else:
                probability = 0.000001
            
            if(not np.isnan(float(probability))):
                probabilities.append(probability)
                
            else:
                probabilities.append(0.000001)
                print("NAN")

        if random.random() < self.q0:
            max_probability = max(probabilities)
            max_probability_index = probabilities.index(max_probability)
            return list(remaining_vertices)[max_probability_index]
        else:
            total_probabilities = sum(probabilities)
            probabilities = [p / total_probabilities for p in probabilities]
            #print(probabilities)
            return np.random.choice(list(remaining_vertices),size=1,p=probabilities)[0]

    def evaluate_solution(self, solution):
        solution_cost = socialWelfare(self.graph,solution,alpha=self.alpha)  # Penalty cost
        return solution_cost

    def update_pheromone(self, solution, solution_cost):
        pheromone_deposit = 1 / solution_cost
        for i in range(len(solution) - 1):
            from_vertex = solution[i]
            to_vertex = solution[i + 1]
            self.pheromone_matrix[from_vertex][to_vertex] += pheromone_deposit
            self.pheromone_matrix[to_vertex][from_vertex] += pheromone_deposit

        self.pheromone_matrix = [[(1 - self.evaporation_rate) * pheromone + self.evaporation_rate / self.graph.num_servers
                                  for pheromone in row]
                                 for row in self.pheromone_matrix]