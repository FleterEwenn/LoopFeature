from point import Point

class Graph:
    def __init__(self, list_path:list):
        self.graph = {}

        for path in list_path:
            list_point = [Point(round(point["lat"], 5), round(point["long"], 5)) for point in path["geometry"]]

            for i in range(1, len(list_point)):
                self.graph[list_point[i]] = self.graph.get(list_point[i], []) + [list_point[i-1]]
                self.graph[list_point[i-1]] = self.graph.get(list_point[i-1], []) + [list_point[i]]
        
        self.dijkstra = {n:(float("inf"), None) for n in self.graph}
        
    def get_neighbors(self, point:Point)->list[(Point, float)]:
        return self.graph[point]
    
    def get_shortest_path(self, point:Point)->tuple[Point, float]:
        return self.dijkstra[point]

    def construct_dijkstra(self, start:Point):

        self.dijkstra[start] = (0, start)

        file = [(0, start)]

        while len(file) > 0:
            current_dist, current_node = file.pop(0)

            if not current_dist > self.dijkstra[current_node][0]:

                for neighbor, neighbor_dist in self.get_neighbors(current_node):
                    new_dist = current_dist + neighbor_dist
                    
                    if new_dist < self.dijkstra[neighbor][0]:
                        self.dijkstra[neighbor] = (new_dist, current_node)

                        file.append((new_dist, neighbor))