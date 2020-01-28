#!/usr/bin/env python
# coding: utf-8

# In[1]:


from queue import heappop, heappush
from math import inf
from collections import deque


# In[2]:


class Graph:
    def __init__(self, directed=True):
        self.edges = {}
        self.directed = directed

    def add_edge(self, node1, node2, cost = 1, __reversed=False):
        try: neighbors = self.edges[node1]
        except KeyError: neighbors = {}
        neighbors[node2] = cost
        self.edges[node1] = neighbors
        if not self.directed and not __reversed: self.add_edge(node2, node1, cost, True)

    def neighbors(self, node):
        try: return self.edges[node]
        except KeyError: return []

    def cost(self, node1, node2):
        try: return self.edges[node1][node2]
        except: return inf

    def breadth_first_search(self, start, goal):
        found, fringe, visited, came_from = False, deque([start]), set([start]), {start: None}
        print('{:15s} | {}'.format('Expand Node', 'Fringe'))
        print('-------------------------')
        print('{:15s} | {}'.format('-', start))
        while not found and len(fringe):
            current = fringe.pop()
            print('{:15s}'.format(current), end=' | ')
            if current == goal: found = True; break
            for node in self.neighbors(current):
                if node not in visited: visited.add(node); fringe.appendleft(node); came_from[node] = current
            print(', '.join(fringe))
        if found: print(); return came_from
        else: print('No path from {} to {}'.format(start, goal))
    
    def depth_limited_search(self, start, goal, limit=-1):
        print('Depth limit =', limit)
        found, fringe, visited, came_from = False, deque([(0, start)]), set([start]), {start: None}
        print('{:15s} | {}'.format('Expand Node', 'Fringe'))
        print('-------------------------')
        print('{:15s} | {}'.format('-', start))
        while not found and len(fringe):
            depth, current = fringe.pop()
            print('{:15s}'.format(current), end=' | ')
            if current == goal: found = True; break
            if limit == -1 or depth < limit:
                for node in self.neighbors(current):
                    if node not in visited:
                        visited.add(node); fringe.append((depth + 1, node))
                        came_from[node] = current
            print(', '.join([n for _, n in fringe]))
        if found: print(); return came_from
        else: print('No path from {} to {}'.format(start, goal))

    def uniform_cost_search(self, start, goal):
        found, fringe, visited, came_from, cost_so_far = False, [(0, start)], set([start]), {start: None}, {start: 0}
        print('{:15s} | {}'.format('Expand Node', 'Fringe'))
        print('-------------------------')
        print('{:15s} | {}'.format('-', str((0, start))))
        while not found and len(fringe):
            _, current = heappop(fringe)
            print('{:15s}'.format(current), end=' | ')
            if current == goal: found = True; break
            for node in self.neighbors(current):
                new_cost = cost_so_far[current] + self.cost(current, node)
                if node not in visited or cost_so_far[node] > new_cost:
                    visited.add(node); came_from[node] = current; cost_so_far[node] = new_cost
                    heappush(fringe, (new_cost, node))
            print(', '.join([str(n) for n in fringe]))
        if found: print(); return came_from, cost_so_far[goal]
        else: print('No path from {} to {}'.format(start, goal)); return None, inf

    @staticmethod
    def print_path(came_from, goal):
        parent = came_from[goal]
        if parent:
            Graph.print_path(came_from, parent)
        else: print(goal, end='');return
        print(' =>', goal, end='')


    def __str__(self):
        return str(self.edges)


# In[3]:


graph = Graph(directed=True)
graph.add_edge('Arad', 'Zerind', 75)
graph.add_edge('Arad', 'Timisoara', 118)
graph.add_edge('Arad', 'Sibiu', 140)
graph.add_edge('Zerind', 'Oradea', 71)
graph.add_edge('Zerind', 'Arad', 75)
graph.add_edge('Timisoara', 'Arad', 118)
graph.add_edge('Timisoara', 'Lugoj', 111)
graph.add_edge('Sibiu', 'Arad', 140)
graph.add_edge('Sibiu', 'Oradea', 151)
graph.add_edge('Sibiu', 'Fagaras', 99)
graph.add_edge('Sibiu', 'RimnicuVilcea', 80)
graph.add_edge('Oradea', 'Zerind', 71)
graph.add_edge('Oradea', 'Sibiu', 151)
graph.add_edge('Lugoj', 'Timisoara', 111)
graph.add_edge('Lugoj', 'Mehadia', 70)
graph.add_edge('RimnicuVilcea', 'Sibiu', 80)
graph.add_edge('RimnicuVilcea', 'Pitesti', 97)
graph.add_edge('RimnicuVilcea', 'Craiova', 146)
graph.add_edge('Mehadia', 'Lugoj', 70)
graph.add_edge('Mehadia','Dobreta', 75)
graph.add_edge('Craiova', 'Dobreta', 120)
graph.add_edge('Craiova', 'RimnicuVilcea', 146)
graph.add_edge('Craiova', 'Pitesti', 138)
graph.add_edge('Pitesti', 'RimnicuVilcea', 97)
graph.add_edge('Pitesti', 'Craiova', 138)
graph.add_edge('Pitesti', 'Bucharest', 101)
graph.add_edge('Fagaras', 'Sibiu', 99)
graph.add_edge('Fagaras', 'Bucharest', 211)
graph.add_edge('Dobreta', 'Mehadia', 75)
graph.add_edge('Dobreta', 'Craiova', 120)
graph.add_edge('Bucharest', 'Fagaras', 211)
graph.add_edge('Bucharest', 'Pitesti', 101)
graph.add_edge('Bucharest', 'Giurgiu', 90)
graph.add_edge('Giurgiu', 'Bucharest',9)

print(graph)


# In[4]:


start, goal, l = 'Arad', 'Bucharest', 5
print('Breadth First Search'); print('-------------------------'); 
bfs_path = graph.breadth_first_search(start, goal)
if (bfs_path): print('Path:', end=' '); Graph.print_path(bfs_path, goal); print();print()
print('Depth Limited Search'); print('-------------------------'); 
dlm_path = graph.depth_limited_search(start, goal, l)
if (dlm_path): print('Path:', end=' '); Graph.print_path(dlm_path, goal); print();print()
print('Uniform Cost Search'); print('-------------------------'); 
ucs_path, cost = graph.uniform_cost_search(start, goal)
if (ucs_path): print('Path:', end=' '); Graph.print_path(ucs_path, goal); print('\nCost:', cost)

