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

                for neighbor, neighbor_weight, _ in self.get_neighbors(current_node):

                    new_weight = current_weight + neighbor_weight
                    if new_weight < self.__dijkstra[neighbor][0]:
                        self.__dijkstra[neighbor] = (new_weight, current_node)

                        file.append((new_weight, neighbor))
    
    def add_elements(self, elements_list:list, other_params=None):
        for i in range(1, len(elements_list)):
            weight = self.__weight_function(elements_list[i], elements_list[i-1])
            self.graph[elements_list[i]] = self.graph.get(elements_list[i], []) + [(elements_list[i-1], weight, other_params)]
            self.graph[elements_list[i-1]] = self.graph.get(elements_list[i-1], []) + [(elements_list[i], weight, other_params)]