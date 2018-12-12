# -*- coding: utf-8 -*-
'''
Module to build preference graphs

This graphs are used in theory consistency tests
'''
from preference.interval import intersect


class PreferenceGraph(object):
    '''
    Preference Graph

    Its main function is test of acyclic
    '''

    # Dictionary do store vertex and edges
    _graph_dict = {}

    def __init__(self):
        '''
        Initializes a graph object
        '''
        # Dictionary to store vertices and edges
        self._graph_dict = {}

    def __str__(self):
        return str(self._graph_dict)

    def __repr__(self):
        return self.__str__()

    def __del__(self):
        self._graph_dict.clear()
        del self._graph_dict

    def add_edge(self, from_vertex, to_vertex):
        '''
        Add an edge from 'from_vertex' to 'to_vertex'

        If vertices don't exist, they will be created
        '''
        if from_vertex not in self._graph_dict:
            self._graph_dict[from_vertex] = []
        if to_vertex not in self._graph_dict:
            self._graph_dict[to_vertex] = []
        if to_vertex not in self._graph_dict[from_vertex]:
            self._graph_dict[from_vertex].append(to_vertex)

    def depth_first_search(self, start_vertex, goal_vertex):
        '''
        Depth first search on graph

        The search start at 'star_vertex' and try reach at 'goal_vertex'
        '''
        # Visited vertex
        visited_list = [start_vertex]
        # Next vertices to be visited_list
        waiting_list = self._graph_dict[start_vertex]
        # While there is vertex to be visited
        while waiting_list != []:
            # Get next vertex
            next_vertex = waiting_list.pop()
            # Check if 'goal_vertex' was reached
            if intersect(goal_vertex, next_vertex):
                return True
            # Check if 'next_vertex' was be visited
            if next_vertex not in visited_list:
                # Add 'next_vertex' to 'visited_list'
                visited_list.append(next_vertex)
                # Next vertices to be visited
                waiting_list += self._graph_dict[next_vertex]
        # Return false if 'goal_vertex' was not reached
        return False

    def is_acyclic(self):
        '''
        Check if the graph is acyclic
        '''
        # Call depth first search form each vertex to itself
        for vertex in self._graph_dict:
            if self.depth_first_search(vertex, vertex):
                return False
        return True

    def update_intersections(self):
        '''
        Update interval intersections
        '''
        # For every vertex ve1
        for ve1 in self._graph_dict:
            # New list of vertex do create edges from ve1
            new_list = []
            # For every vertex ve2 in edges ve1 -> ve2
            for ve2 in self._graph_dict[ve1]:
                # For every vertex ve3
                for ve3 in self._graph_dict:
                    # Check if ve2 is different of ve3
                    # And if there is intersection in their intervals
                    if ve2 != ve3 and intersect(ve2, ve3):
                        new_list.append(ve3)
            # Create edges from ve1 to vetices in new list
            self._graph_dict[ve1] += new_list
