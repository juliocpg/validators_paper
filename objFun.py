from Graphs import Graph
import numpy as np


def userUtilities(graph,x):
    Mat = graph.adj_matrix[x,:]
    
    column_max = np.max(Mat, axis=0)[graph.num_servers:]
    
    return column_max


def socialWelfare(graph,x,alpha):
    Aloc = []
    for j in range(graph.num_users):
            Cost = 0
            for i in range(len(x)):
                Cost = max(Cost,graph.adj_matrix[x[i],graph.num_servers + j])
            Aloc.append(Cost)

    maxi = max(Aloc)
    n = len(x)
    SWF = 0.0
    if(alpha == 1):
        for i in range(len(Aloc)):
            SWF += np.log(abs(Aloc[i]/maxi))
    else:
        for i in range(len(Aloc)):
            SWF += (Aloc[i]/maxi)**(1 - alpha)
        SWF = SWF / (1 - alpha)
    if(SWF == 0):
         SWF = 0.0000001
        
    return -1*SWF


