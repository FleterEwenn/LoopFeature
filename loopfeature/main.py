from overpass import get_path
from graph import Graph
from point import Point
from segment import Segment
from generate_GPX import generate_GPX
import time
import rasterio

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
with rasterio.open("loopfeature/data/france.tif") as tiff_file:
    band = tiff_file.read(1)
    for path in list_path:
        
        elevation_gain = 0
        x,y = tiff_file.index(path["geometry"][0]["longitude"], path["geometry"][0]["latitude"])
        past_elevation = band[x, y]

        total_dist = 0
        past_Point = Point(path["geometry"][0]["latitude"], path["geometry"][0]["longitude"], path["id"], past_elevation)

        list_points = []
        for point in path["geometry"]:
            lat = round(point["lat"], 5)
            lon = round(point["lon"], 5)
            
            x,y = tiff_file.index(lon, lat)
            elevation = band[x, y]

            if (round(center[0], 3), round(center[1], 3)) == (round(point["lat"], 3), round(point["lon"], 3)) and not start:
                start = Point(lat, lon, path["id"], elevation)

            list_points.append(Point(lat, lon, path["id"], elevation))

            elevation_gain += (past_elevation - elevation)
            past_elevation = elevation

            total_dist += past_Point.calcul_dist(point)
            past_Point = point

            ratio = elevation_gain/(total_dist/1000)

        graphe.add_elements(list_points)

loop_path = graphe.create_loop(start, distance)

generate_GPX(loop_path[0])