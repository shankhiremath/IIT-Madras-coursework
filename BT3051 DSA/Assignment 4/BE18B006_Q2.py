import networkx as nx
# Use of any function from networkx.algorithms module is strictly not allowed.
# Matplotlib can be used for visualization purposes
import matplotlib.pyplot as plt

# Add your functions here if needed

def dfs_cycle(G, node, visit_status, dfs_stack, cycle_list):
    visit_status[node] = True
    dfs_stack.append(node)
    
    while len(dfs_stack) > 0:
        vertex = dfs_stack.pop()
        for neighbor in list(G.adj[vertex]):
            if visit_status[neighbor] == False:
                dfs_stack.append(neighbor)
                visit_status[neighbor] = True
            else:
                for i in range(len(dfs_stack)):
                    if dfs_stack[i] == neighbor:
                        cycle_list.append(dfs_stack[i:])

def construct_metabolic_graph(name_of_json_file):
    """
    Given the reaction dict, return the metabolic directed bi-partite networkx graph
    """
    metabgraph = nx.DiGraph()
    data = eval(open(name_of_json_file, 'r').read())
    colors = {}
    for reaction in data['reactions']:
        metab = reaction['metabolites'].keys()
        reaction_id = reaction['id']
        l, j = len(metab), 0

        for m in metab:
            sval = reaction['metabolites'][m]
            if sval < 0 and j < l:
                metabgraph.add_edge(m, reaction_id)
                colors[m], colors[reaction_id] = 'blue', 'red'
            elif sval > 0 and j < l:
                metabgraph.add_edge(reaction_id, m)
                colors[m], colors[reaction_id] = 'blue', 'red'
            j += 1

    colornodes = [colors[node] for node in metabgraph.nodes()] 

    return metabgraph, colornodes


def Find_Cycles_In_Metabolic_Graph(Graph):
    """
    Given a bi-partite networkx graph, return the list of list of metabolites involved in the cycle i.
    """
    nodecount = Graph.number_of_nodes()
    visit_status, dfs_stack = {}, []
    cycle_list = []
    
    for node in list(Graph.nodes()):
        visit_status[node] = False

    for node in list(Graph.nodes()):
        if visit_status[node] == False:
            dfs_cycle(Graph, node, visit_status, dfs_stack, cycle_list)
    
    return cycle_list

# For the purpose of parsing, look under "metabolites" sub-section of "reaction" section. The stoichiometric coefficients will help you in determining if a metabolite is a reactant or a product.
G, colors = construct_metabolic_graph("e_coli_core.json")
# Add code to visualized G below
fig = plt.figure(1, figsize=(40, 20), dpi = 80)
nx.draw_kamada_kawai(G, with_labels = True, node_color = colors, font_weight = 'normal')
plt.show()

cycles = Find_Cycles_In_Metabolic_Graph(G)
print(cycles)