import networkx as nx
# Use of any function from networkx.algorithms module is strictly not allowed.
# Other libraries are not allowed except for matplotlib for visualization purposes

# Add your functions here if needed
# You are allowed to use the function that you used in the previous subquestion

def get_key(val, my_dict):
    for key, value in my_dict.items():
         if val == value:
                return key

def most_critical_node_for_contagion(G):
    """
    Given an connected undirected weighted networkx graph which represents the physical contant graph of a community, return the most critical node. The infection of the most critical node will result in minimum time for the spread in the whole community.
    """
    dist_dict = {}
    for node in list(G.nodes()):
        dist_dict[node] = minimum_time_for_spread_of_contagion(G, node)
    values = []
    for key in dist_dict:
        values.append(dist_dict[key])
    answer = get_key(min(values), dist_dict)
    print('Expected output:', answer)
    print('Patient zero node | minimum time taken')
    nodelist = sorted(list(G.nodes()))
    for i in nodelist:
        if i == answer:
            print('     ', i, '            |  ', dist_dict[i], ' - minimum time', sep='')
        else:
            print('     ', i, '            |  ', dist_dict[i], sep='')    

def minimum_time_for_spread_of_contagion(G, patient_zero):
    """
    Given an connected undirected weighted networkx graph which represents the physical contant graph of a community and a node which represents patient zero of the contagion, return the minimum time taken for the contagion to spread in the complete graph.
    """
    V, inf = G.number_of_nodes(), float("inf")
    dist = [([inf] * V) for i in range(V)]
    weights = nx.get_edge_attributes(G , 'weight')
    
    for i, j in list(G.edges()):
        dist[i - 1][j - 1] = weights[(i, j)]
        dist[j - 1][i - 1] = weights[(i, j)]
        
    for i in list(G.nodes()):
        dist[i - 1][i - 1] = 0

    for k in range(V):
        for i in range(V):
            for j in range(V):
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    
    distances = dist[patient_zero - 1]
    return max(distances)

G = nx.Graph()
G.add_edge(1,2,weight = 2); G.add_edge(3,2,weight = 3); G.add_edge(3,1,weight = 2)
G.add_edge(3,4,weight = 1); G.add_edge(4,5,weight =3); G.add_edge(5,6,weight =4)
G.add_edge(7,6,weight =7); G.add_edge(5,8,weight =2); G.add_edge(7,8,weight =6)

print(most_critical_node_for_contagion(G))
# Expected output: 5
# Explanation: 
# Patient zero node | minimum time taken
#      1            |  15
#      2            |  16
#      3            |  12
#      4            |  11
#      5            |  8 - minimum time
#      6            |  12
#      7            |  15