from overpass import get_path, calculer_dist
import time
import random

list_path = False

while not list_path:
    list_path = get_path()
    time.sleep(0.01)

graphe = {}
for path in list_path:
    list_point = [(pt["lat"], pt["lon"]) for pt in path["geometry"]]

    for i in range(1, len(list_point)):
        point1 = (round(list_point[i-1][0], 5), round(list_point[i-1][1], 5))
        point2 = (round(list_point[i][0], 5), round(list_point[i][1], 5))
        dist = calculer_dist(point1, point2)
        graphe[point1] = graphe.get(point1, []) + [(point2, dist)]
        graphe[point2] = graphe.get(point2, []) + [(point1, dist)]

start = list(graphe.keys())[0]
dijkstra = {}
for n in graphe:
    dijkstra[n] = (float("inf"), None)

dijkstra[start] = (0, start)

file = [(0, start)]

while len(file) > 0:
    current_dist, current_node = file.pop(0)

    if not current_dist > dijkstra[current_node][0]:

        for neighbor, neighbor_dist in graphe[current_node]:
            new_dist = current_dist + neighbor_dist
            if new_dist < dijkstra[neighbor][0]:
                dijkstra[neighbor] = (new_dist, current_node)

                file.append((new_dist, neighbor))

with open("dijkstra.txt", "w") as f:
    f.write(str(dijkstra))
with open("graphe.txt", "w") as f:
    f.write(str(graphe))

max = 5000
dist = 0
point = start
passed = [start]

while dist + dijkstra[point][0] < max:
    point, curr_dist = graphe[point][random.randint(0, len(graphe[point])-1)]
    dist += current_dist
    passed.append(point)

while dijkstra[point][0] != start:
    curr_dist, point = dijkstra[point]
    dist += curr_dist
    passed.append(point)

print(dist)
print(passed)