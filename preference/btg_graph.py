# -*- coding: utf-8 -*-
'''
Module to build preference graphs

This graphs are used in theory consistency tests
'''

import copy


class BTG_Graph(object):
    '''
    Better Than Graph (BTG) Graph

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

        # hash dictionaries the lazy way
        # from_vertex=str(from_vertex)

        if to_vertex is not None:
            # to_vertex  =str(to_vertex)

            if from_vertex not in self._graph_dict:
                self._graph_dict[from_vertex] = []
            if to_vertex not in self._graph_dict:
                self._graph_dict[to_vertex] = []
            if to_vertex not in self._graph_dict[from_vertex]:
                self._graph_dict[from_vertex].append(to_vertex)
        else:
            if from_vertex not in self._graph_dict:
                self._graph_dict[from_vertex] = []

    def get_top_vertex(self):
        nodes = set()

        for index_node in self._graph_dict:
            nodes.add(index_node)

        for index_node in self._graph_dict:
            for node in self._graph_dict[index_node]:
                if node in nodes:
                    nodes.remove(node)

        return nodes

    def graph_to_preference_list(self):

        # make a copy of the graph
        graph = copy.deepcopy(self)

        preference_list = []
        top_nodes = graph.get_top_vertex()

        while len(top_nodes) > 0:
            preference_list.append(top_nodes)

            # remove edges from graph
            for node in top_nodes:
                graph._graph_dict.pop(node)

            # get next level of nodes
            top_nodes = graph.get_top_vertex()

        return preference_list
