
"""
This file contains the functions that solve question 1 and 2 from FIT2004 Assignment 4.

Graph class: Converts the vfile and efile into a graph that is stored using an edge list
captured_chains: Function which solves question 1
DFS: Runs depth first search
Terrain_pathfinding: Function which solves question 2
index_to_vehicle_type: Converts an index into the string that represents the vehicle type

Author: Damien Ambegoda (30594235)
Last modified: 3/11/2020
"""

from collections import deque
import re
from math import inf
import queue


class Graph:
    """ Creates graph from vfile and efile
    self.vertex_properties: stores the special property of each vertex
    self.edge_list: stores the edges of each vertex. Each vertex is given a nested list.

    Each vertex's ID is in the index to access its data in vertex_properties and edge_list
    """
    def __init__(self, vfile, efile):
        """ Initialises Graph by reading vfile and efile

        :param vfile: txt file with vertex data. First line is the number of vertices and every other line is "a b"
                      where a is the vertex number and b is the property of the vertex.

        :param efile: txt file with edge data. First line is the number of edges and every other line is "u v" where
                      u and v are vertex ID's and represents an edge between u and v
        Time Complexity: O(V + E) where V is the number of vertices in vfile and E is the number of edges in efile
        """
        # vertex_properties[i] stores the property of the vertex with ID = i
        self.vertex_properties = []

        # edge_list[i] stores the vertices that can be reached from the ith vertex
        self.edge_list = [[]]

        f = open(str(vfile))
        vertex_counter = int(f.readline())
        # Each vertex has its own index in vertex_properties and edge_list
        self.vertex_properties = [None for _ in range(vertex_counter)]
        self.edge_list = [[] for _ in range(vertex_counter)]

        # Reads each line in vfile after the first line and stores the vertex property
        for _ in range(vertex_counter):
            line = f.readline()
            x = re.findall(r'([0-9]*)( )([0-9]*)', line)
            self.vertex_properties[int(x[0][0])] = int(x[0][2])
        f.close()
        f = open(str(efile))
        edge_counter = int(f.readline())

        # Reads each line in efile after the first line and stores the edge's destination in the edge_list. If the edge
        # is between u and v, it stores v in u's edge list and stores u in v's edge list
        for _ in range(edge_counter):
            line = f.readline()
            x = re.findall(r'([0-9]*)( )([0-9]*)', line)
            u = x[0][0]
            v = x[0][2]
            self.edge_list[int(u)].append(int(v))
            self.edge_list[int(v)].append(int(u))
        f.close()


def captured_chains(vfile, efile):
    """ Given the vertex data and edge data (discussed in Graph.__init__), the function determines what chains are
    captured. It converts the vertex and edge data into a graph by calling the Graph class and using depth first search,
    determines which chains of the same colour are not next to an empty vertex.

    Time Complexity: O(V + E) where V is the number of vertices in the input graph and E is the number of edges in the
                     input graph
    """
    # Graph class convertes vfile and efile into a graph
    graph = Graph(vfile, efile)
    global visited
    visited = [0]*len(graph.vertex_properties)
    res = []

    # checks every vertex
    for vertex_index in range(len(visited)):
        # function does not run again
        if not visited[vertex_index]:
            global current_chain
            current_chain = []
            global captured_chain_check
            captured_chain_check = deque()
            DFS(graph, vertex_index)
            if len(current_chain) != 0 and len(captured_chain_check) == 0:
                res.append(current_chain)
            captured_chain_check.clear()
    return res


def DFS(graph, vertex_ID):
    if visited[vertex_ID] == 1:
        return
    visited[vertex_ID] = 1
    colour = graph.vertex_properties[vertex_ID]
    if colour == 0:
        return
    empty_vertex_neighbour = False
    stack = deque()
    for edge in graph.edge_list[vertex_ID]:
        if graph.vertex_properties[edge] == 0:
            empty_vertex_neighbour = True
        if graph.vertex_properties[edge] == colour and not visited[edge]:
            stack.append(edge)
    if not empty_vertex_neighbour:
        current_chain.append(vertex_ID)
    else:
        captured_chain_check.append('X')

    while len(stack) != 0:
        next_vertex = stack.pop()
        DFS(graph, next_vertex)


def terrain_pathfinding(vfile, efile, crossing_time, transform_cost, start, end):
    if start == end:
        return (0, [])
    graph = Graph(vfile, efile)
    pqueue = queue.PriorityQueue()
    # If each index has a triplet, 0 is wheel, 1 is tank, 2 is hover. Wheel, tank and hover will be referred to as
    # subvertex as every vertex can be travelled through with each form
    # O(V)
    distance_to_vertex = [[inf, inf, inf] for _ in range(len(graph.vertex_properties))]
    distance_to_vertex[start] = [0, transform_cost, transform_cost]
    # O(V)
    distance_through_vertex = [[inf, inf, inf] for _ in range(len(graph.vertex_properties))]

    # O(V)
    visited = [[0,0,0] for _ in range(len(graph.vertex_properties))]
    # O(V)
    pred = [[(None, None),(None, None),(None, None)] for _ in range(len(graph.vertex_properties))]
    pred[start] = [(0, 0), (0,0), (0,0)]

    # Saves the time required to travel through each subvertex
    # O(V)
    for i in range(len(graph.vertex_properties)):
        if graph.vertex_properties[i] == 0:
            distance_through_vertex[i] = [crossing_time["wheel"]["plain"], crossing_time["tank"]["plain"],
                                          crossing_time["hover"]["plain"]]
        elif graph.vertex_properties[i] == 1:
            distance_through_vertex[i] = [crossing_time["wheel"]["hill"], crossing_time["tank"]["hill"],
                                          crossing_time["hover"]["hill"]]
        else:
            distance_through_vertex[i] = [crossing_time["wheel"]["swamp"], crossing_time["tank"]["swamp"],
                                          crossing_time["hover"]["swamp"]]

    # Pushes every subvertex onto priority queue
    # O(3V)
    for i in range(len(distance_to_vertex)):
        for j in range(len(distance_through_vertex[0])):
            pqueue.put((distance_to_vertex[i][j], i, j))
    # each subvertex checked once
    # O(3V)
    while not pqueue.empty() and visited[end] == [0,0,0]:
        curr_distance_to, curr_vertex_ID, subvertex = pqueue.get()
        # If vertex has already been visited, ignore it. After it has been visited, the distance is locked in
        if visited[curr_vertex_ID][subvertex] == 1:
            continue
        # if vertex has been updated after this version was pushed then ignore it
        if curr_distance_to != distance_to_vertex[curr_vertex_ID][subvertex]:
            continue
        visited[curr_vertex_ID][subvertex] = 1

        relaxed_vertices = []
        # O(E)
        edge_index_in_relax_vertices = -1
        for edge_destination in graph.edge_list[curr_vertex_ID]:
            edge_index_in_relax_vertices += 1
            # Goes through each subvertex
            # If edge_destination's  has been finalised then it can't be relaxed

            relaxed_vertices.append([edge_destination, 0, 0, 0])

            # pred = [[(None, None),(None, None),(None, None)] for _ in range(len(graph.vertex_properties))]
            if subvertex == 0:
                # distance from current subvertex to next subvertex is the distance to travel through current
                # vertex as wheel + the distance to get to this vertex. Transforming before leaving current vertex. If at w subvertex
                # and pred is not a wheel then transform first then make transition

                if visited[edge_destination][0] == 0:
                    travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][0] + \
                                                            distance_to_vertex[curr_vertex_ID][0]
                    # If travelling through current vertex is a shorter path than previous path to next vertex then relax
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][0]:
                        distance_to_vertex[edge_destination][0] = travel_through_current_vertex_to_next
                        pred[edge_destination][0] = (curr_vertex_ID, 0)
                        relaxed_vertices[edge_index_in_relax_vertices][1] = 1

                if visited[edge_destination][1] == 0:
                    if edge_destination != end:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][0] + distance_to_vertex[curr_vertex_ID][0] + transform_cost
                    else:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][0] + \
                                                                distance_to_vertex[curr_vertex_ID][0]
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][1]:
                        distance_to_vertex[edge_destination][1] = travel_through_current_vertex_to_next
                        pred[edge_destination][1] = (curr_vertex_ID, 0)
                        relaxed_vertices[edge_index_in_relax_vertices][2] = 1

                if visited[edge_destination][2] == 0:
                    if edge_destination != end:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][0] + \
                                                                distance_to_vertex[curr_vertex_ID][
                                                                    0] + transform_cost
                    else:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][0] + \
                                                                distance_to_vertex[curr_vertex_ID][0]
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][2]:
                        distance_to_vertex[edge_destination][2] = travel_through_current_vertex_to_next
                        pred[edge_destination][2] = (curr_vertex_ID, 0)
                        relaxed_vertices[edge_index_in_relax_vertices][3] = 1

            if subvertex == 1:
                # distance from current subvertex to next subvertex is the distance to travel through current
                # vertex as wheel + the distance to get to this vertex. Transforming before leaving current vertex. If at w subvertex
                # and pred is not a wheel then transform first then make transition

                if visited[edge_destination][0] == 0:
                    # If travelling through current vertex is a shorter path than previous path to next vertex then relax
                    if edge_destination != end:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][1] + \
                                                                distance_to_vertex[curr_vertex_ID][1] + transform_cost
                    else:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][1] + \
                                                                distance_to_vertex[curr_vertex_ID][1]
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][0]:
                        distance_to_vertex[edge_destination][0] = travel_through_current_vertex_to_next
                        pred[edge_destination][0] = (curr_vertex_ID, 1)
                        relaxed_vertices[edge_index_in_relax_vertices][1] = 1

                if visited[edge_destination][1] == 0:
                    travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][1] + \
                                                            distance_to_vertex[curr_vertex_ID][1]
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][1]:
                        distance_to_vertex[edge_destination][1] = travel_through_current_vertex_to_next
                        pred[edge_destination][1] = (curr_vertex_ID, 1)
                        relaxed_vertices[edge_index_in_relax_vertices][2] = 1

                if visited[edge_destination][2] == 0:
                    if edge_destination != end:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][1] + \
                                                                distance_to_vertex[curr_vertex_ID][1] + transform_cost
                    else:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][1] + \
                                                                distance_to_vertex[curr_vertex_ID][1]
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][2]:
                        distance_to_vertex[edge_destination][2] = travel_through_current_vertex_to_next
                        pred[edge_destination][2] = (curr_vertex_ID, 1)
                        relaxed_vertices[edge_index_in_relax_vertices][3] = 1

            if subvertex == 2:
                # distance from current subvertex to next subvertex is the distance to travel through current
                # vertex as wheel + the distance to get to this vertex. Transforming before leaving current vertex. If at w subvertex
                # and pred is not a wheel then transform first then make transition
                if visited[edge_destination][0] == 0:
                    if edge_destination != end:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][2] + \
                                                                distance_to_vertex[curr_vertex_ID][2] + transform_cost
                    else:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][2] + \
                                                                distance_to_vertex[curr_vertex_ID][2]
                    # If travelling through current vertex is a shorter path than previous path to next vertex then relax
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][0]:
                        distance_to_vertex[edge_destination][0] = travel_through_current_vertex_to_next
                        pred[edge_destination][0] = (curr_vertex_ID, 2)
                        relaxed_vertices[edge_index_in_relax_vertices][1] = 1

                if visited[edge_destination][1] == 0:
                    if edge_destination != end:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][2] + \
                                                                distance_to_vertex[curr_vertex_ID][2] + transform_cost
                    else:
                        travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][2] + \
                                                                distance_to_vertex[curr_vertex_ID][2]
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][1]:
                        distance_to_vertex[edge_destination][1] = travel_through_current_vertex_to_next
                        pred[edge_destination][1] = (curr_vertex_ID, 2)
                        relaxed_vertices[edge_index_in_relax_vertices][2] = 1

                if visited[edge_destination][2] == 0:
                    travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][2] + \
                                                            distance_to_vertex[curr_vertex_ID][2]
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][2]:
                        distance_to_vertex[edge_destination][2] = travel_through_current_vertex_to_next
                        pred[edge_destination][2] = (curr_vertex_ID, 2)
                        relaxed_vertices[edge_index_in_relax_vertices][3] = 1

        #relaxed_vertices.append([edge_destination, 0, 0, 0])
        # O(V)
        # If vertexes have been relaxed, repush them into the pqueue
        for i in range(edge_index_in_relax_vertices+1):
            for j in range(1, 4):
                if relaxed_vertices[i][j] == 1:
                    # O(logV)
                    # Push (distance to subvertex, vertex_id, subvertex_id)
                    pqueue.put((distance_to_vertex[relaxed_vertices[i][0]][j-1], relaxed_vertices[i][0], j-1))

    min_distance_index = 0
    for x in range(1, len(distance_to_vertex[end])):
        if distance_to_vertex[end][x] < distance_to_vertex[end][min_distance_index]:
            min_distance_index = x

    # pred = [[(None, None), (None, None), (None, None)] for _ in range(len(graph.vertex_properties))]
    # pred[edge_destination][2] = (curr_ID, 2)
    # pred tuple is (vertex_ID, which vehicle type)
    res = [distance_to_vertex[end][min_distance_index], []]
    res_temp = []
    str = index_to_vehicle_type(pred[end][min_distance_index][1])
    res_temp.append((end, str))

    pred_vertex = pred[end][min_distance_index]
    while res_temp[-1][0] != start:
        curr_vertex_ID, subvertex = pred_vertex
        vehicle_type = index_to_vehicle_type(subvertex)
        res_temp.append((curr_vertex_ID, vehicle_type))

        pred_vertex = pred[curr_vertex_ID][subvertex]
    for i in range(len(res_temp)-1, -1, -1):
        res[1].append(res_temp[i])
    return res


def index_to_vehicle_type(index):
    if index == 0:
        return "wheel"
    if index == 1:
        return "tank"
    if index == 2:
        return "hover"



