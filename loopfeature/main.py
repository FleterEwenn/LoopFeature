from overpass import get_path
from dijkstra import dijkstra
from graphe_manage import create_graphe, create_loop
from generate_GPX import generate_GPX
import time

list_path = False
print("Veuillez entrez les coordonnées du point de départ")
lat_center = input("latitude : ")
long_center = input("longitude : ")

center = (float(lat_center), float(long_center))

distance = float(input("Entrez la distance à courir (en km) : "))
distance = distance * 1000

while not list_path:
    list_path = get_path(center, distance)
    time.sleep(0.1)

graphe = create_graphe(list_path)

for point in graphe:
    if (round(center[0], 3), round(center[1], 3)) == (round(point[0], 3), round(point[1], 3)):
        start = point

shortly_distance = dijkstra(graphe, start)

with open("graphe.txt", "w") as f:
    f.write(str(graphe))

loop_path = create_loop(start, shortly_distance, graphe, distance)

print(loop_path[1])

generate_GPX(loop_path[0])