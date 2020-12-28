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

    Time Complexity: O(V + E) where V is the number of vertices in the vfile and E is the number of edges in the
                     efile
    """
    # Graph class convertes vfile and efile into a graph
    graph = Graph(vfile, efile)

    # visited list is global so it can be accessed through any of the recursive calls
    global visited
    visited = [0]*len(graph.vertex_properties)
    res = []

    # runs on every vertex which ensures that no vertex is skipped
    for vertex_index in range(len(visited)):
        # vertices may have already been visited due to being part of the DFS so the visited list ensures no vertex is
        # visited more than once
        if not visited[vertex_index]:
            # current_chain and captured_chain_check is global so that it can be accessed through the recursive calls
            global current_chain
            current_chain = []
            global captured_chain_check

            # calls the queue class
            captured_chain_check = deque()

            DFS(graph, vertex_index)
            if len(current_chain) != 0 and len(captured_chain_check) == 0:
                res.append(current_chain)
            captured_chain_check.clear()
    return res


def DFS(graph, vertex_ID):
    """ Given a graph and a source vertex, the function runs depth first search looking for chains which are vertices
    with the same colour that are directly connected. It runs depth first search on a chain until there is nothing
    else to add to the chain. Rather than returning anything, it adds to the global variables that are visited,
    current_chain and captured_chain_check.

    visited: keeps track of all vertices that are visited by DFS at some point
    current_chain: keeps track of the current group of vertices that make up a chain.
    captured_chain_check: a bool variable that checks whether the chain is captured or free. The chain will be free
                          if any member of the chain is next to an empty vertex

    Time Complexity: O(V + E) where V is the number of vertices in the input graph and E is the number of edges in the
                     input graph
    """
    # If vertex has been visited, don't run DFS again
    if visited[vertex_ID] == 1:
        return
    visited[vertex_ID] = 1
    # determines the colour of the vertex by referring to the vertex properties
    colour = graph.vertex_properties[vertex_ID]
    # if the vertex is empty then it cannot be part of a chain
    if colour == 0:
        return
    # a variable just to check if the chain is captured or free
    empty_vertex_neighbour = False

    stack = deque()
    # Checks all the neighbours of the current vertex
    for edge in graph.edge_list[vertex_ID]:
        # if any of the neighbours are empty then the chain is not captured
        if graph.vertex_properties[edge] == 0:
            empty_vertex_neighbour = True
        # if the neighbour is the same colour it is part of the same chain. It is added to the stack as part of the
        # implementation of depth first search
        if graph.vertex_properties[edge] == colour:
            stack.append(edge)

    # if there is no empty vertex neighbour (so chain is still captured), it appends the current vertex to the list
    # storing the chain. Else it stores a marker saying the chain is free
    if not empty_vertex_neighbour:
        current_chain.append(vertex_ID)
    else:
        captured_chain_check.append('X')

    # It continues to call DFS as long as there are still vertices in the chain that have not been checked
    while len(stack) != 0:
        next_vertex = stack.pop()
        DFS(graph, next_vertex)


def terrain_pathfinding(vfile, efile, crossing_time, transform_cost, start, end):
    """ Given the vertices, edges, crossing time for each land type, the time it takes to transform, a start vertex
    and an end vertex, the function determines the optimal time taken to reach the end vertex from the start vertex
    and also returns the path taken

    Time Complexity: O(E * logV) where E is the number of edges in efile and v is the number of vertices in vfile
    """
    # no path or time needs to be taken if start == end
    if start == end:
        return (0, [])
    # Calls the Graph class to create the graph from vfile and efile
    graph = Graph(vfile, efile)

    # Creates a priority queue
    pqueue = queue.PriorityQueue()
    # Each vertex is split into 3 subvertices. distance_to_vertex[i][0] is the distance to the wheel subvertex on the
    # ith vertex, [i][1] is tank and [i][2] is hover
    # O(V)
    distance_to_vertex = [[inf, inf, inf] for _ in range(len(graph.vertex_properties))]
    # Starts in wheel form so to be at the start in wheel form is 0 while being at the start in hover or tank form
    # will be the transform cost
    distance_to_vertex[start] = [0, transform_cost, transform_cost]
    # O(V)
    # This will store the time taken to traverse through the vertex in each of the 3 forms
    distance_through_vertex = [[inf, inf, inf] for _ in range(len(graph.vertex_properties))]

    # O(V)
    visited = [[0,0,0] for _ in range(len(graph.vertex_properties))]
    # O(V)
    # This keeps track of what vertex and vehicle type (subvertex) is used to reach any vertex in each of its vehicle
    # types. This stores specifically the vertex and vehicle type just before in the shortest path.
    pred = [[(None, None),(None, None),(None, None)] for _ in range(len(graph.vertex_properties))]
    pred[start] = [(0, 0), (0,0), (0,0)]

    # Saves the time required to travel through each vertex in each vehicle type (subvertex)
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
    # O(V)
    for i in range(len(distance_to_vertex)):
        for j in range(len(distance_through_vertex[0])):
            pqueue.put((distance_to_vertex[i][j], i, j))

    # It runs through the priority queue until there is a path to reach the end vertex. The first path to the end vertex
    # will be the shortest path
    while not pqueue.empty() and visited[end] == [0,0,0]:
        # (distance to get to vertex in a certain vehicle type, the vertex ID, the vehicle type at the beginning of
        # iteration at the vertex)
        curr_distance_to, curr_vertex_ID, subvertex = pqueue.get()
        # If vertex has already been visited, ignore it. After it has been visited, the distance is locked in
        if visited[curr_vertex_ID][subvertex] == 1:
            continue
        # if vertex has been updated after this version was pushed onto the priority queue then ignore it
        if curr_distance_to != distance_to_vertex[curr_vertex_ID][subvertex]:
            continue
        visited[curr_vertex_ID][subvertex] = 1

        # Keeps track of what vertices were changed and therefore have to be added into the priority queue again
        relaxed_vertices = []
        edge_index_in_relax_vertices = -1
        # Runs through all the neighbours of the current vertex that has been popped off the priority queue
        for edge_destination in graph.edge_list[curr_vertex_ID]:
            edge_index_in_relax_vertices += 1

            # bitlist to check if any of the subvertices have been relaxed
            relaxed_vertices.append([edge_destination, 0, 0, 0])

            # From the vehicle type which is represented through subvertex, the following code determines the distance
            # to traverse through the current vertex in the vehicle type and reach the neighbouring vertex in a specific
            # vehicle type.
            # e.g. Current vertex ID = 3, subvertex = 0, neighbouring vertex ID = 4. The following code will determine
            # how long it takes to get to vertex 4 in wheel form and finish in wheel form, how long it takes to reach
            # vertex 4 in wheel form and finish in tank form (so has to transform once it reaches 4) and the same for
            # hover form.

            # To compute the distance, it looks at the distance to reach the current vertex in the vehicle form
            # (subvertex), how long it takes to traverse the current vertex in the form and then adds the transform cost
            # if the destination subvertex vehicle form is different to current vehicle form

            if subvertex == 0:

                # if the subvertex has already been finalised by being visited, it cannot be relaxed
                if visited[edge_destination][0] == 0:
                    travel_through_current_vertex_to_next = distance_through_vertex[curr_vertex_ID][0] + \
                                                            distance_to_vertex[curr_vertex_ID][0]
                    # If travelling through current vertex is a shorter path than previous path to next vertex then
                    # relax by updating distance, pred list and relaxed_vertices list
                    if travel_through_current_vertex_to_next < distance_to_vertex[edge_destination][0]:
                        distance_to_vertex[edge_destination][0] = travel_through_current_vertex_to_next
                        pred[edge_destination][0] = (curr_vertex_ID, 0)
                        relaxed_vertices[edge_index_in_relax_vertices][1] = 1

                if visited[edge_destination][1] == 0:
                    # If the destination is the end then it does not need to transform. Otherwise it should transform
                    # once reaching destination vertex
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

        # If vertexes have been relaxed, repush them into the pqueue
        for i in range(edge_index_in_relax_vertices+1):
            for j in range(1, 4):
                if relaxed_vertices[i][j] == 1:
                    # O(logV)
                    # Push (distance to subvertex, vertex_id, subvertex_id) onto priority queue
                    pqueue.put((distance_to_vertex[relaxed_vertices[i][0]][j-1], relaxed_vertices[i][0], j-1))

    # Determines which vehicle type (subvertex) has the shortest path to reach the end vertex
    min_distance_index = 0
    for x in range(1, len(distance_to_vertex[end])):
        if distance_to_vertex[end][x] < distance_to_vertex[end][min_distance_index]:
            min_distance_index = x

    # res stores the shortest distance to reach the end vertex and then a list of tuples showing the path taken to reach
    # the end vertex in the shortest path
    res = [distance_to_vertex[end][min_distance_index], []]

    # Stores the path back to front which will be reversed later
    res_temp = []
    # Converts subvertex IDs into string representing the vehicle type
    str = index_to_vehicle_type(pred[end][min_distance_index][1])
    res_temp.append((end, str))

    # pred_vertex is the subvertex directly before the current subvertex in the path
    pred_vertex = pred[end][min_distance_index]

    # While loop goes backwards from the end vertex until it reaches the start vertex and appends the path to res_temp
    # continues until the start vertex has been appended
    while res_temp[-1][0] != start:
        curr_vertex_ID, subvertex = pred_vertex
        vehicle_type = index_to_vehicle_type(subvertex)
        res_temp.append((curr_vertex_ID, vehicle_type))
        pred_vertex = pred[curr_vertex_ID][subvertex]

    # res_temp is in reverse order so this appends the path in the correct order to res to be returned
    for i in range(len(res_temp)-1, -1, -1):
        res[1].append(res_temp[i])
    return res


def index_to_vehicle_type(index):
    """ Given a subvertex index, it returns the string that represents the vehicle form for that subvertex

    Time Complexity: O(1)
    """
    if index == 0:
        return "wheel"
    if index == 1:
        return "tank"
    if index == 2:
        return "hover"


