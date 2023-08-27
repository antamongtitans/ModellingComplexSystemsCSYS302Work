import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
import random
import csv

class travelor:
    def __init__(self, start_n, stop_n, max_m):
        self.nodes_traveled_rnd = [start_n]
        self.nodes_traveled_wrd = [start_n]
        self.current_node = start_n
        self.start_node = start_n
        self.return_start = False
        self.iter_return = 0
        self.number_nodes_rnd = 0
        self.unique_nodes_rnd = 0
        self.CF_rnd = 0
        self.number_nodes_wrd = 0
        self.unique_nodes_wrd = 0
        self.CF_wrd = 0
        self.groups = []
        self.max_moves = max_m
        self.destination = stop_n
        self.find_dest_rnd = False
        self.find_dest_wrd = False
        self.iter_dest_rnd = -1
        self.iter_dest_wrd = -1
        self.shortest_path = []
        
    def check_start_rnd(self, new_node):
        if (self.find_dest_rnd == False):
            if (self.destination == new_node):
                self.iter_dest_rnd = len(self.nodes_traveled_rnd) + 1
                return True
            else:
                return False
        else:
            return True
            
    def check_start_wrd(self, new_node):
        if (self.find_dest_wrd == False):
            if (self.destination == new_node):
                self.iter_dest_wrd = len(self.nodes_traveled_wrd) + 1
                return True
            else:
                return False
        else:
            return True
            
    def move_2_node_wrd(self, new_node):
        self.nodes_traveled_wrd.append(new_node)
        self.current_node = new_node
        self.find_dest_wrd = self.check_start_wrd(new_node)
        
    def move_2_node_rnd(self, new_node):
        self.nodes_traveled_rnd.append(new_node)
        self.current_node = new_node
        self.find_dest_rnd = self.check_start_rnd(new_node)
    
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
        self.number_nodes_wrd = len(self.nodes_traveled_wrd)
        self.unique_nodes_wrd = len(set(self.nodes_traveled_wrd))
        self.CF_wrd = float(self.unique_nodes_wrd) / self.number_nodes_wrd
        self.number_nodes_rnd = len(self.nodes_traveled_rnd)
        self.unique_nodes_rnd = len(set(self.nodes_traveled_rnd))
        self.CF_rnd = float(self.unique_nodes_rnd) / self.number_nodes_rnd
        shortest_path_len = len(self.shortest_path)
        return [self.CF_wrd, self.unique_nodes_wrd, self.number_nodes_wrd, self.find_dest_wrd, self.iter_dest_wrd, shortest_path_len, self.CF_rnd, self.unique_nodes_rnd, self.number_nodes_rnd, self.find_dest_rnd, self.iter_dest_rnd]
        
    def update_groups(self, group_in):
        self.groups = group_in
        
    def done_traveling(self, moves):
        if (self.destination == self.current_node):
            return True
        if (moves > self.max_moves):
            return True
        return False
        
    def shortest_path_1(self, path):
        self.shortest_path = path
    
    def update_rand_moves(self,rnd_moves):
        self.num_random_moves = rnd_moves
        
    def reset(self):
        self.current_node = self.start_node

def find_stop_n(G, groups_dict, start_node):
    #find start node group
    remove_groups = groups_dict[start_node]
    stop_nodes = []
    print(remove_groups)
    #eliminate all nodes with those groups
    for key, value in groups_dict.items():
        if (not any(item in value for item in remove_groups)):
            stop_nodes.append(key)
    #randomly select from nodes left
    return random.choice(stop_nodes)
    
def get_weighted_moves(start_node, possible_nodes, g2g, groups_dict):
    possible_nodes_out = []
    start_groups = groups_dict[start_node]
    for node in possible_nodes:
        multiply_node_by = 0
        end_groups = groups_dict[node]
        for group_start in start_groups:
            for group_end in end_groups:
                multiply_node_by = multiply_node_by + g2g[group_start][group_end]
        for i in range(int(multiply_node_by)):
            possible_nodes_out.append(node)
    #get possible end_nodes
    #find groups of end_nodes
    #look up in matrix [start_node_group][end_node_group]
    #add multiple times if different groups
    #add to possible nodes repeated a bunch then select a random one from the list
    return possible_nodes_out

def run_simulation(iterations, max_moves, G, g2g_matrix, groups_dict):
    #create list of travelors
    travelors = []
    for iter in range(iterations):
        start_node = random.choice(list(G.nodes()))
        stop_node = find_stop_n(G, groups_dict, start_node)
        #Create new simulation
        my_travelor = travelor(start_node, stop_node, max_moves)
        my_travelor.update_groups(groups_dict[start_node])
        #test with random moves how long it takes
        moves = 0
        while (not my_travelor.done_traveling(moves)):
            new_node = random.choice(list(nx.node_connected_component(G, my_travelor.get_current_node())))
            my_travelor.move_2_node_rnd(new_node)
            moves = moves + 1
        my_travelor.update_rand_moves(moves)
        #test with weird walk how long it takes
        moves = 0
        my_travelor.reset()
        while (not my_travelor.done_traveling(moves)):
            unweighted_moves = list(nx.node_connected_component(G, my_travelor.get_current_node()))
            possible_moves = get_weighted_moves(my_travelor.get_current_node(), unweighted_moves, g2g_matrix, groups_dict)
            new_node = random.choice(possible_moves)
            my_travelor.move_2_node_wrd(new_node)
            moves = moves + 1
        #find shortest path for comparison add to travelors
        path = nx.shortest_path(G, source=start_node, target=stop_node)
        my_travelor.shortest_path_1(path)
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
    iterations = 100
    moves = 10000
    #reading in csv file
    mydata = np.genfromtxt('MARVEL P2P.csv', delimiter=',')
    p2p_matrix = mydata[1:,1:]
    #groups
    marvalG2G_in = np.genfromtxt('MARVEL G2G.csv', delimiter=',')
    g2g_matrix = marvalG2G_in[1:,1:]
    
    proj_in = np.genfromtxt('MARVEL Project.csv', delimiter=',')
    proj_matrix = proj_in[1:,1:]
    
    travelor_groups = {}
    for idx, x in np.ndenumerate(proj_matrix):
        if (x == 1):
            if (idx[0] in travelor_groups.keys()):
                list_g = travelor_groups[idx[0]]
                list_g.append(idx[1])
            else:
                list_g = [idx[1]]
            travelor_groups[idx[0]] = list_g
    
    #update travelors 
    G = nx.from_numpy_matrix(p2p_matrix)
    travelors = run_simulation(iterations, moves, G, g2g_matrix, travelor_groups)
    #move above to sperate function
    #color eges that have been traversed / get edges that have been travered probably through list of nodes just tuple at every step
    #color nodes that have been visited
    #functionafy to make it happen for many iterations
    display_graph(False, G)
    display_graph_paths(False, G, travelors[3])
    with open('p2p_marvelCF_part3_10000step.csv', mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow(['Wrd CF','Wrd Unique Nodes','Wrd Total Nodes','Wrd Fnd Dest','Wrd Dest Iteration','Shortest Path Length','Rnd CF','Rnd Unique Nodes','Rnd Total Nodes','Rnd Fnd Dest','Rnd Dest Iteration'])
        for travelor in travelors:
            csv_writer.writerow(travelor.calculate_stats())
            if (travelor.get_return_status()):
                print ("travelor returned on move: " + str(travelor.get_return_move()))