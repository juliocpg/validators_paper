import time
import random
from Graphs import Graph
from ACO import ACO
from GA import GA
from SA import SA 
import numpy as np
from tools import generate_round_robin_sequences

class Solver:
    def __init__(self, p,graph,T):
        self.graph = graph
        self.p = p
        self.T = T
        
    def ACO_Sample(self,sample_size,iterations,alpha):
        ranking = np.zeros((self.graph.num_servers))
        subproblems = generate_round_robin_sequences(self.graph.num_servers, self.T)
                
        for subproblem in subproblems:
            #print(subproblem)
            indexes = subproblem
            subgraph = self.graph.sampleGraph(indexes)
            aco = ACO(p=self.p,graph=subgraph, num_ants=10, evaporation_rate=0.1, alpha_ant=1, beta=1, q0=0.9,alpha=alpha)
            best_solution_aco, best_solution_cost_aco, convergence_time_aco = aco.run(iterations=iterations)
            for node in best_solution_aco:
                ranking[indexes[node]] = ranking[indexes[node]] + 1

        
        indexes =  np.argsort(ranking)
        subgraph_best = self.graph.sampleGraph(indexes[-1*sample_size:])
        aco = ACO(p=self.p,graph=subgraph_best, num_ants=10, evaporation_rate=0.1, alpha_ant=1, beta=1, q0=0.9,alpha=alpha)
        best_solution_aco, best_solution_cost_aco, convergence_time_aco = aco.run(iterations=iterations)
        
        return np.array(best_solution_aco), best_solution_cost_aco, convergence_time_aco/self.graph.num_servers


    def GA_Sample(self,sample_size,iterations,alpha):
        ranking = np.zeros((self.graph.num_servers))
        subproblems = generate_round_robin_sequences(self.graph.num_servers, self.T)
        
        for subproblem in subproblems:
            #print(subproblem)
            indexes = subproblem
            subgraph = self.graph.sampleGraph(indexes)

            ga = GA(p=self.p,graph=subgraph, population_size=50, mutation_rate=0.1, crossover_rate=0.8, elitism_rate=0.1,alpha=alpha)
            best_solution_ga, best_solution_cost_ga, convergence_time_ga = ga.run(iterations=iterations)
            for node in best_solution_ga:
                ranking[indexes[node]] = ranking[indexes[node]] + 1

        indexes =  np.argsort(ranking)
        subgraph_best = self.graph.sampleGraph(indexes[-1*sample_size:])
        ga = GA(p=self.p,graph=subgraph_best, population_size=50, mutation_rate=0.1, crossover_rate=0.8, elitism_rate=0.1,alpha=alpha)
        best_solution_ga, best_solution_cost_ga, convergence_time_ga = ga.run(iterations=iterations)
        
        return np.array(best_solution_ga), best_solution_cost_ga, convergence_time_ga

    def SA_Sample(self,sample_size,iterations,alpha):

        ranking = np.zeros((self.graph.num_servers))
        subproblems = generate_round_robin_sequences(self.graph.num_servers, self.T)
        for subproblem in subproblems:
            #print(subproblem)
            indexes = subproblem
            subgraph = self.graph.sampleGraph(indexes)
            sa = SA(p=self.p,graph=subgraph, initial_temperature=100, cooling_rate=0.9,alpha=alpha)
            best_solution_sa, best_solution_cost_sa, convergence_time_sa = sa.run(iterations=iterations)
            for node in best_solution_sa:
                ranking[indexes[node]] = ranking[indexes[node]] + 1

        indexes =  np.argsort(ranking)
        subgraph_best = self.graph.sampleGraph(indexes[-1*sample_size:])
        sa = SA(p=self.p,graph=subgraph_best, initial_temperature=100, cooling_rate=0.9,alpha=alpha)
        best_solution_sa, best_solution_cost_sa, convergence_time_sa = sa.run(iterations=iterations)
        
        return np.array(best_solution_sa), best_solution_cost_sa, convergence_time_sa