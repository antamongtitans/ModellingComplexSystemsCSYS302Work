import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import random
import csv

class travelor:
    def __init__(self, start_n):
        self.nodes_traveled = [start_n]
        self.current_node = start_n
        self.start_node = start_n
        self.return_start = False
        self.iter_return = 0
        self.number_nodes = 0
        self.unique_nodes = 0
        self.CF = 0
        
    def check_start(self, new_node):
        if (self.return_start == False):
            if (self.start_node == new_node):
                self.iter_return = len(self.nodes_traveled) + 1
                return True
            else:
                return False
        else:
            return True
            
    def move_2_node(self, new_node):
        self.nodes_traveled.append(new_node)
        self.current_node = new_node
        self.return_start = self.check_start(new_node)
    
    def get_path(self):
        return self.nodes_traveled
        
    def get_edge_list(self):
        edge_list = []
        for iter in range(len(self.nodes_traveled) - 1):
            edge_list.append((self.nodes_traveled[iter], self.nodes_traveled[iter+1]))
        return edge_list
        
    def get_return_status(self):
        return self.return_start
        
    def get_return_move(self):
        return self.iter_return
        
    def get_current_node(self):
        return self.current_node
        
    def calculate_stats(self):
        self.number_nodes = len(self.nodes_traveled)
        self.unique_nodes = len(set(self.nodes_traveled))
        self.CF = float(self.unique_nodes) / self.number_nodes
        return [self.CF, self.unique_nodes, self.number_nodes, self.return_start, self.iter_return]
    
def run_simulation(iterations, moves, G):
    #create list of travelors
    travelors = []
    for iter in range(iterations):
        #Create new simulation
        my_travelor = travelor(random.choice(list(G.nodes())))
        for i in range(moves):
            new_node = random.choice(list(nx.node_connected_component(G, my_travelor.get_current_node())))
            my_travelor.move_2_node(new_node)
            #print(new_node)
        travelors.append(my_travelor)
    return travelors

def display_graph(display, Graph):
    if (display):
        pos = nx.spring_layout(Graph,k=0.25,iterations=25,seed=17)
        nx.draw(Graph, pos)
        plt.show()

def display_graph_paths(display, Graph, my_travelor):
    if (display):
        pos = nx.spring_layout(Graph,k=0.25,iterations=25,seed=17)
        no_traveled_nodes = [node for node in list(G.nodes()) if node not in my_travelor.get_path()]
        options = {"node_size": 100, "alpha": 0.8}
        nx.draw_networkx_nodes(Graph, pos, nodelist=no_traveled_nodes, node_color="b", **options)
        nx.draw_networkx_nodes(Graph, pos, nodelist=my_travelor.get_path(), node_color="r", **options)
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_edges(G, pos, edgelist=my_travelor.get_edge_list(), width=8, alpha=0.5, edge_color="r",)
        plt.show()
        
if __name__ == "__main__":
    iterations = 10
    moves = 100
    #reading in csv file
    mydata = np.genfromtxt('MARVEL P2P.csv', delimiter=',')
    p2p_matrix = mydata[1:,1:]
    G = nx.from_numpy_matrix(p2p_matrix)
    travelors = run_simulation(iterations, moves, G)
    #move above to sperate function
    #color eges that have been traversed / get edges that have been travered probably through list of nodes just tuple at every step
    #color nodes that have been visited
    #functionafy to make it happen for many iterations
    display_graph(False, G)
    display_graph_paths(False, G, travelors[8])
    with open('p2p_marvelCF_part1.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['CF','Unique Nodes','Total Nodes','Returned','Return Iteration'])
        for travelor in travelors:
            csv_writer.writerow(travelor.calculate_stats())
            if (travelor.get_return_status()):
                print ("travelor returned on move: " + str(travelor.get_return_move()))