import numpy as np
import random
class Graph:
    def __init__(self, num_servers, num_users):
        self.num_servers = num_servers
        self.num_users = num_users
        self.adj_matrix = np.zeros((num_servers,num_servers + num_users))
        #self.capacity = np.zeros(num_servers)
        #self.demand = np.zeros(num_users)

    def add_edge(self, u, v, weight):
        self.adj_matrix[u,v] = weight
        self.adj_matrix[v,u] = weight

    def set_adjMatrix(self, adj_matrix):
        self.adj_matrix= adj_matrix.copy()
        
    '''
    def set_capacity(self, capacity):
        self.capacity = capacity

    def set_demand(self, demand):
        self.demand = demand
    '''
    def gen_randomGraph(self,Cost_min,Cost_max,d_min,d_max,c_min,c_max):
        
        #Radom demand
        self.set_demand([random.uniform(d_min,d_max) for _ in range(self.num_users)])

        #Random Capacity
        self.set_capacity([random.uniform(c_min,c_max) for _ in range(self.num_servers)])

        #Random Cost
        for i in range(self.num_servers):
            for j in range(self.num_servers + self.num_users):
                if(i == j):
                    self.add_edge(i,j,0)
                else:                    
                    self.adj_matrix[i,j] = random.uniform(Cost_min, Cost_max)

    def gen_randomGraph_Opt(self,Cost_min,Cost_max,p):
        '''
        Generate a random solution where the first p nodes conform a optimal solution
        '''        
        #Random Cost
        for i in range(self.num_servers):
            for j in range(self.num_servers + self.num_users):
                if(i == j):
                    self.add_edge(i,j,0)
                else:                    
                    self.adj_matrix[i,j] = random.uniform(Cost_min, Cost_max)
        

        for i in range(p):
            for j in range(self.num_servers + self.num_users):
                if(i != j):
                    self.adj_matrix[i,j] = Cost_min
    

    def sampleGraph(self, indexes):
        sample_size = len(indexes)        
        sample_adj_matrix = np.zeros((sample_size,sample_size + self.num_users))

        for i in range(len(indexes)):
            for j in range(len(indexes) + self.num_users):
                if(i == j):
                    sample_adj_matrix[i,j] = 0 
                else:          
                    sample_adj_matrix[i,j] = self.adj_matrix[indexes[i],j]
        X = Graph(sample_size, self.num_users)
        X.set_adjMatrix(sample_adj_matrix)
        return X



    def save_to_file(self,filename):
        # Save data to a text file
        with open(filename, 'w') as file:
            file.write(str(self.num_servers)+"\n")
            file.write(str(self.num_users) + "\n")
            file.write("Adjacency Matrix:\n")
            np.savetxt(file, self.adj_matrix)
            #file.write("Demands:\n")
            #np.savetxt(file, self.demand)
            #file.write("Capacities:\n")
            #np.savetxt(file, self.capacity)

    # Method to load data from the text file
    def load_from_file(self,filename):
        with open(filename, 'r') as file:
            self.num_servers = int(file.readline())
            self.num_users = int(file.readline())
            file.readline()  # Skip the line Adjacency Matrix:
            M =[]
            for i in range(self.num_servers):
                M.append(file.readline().strip().split())
            
            self.adj_matrix = np.array([[float(num) for num in sublist] for sublist in M])
            #print(self.adj_matrix)
            #file.readline()  # Skip the line "Demands:"
            #self.demand = np.array([float(num) for num in file.readline().strip().split()])
            #file.readline()  # Skip the line "Capacities:"
            #self.capacity = np.array([float(num) for num in file.readline().strip().split()])
        