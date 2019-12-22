# Program for Baseball Elimination

#  Algorithms Programming Assignment

#  Author - Shubham Rohal & Puneet Soni

import pandas as pd
import networkx as nx
import csv
from itertools import chain

# Change the input file in next line to test the input files.
with open('1.txt', 'r') as fin:
    data = fin.read().splitlines(True)
with open('new.txt', 'w') as fout:
    fout.writelines(data[1:])
with open('new.txt', 'r') as in_file:
    stripped = (line.strip('\n') for line in in_file)
    lines = (line.split() for line in stripped if line)
    with open('log.csv', 'w') as out_file:
        writer = csv.writer(out_file)
        writer.writerows(lines)
teams = int(data[0])
if (teams == 1):
    print('-1')
# print("Number of teams="+str(teams))
else:
    data = pd.read_csv('log.csv', header=None)
    wins = data.iloc[:, 1]
    remain = data.iloc[:, 3]
    eliminated = []
    max_wins= max(wins)
    #print(max_wins)
    leader=[]
    for i in range(teams):
        if wins[i]== max_wins:
            leader.append(i)
    if(sum(remain)==0):
        for i in range(teams):
            eliminated.append(i)
        for i in range(len(leader)):
            eliminated.remove(leader[i])
        for i in eliminated:
                #print("Teams which got eliminated are -")
                print(i, end=" ")
    else:
        i = 0
        n = 5
        layer1_values = []
        for i in range(teams - 1):
            y = pd.array(data.iloc[i])
            layer1_values.append(y[n:])
            n = n + 1
        Layer1_capacities = list(chain.from_iterable(layer1_values))
        layer_id = 'L1'
        layer_1_ids = []
        for i in range(0, len(Layer1_capacities)):
            node_id = layer_id + str(i)
            layer_1_ids.append(node_id)
        layer_id = 'L2'
        layer_2_ids = []
        for i in range(0, teams):
            node_id = layer_id + str(i)
            layer_2_ids.append(node_id)


        def ford_fulkerson(graph, source, sink, i):
            flow, path = 0, True

            while path:
                # search for path with flow reserve
                path, reserve = depth_first_search(graph, source, sink)
                flow += reserve

                # increase flow along the path
                for v, u in zip(path, path[1:]):
                    if graph.has_edge(v, u):
                        graph[v][u]['flow'] += reserve
                    else:
                        graph[u][v]['flow'] -= reserve

            the_Sum = sum(Layer1_capacities)
            # print(flow)
            # print(the_Sum)
            if flow != the_Sum:
                eliminated.append(i)


        def depth_first_search(graph, source, sink):
            undirected = graph.to_undirected()
            explored = {source}
            stack = [(source, 0, dict(undirected[source]))]

            while stack:
                v, _, neighbours = stack[-1]
                if v == sink:
                    break

                # search the next neighbour
                while neighbours:
                    u, e = neighbours.popitem()
                    if u not in explored:
                        break
                else:
                    stack.pop()
                    continue

                # current flow and capacity
                in_direction = graph.has_edge(v, u)
                capacity = e['capacity']
                flow = e['flow']
                neighbours = dict(undirected[u])

                # increase or redirect flow at the edge
                if in_direction and flow < capacity:
                    stack.append((u, capacity - flow, neighbours))
                    explored.add(u)
                elif not in_direction and flow:
                    stack.append((u, flow, neighbours))
                    explored.add(u)

            # (source, sink) path and its flow reserve
            reserve = min((f for _, f, _ in stack[1:]), default=0)
            path = [v for v, _, _ in stack]

            return path, reserve


        for n in range(0, teams):
            graph = nx.DiGraph()
            graph.add_node('S')
            graph.add_nodes_from(layer_1_ids)
            graph.add_nodes_from(layer_2_ids)
            graph.add_node('T')
            Twins = [wins[n] + remain[n]]
            for i in range(0, len(layer_1_ids)):
                graph.add_edges_from([('S', layer_1_ids[i], {'capacity': Layer1_capacities[i], 'flow': 0})])
            k = 0
            for i in range(0, teams):
                for j in range(i, teams - 1):
                    graph.add_edges_from([(layer_1_ids[k], layer_2_ids[i], {'capacity': Layer1_capacities[k], 'flow': 0})])
                    graph.add_edges_from(
                        [(layer_1_ids[k], layer_2_ids[j + 1], {'capacity': Layer1_capacities[k], 'flow': 0})])
                    if (k < (((teams * (teams - 1)) / 2) - 1)):
                        k = k + 1
            for i in range(0, teams):
                if (i == n):
                    graph.add_edges_from([(layer_2_ids[i], 'T', {'capacity': remain[i], 'flow': 0})])
                else:
                    graph.add_edges_from([(layer_2_ids[i], 'T', {'capacity': Twins - wins[i], 'flow': 0})])
            ford_fulkerson(graph, 'S', 'T', n)

       # print(eliminated)

        # %%
        print("------------------------Project for Baseball Elimination------------------------")

        # To check the condition and print the value for the eliminated teams

        if (len(eliminated) == 0):
           # print("-1 denotes teams are not eliminated")
            print(-1)
        else:
           # print("Teams which got eliminated are -")
            for i in eliminated:
                print(i, end=" ")

