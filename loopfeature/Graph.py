import random

class Graph:
    def __init__(self, weight_function):
        self.graph = {}        
        self.__dijkstra = {}
        self.__weight_function = weight_function
        
    def get_neighbors(self, node)->list:
        return self.graph[node]
    
    def get_shortest_path(self, node)->tuple:
        return self.__dijkstra[node]

    def construct_dijkstra(self, start):
        self.__dijkstra = {n:(float("inf"), None) for n in self.graph}

        self.__dijkstra[start] = (0, start)

        file = [(0, start)]

        while len(file) > 0:
            current_weight, current_node = file.pop(0)

            if not current_weight > self.__dijkstra[current_node][0]:

                for neighbor, neighbor_weight in self.get_neighbors(current_node):

                    new_weight = current_weight + neighbor_weight
                    if new_weight < self.__dijkstra[neighbor][0]:
                        self.__dijkstra[neighbor] = (new_weight, current_node)

                        file.append((new_weight, neighbor))
        
    def create_loop(self, start, dist_max:float):
        self.construct_dijkstra(start)
        
        node = start
        passed = [start]
        dist = 0

        while dist + self.get_shortest_path(node)[0] < dist_max:
            if len(self.get_neighbors(node)) > 2:
                list_available_node = [p for p in self.get_neighbors(node)]
            elif len(self.get_neighbors(node)) > 1:
                list_available_node = [p for p in self.get_neighbors(node)]
            else:
                list_available_node = self.get_neighbors(node)

            random.shuffle(list_available_node)
            node, curr_dist = random.choice(list_available_node)

            dist += curr_dist
            passed.append(node)

        dist += self.get_shortest_path(node)[0]

        while node != start:
            node = self.get_shortest_path(node)[1]
            passed.append(node)
        
        return passed, dist
    
    def add_elements(self, elements_list:list):
        for i in range(1, len(elements_list)):
            weight = self.__weight_function(elements_list[i], elements_list[i-1])
            self.graph[elements_list[i]] = self.graph.get(elements_list[i], []) + [(elements_list[i-1], weight)]
            self.graph[elements_list[i-1]] = self.graph.get(elements_list[i-1], []) + [(elements_list[i], weight)]