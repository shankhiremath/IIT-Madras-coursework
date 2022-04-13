import networkx as nx
# Use of any function from networkx.algorithms module is strictly not allowed.
# Other libraries are not allowed except for matplotlib for visualization purposes
from matplotlib import pyplot as plt

# Add your functions here if needed

def get_key(val, my_dict):
    for key, value in my_dict.items():
         if val == value:
                return key

def minimum_time_for_spread_of_contagion(G, patient_zero):
    """
    Given an connected undirected weighted networkx graph which represents the physical contant graph of a community and a node which represents patient zero of the contagion, return the minimum time taken for the contagion to spread in the complete graph.
    """
    V, inf = G.number_of_nodes(), float("inf")
    dist = [([inf] * V) for i in range(V)]
    weights = nx.get_edge_attributes(G , 'weight')
    node_dict_direct, node_dict = {}, {}
    
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
                    if i == patient_zero - 1:
                        #print('i =', i+1, 'k =', k+1, 'j =', j+1, 'dist[i][j] = ', dist[i][j])
                        node_dict[j+1] = dist[i][j]
                else:
                    if i == patient_zero - 1:
                        #print('i =', i+1, 'k =', k+1, 'j =', j+1, 'dist[i][j] = ', dist[i][j])
                        node_dict_direct[j+1] = dist[i][j]

    final_direct, direct_vals = {}, []
    for i in list(node_dict_direct.keys()):
        if i not in list(node_dict.keys()):
            final_direct[i] = node_dict_direct[i]
    final, vals = {}, []
    for i in list(node_dict.keys()):
        final[i] = node_dict[i]
        vals.append(node_dict[i])
    vals = sorted(vals)
    for k in final_direct:
        direct_vals.append(final_direct[k])
    
    direct_vals = sorted(direct_vals)
    
    answer = direct_vals + vals
    answer = max(answer)
    
    print('Expected output: ', answer, sep = '')
    print('Infected node | Time taken to reach that node')

    for i in direct_vals:
        print('     ', get_key(i, final_direct),  '        |  ', i, sep='')


    for i in vals:
        print('     ', get_key(i, final),  '        |  ', i, sep='')
    
G = nx.Graph()
G.add_edge(1,2,weight = 2); G.add_edge(3,2,weight = 3); G.add_edge(3,1,weight = 2)
G.add_edge(3,4,weight = 1); G.add_edge(4,5,weight =3); G.add_edge(5,6,weight =4)
G.add_edge(7,6,weight = 7); G.add_edge(5,8,weight =2); G.add_edge(7,8,weight =6)

# print(nx.info(G))
# pos = nx.spring_layout(G)
# nx.draw_networkx(G, pos)
# labels = nx.get_edge_attributes(G, 'weight')
# nx.draw_networkx_edge_labels(G, pos, edge_labels = labels)
# plt.show()

print(minimum_time_for_spread_of_contagion(G, 3))

# Expected output: 12
# Explanation: 
# Infected node | Time taken to reach that node
#      3        |  0
#      4        |  1
#      1        |  2
#      2        |  3
#      5        |  4 (1+3)
#      8        |  6 (1+3+2)
#      7        |  12(1+3+2+6)

# Hint:
# Therefore, minimum time taken to spread in the community = argmax_i(min(time taken to reach node i from patient zero node))
# Mininum time taken to reach node i from patient zero node can be thought of as a dynamic programming question. 
# Time taken to reach node i from node j can be thought of as a dynamic programming question. 
# To find the shortest path/minimum time taken for the person to be infected you can either use Dijkstra's algorithm or a dynamic programming variant of Dijkstra's algorithm i.e. Floyd-Warshall algorithm for all pairs of shortest paths

"""Pseudocode for Floyd-Warshall algorithm
let dist be a |V| × |V| array of minimum distances initialized to ∞ (infinity)
for each edge (u, v) do
    dist[u][v] ← w(u, v)  // The weight of the edge (u, v)
for each vertex v do
    dist[v][v] ← 0
for k from 1 to |V|
    for i from 1 to |V|
        for j from 1 to |V|
            if dist[i][j] > dist[i][k] + dist[k][j] 
                dist[i][j] ← dist[i][k] + dist[k][j]
            end if
"""