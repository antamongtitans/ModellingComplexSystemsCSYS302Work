import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import random
import csv
import sys

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
    
    def get_start_node(self):
        return [self.start_node]
        
    def get_stop_node(self):
        return [self.current_node]
        
    def calculate_stats(self):
        self.number_nodes = len(self.nodes_traveled)
        self.unique_nodes = len(set(self.nodes_traveled))
        self.CF = float(self.unique_nodes) / self.number_nodes
        return [self.CF, self.unique_nodes, self.number_nodes, float(self.return_start), self.iter_return]
    
def run_simulation(moves, G, start_nodes):
    #create list of travelors
    travelors = []
    my_travelor = None
    #random.seed(datetime.now())
    for iter in range(len(start_nodes)):
        #Create new simulation
        my_travelor = travelor(start_nodes[iter])
        for i in range(moves):
            new_node = random.choice(list(nx.node_connected_component(G, my_travelor.get_current_node())))
            my_travelor.move_2_node(new_node)
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
        nx.draw_networkx_nodes(Graph, pos, nodelist=my_travelor.get_start_node(), node_color="g", **options)
        nx.draw_networkx_nodes(Graph, pos, nodelist=my_travelor.get_stop_node(), node_color="y", **options)
        nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5)
        nx.draw_networkx_edges(G, pos, edgelist=my_travelor.get_edge_list(), width=8, alpha=0.5, edge_color="r",)
        plt.show()
        
if __name__ == "__main__":
    start_nodes = [133, 988, 1283, 236, 830, 587, 634, 662, 663, 667, 1504, 1510, 1055, 1143, 1309, 1481, 344, 1283, 1135, 240, 791,
    799, 825, 842, 851, 1037, 1226, 1055, 1143, 1309, 1481, 236, 1283, 344, 1135, 587, 634, 662, 663, 667, 1504, 1510, 1055, 1143, 1309]
    moves = 1000
    iters = 100
    #reading in csv file
    mydata = np.genfromtxt('MARVEL P2P.csv', delimiter=',')
    p2p_matrix = mydata[1:,1:]
    G = nx.from_numpy_matrix(p2p_matrix)
    #for some reason doesn't work
    travelors_total = []
    for i in range(len(start_nodes)):   
        travelors_total.append([0,0,0,0,0])

    for iter in range(iters):
        output_str = "iteration: " + str(iter) + " started"
        sys.stdout.write(output_str)
        sys.stdout.flush()
        travelors = []
        travelors = run_simulation(moves, G, start_nodes)
        current_travelor = 0
        for travelor_1 in travelors:
            addition = travelor_1.calculate_stats()
            for item in range(len(addition)):
                travelors_total[current_travelor][item] = travelors_total[current_travelor][item] + addition[item]
            current_travelor = current_travelor + 1
       
    with open('p2p_marvelCF_part2_1000_teststep_100iter.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['CF','Unique Nodes','Total Nodes','Returned','Return Iteration'])
        print(travelors_total)
        for i in range(len(travelors_total)):
            travelors_total[i][:] = [float(x) / iters for x in travelors_total[i]]
        for travelor in travelors_total:
            csv_writer.writerow(travelor)