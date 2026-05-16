from overpass import get_path
from dijkstra import dijkstra
from graphe_manage import create_graphe, create_loop
import time

list_path = False

while not list_path:
    list_path = get_path()
    time.sleep(0.01)

graphe = create_graphe(list_path)

start = list(graphe.keys())[0]
shortly_distance = dijkstra(graphe, start)

with open("dijkstra.txt", "w") as f:
    f.write(str(shortly_distance))
with open("graphe.txt", "w") as f:
    f.write(str(graphe))

loop_path = create_loop(start, shortly_distance, graphe, 1000)

print(loop_path[1])

with open("path.txt", "w") as f:
    f.write(str(loop_path[0]))