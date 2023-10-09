import time
import random
import numpy as np
from Graphs import Graph
from objFun import socialWelfare


def roundRobin_sample(n,k):
    r = random.randint(1,n)
    nodes = list(i % n for i in range(r, r + k))
    return nodes

def roundRobin(p,graph,alpha):
    n = graph.num_servers
    consensus = roundRobin_sample(n,p)
    #print(consensus)
    Fairness = socialWelfare(graph=graph,x=consensus,alpha=alpha)
    return Fairness,consensus


def Rand(p,graph,alpha):
    n = graph.num_servers
    consensus = random_list = random.sample(range(n), p)
    #print(consensus)
    Fairness = socialWelfare(graph=graph,x=consensus,alpha=alpha)
    
    return Fairness,consensus
