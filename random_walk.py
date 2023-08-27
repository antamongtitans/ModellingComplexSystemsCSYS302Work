import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import csv

def output_lines(x, y, z):
    start_node = [x[0], y[0], z[0]]
    node_path = []
    returned = False
    return_iter = -1
    for node in range(1,len(x)):
        node_path.append([x[node], y[node], z[node]])
        if (start_node == [x[node], y[node], z[node]]):
            print("Returned at iter: " + str(node))
            return_iter = node
            returned = True
    total_nodes = len(x)
    unique_nodes = len(set(map(tuple,node_path)))
    CF = float(unique_nodes) / total_nodes
    #unique_nodes = len(map(list,unique_nodes_tuple))
    return [CF, unique_nodes, total_nodes, returned, return_iter]
    
N = 1000
iterations = 100
csv_lines = []
with open('3d_randomWalkCF_part1.csv', mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    csv_writer.writerow(['CF','Unique Nodes','Total Nodes','Returned','Return Iteration'])
    for iter in range(iterations):
        R = (np.random.rand(N)*6).astype("int")
        x = np.zeros(N)
        y = np.zeros(N)
        z = np.zeros(N)
        x[ R==0 ] = -1; x[ R==1 ] = 1
        y[ R==2 ] = -1; y[ R==3 ] = 1
        z[ R==4 ] = -1; z[ R==5 ] = 1
        x = np.cumsum(x)
        y = np.cumsum(y)
        z = np.cumsum(z)
        csv_writer.writerow(output_lines(x,y,z))

plt.figure()
ax = plt.subplot(1,1,1, projection='3d')
ax.plot(x, y, z,alpha=0.6)
ax.scatter(x[-1],y[-1],z[-1])
plt.show()