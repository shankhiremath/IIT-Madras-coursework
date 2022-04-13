# Question 3
import networkx as nx
# Use of any function from networkx.algorithms module is strictly not allowed.
# Other libraries are not allowed except for matplotlib for visualization purposes
import matplotlib.pyplot as plt

def planning_your_program(prerequisite_dict):
    """
    Given a dictionary of prerequisite courses, return the list of courses such that the sequence denotes the order in which the courses could possibly be done in order to satisfy the prerequisite condition.
    """
    
    """ Add your functions here if needed """
    
    def iscomplete(G, node_flag):
        '''
        Returns True if all nodes are marked P and False otherwise
        '''
        for node in list(G.nodes()):
            if node_flag[node] == 'U':
                return False
        return True
    
    def prereq(G, neighbor, node_flag):
        '''
        Returns True if a course has any pending prereqs and False otherwise
        '''
        prereq_list = list(G.pred[neighbor])
        for p in prereq_list:
            if node_flag[p] == 'U':
                return True
        return False
    
    def create_dependency_graph(prerequisite_dict):
        """Create and return a networkx dependency graph based on the prerequisite dictionary"""
        G = nx.DiGraph()
        # Add your code here
        for course in prerequisite_dict:
            for prereq in prerequisite_dict[course]:
                G.add_edge(prereq, course)
        # Visualisation
        #nx.draw_circular(G, with_labels = True)
        #plt.show()
        return G

    def find_the_program_pathway(G):
        """return the required program pathway from the Course Dependency Graph"""
        course_list = []
        # Add your code here
        node_flag = {}
        for node in list(G.nodes()):
            node_flag[node] = 'U'
        
        for node in list(G.nodes()):
            if len(list(G.pred[node])) == 0:
                node_flag[node] = 'P'
                course_list.append(node)
        
        for node in list(G.nodes()):
            if node_flag[node] == 'P':
                for neighbor in list(G.adj[node]):
                    if prereq(G, neighbor, node_flag) == False:
                        node_flag[neighbor] = 'P'
                        course_list.append(neighbor)    
                        if(iscomplete(G, node_flag) == True):
                            return course_list
                    else:
                        continue

    Course_Dependency_Graph = create_dependency_graph(prerequisite_dict)
    program_pathway = find_the_program_pathway(Course_Dependency_Graph)
    
    return program_pathway

prerequisite_dict = {"BT3051":["CS1100", "BT1000"], "CS6024":["BT3051"], "CS6091": ["CS6024", "BT3051", "CS1100"], "CS1100":[], "BT1000":[]}

print(planning_your_program(prerequisite_dict))
# Expected output: ["BT1000", "CS1100", "BT3051", "CS6024", "CS6091"] or ["CS1100", "BT1000", "BT3051", "CS6024", "CS6091"]

"""
Hints:
1. Firstly, complete all the courses that do not have any prerequisities. 
2. Then check if the first neighbors of the previous courses have prerequisities other than already completed courses. If not, then mark them complete.
3. Reiterate the 2nd step until all the courses are completed.
"""
