from overpass import get_path
from graph import Graph
from point import Point
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

start = None

graphe = Graph(Point.calcul_dist)
for path in list_path:
    list_points = []
    for point in path["geometry"]:

        if (round(center[0], 3), round(center[1], 3)) == (round(point["lat"], 3), round(point["lon"], 3)) and not start:
            start = Point(round(point["lat"], 5), round(point["lon"], 5))

        list_points.append(Point(round(point["lat"], 5), round( point["lon"], 5)))
    graphe.add_elements(list_points)

with open("graphe.txt", "w") as f:
    f.write(str(graphe.graph))

loop_path = graphe.create_loop(start, distance)
print(loop_path[0])

print(loop_path[1])

generate_GPX(loop_path[0])