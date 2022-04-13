import numpy as np 
import matplotlib.pyplot as plt
from numpy import random
import networkx as nx

def get_leaders(G):
    return sorted(G.nodes, key = G.degree, reverse=True)[:6]

SocialGraph = nx.barabasi_albert_graph(60, 2, 42)
Leaders = get_leaders(SocialGraph)
Trump_Card = 59;

# You are given SocialGraph which reflects the social network of the 60 participants.
# Six chosen leaders are given to you as a list using variable called 'Leaders'

# Add any functions required

def Form_Teams(G, Leaders):
    """ Form six teams each consisting of 10 individuals """
    teams = {i:[] for i in Leaders}
    """ Add your code here """
    perm = random.permutation(6)
    teamlist = []
    for i in perm:
        neighbors = list(G.neighbors(Leaders[i]))
        print(Leaders[i], neighbors)
        if len(neighbors) >= 10:
            for j in range(10):
                if neighbors[j] not in teamlist:
                    teams[Leaders[i]].append(neighbors[j])
                    teamlist.append(neighbors[j])
        else:
            for j in range(len(neighbors)):
                if neighbors[j] not in teamlist:
                    teams[Leaders[i]].append(neighbors[j])
                    teamlist.append(neighbors[j])

    return teams

def Tug_of_war_Trump_Card(Teams):
    """ Tug of war round. Each team has equal chance of winning. Returns three winning teams."""
    """ Add your code here """
    perm = random.permutation(6)
    perm2 = random.permutation(2)
    Winning_Teams = {}
    keyslist = list(Teams.keys())
    Winning_Teams[keyslist[0]] = Teams(keyslist[0])
    Winning_Teams[keyslist[1]] = Teams(keyslist[1])
    
    return Winning_Teams

def simulate_Trump_Card(G, Leaders): # Copy this function from the previous subquestion with appropriate modifications
    """ Simulate the scenario multiple times """
    probabilities_of_winning = {i:0.2 for i in G.nodes}
    """ Modify the code as required """

    for i in range(10000):
        Teams = Form_Teams(G,Leaders)
        Winners = Tug_of_war_Trump_Card(Teams, Trump_Card) 
        # Update the probabilites

    return probabilities_of_winning