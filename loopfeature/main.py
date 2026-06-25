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

        x,y = tiff_file.index(path["geometry"][0]["lon"], path["geometry"][0]["lat"])
        elevation = band[x, y]

        total_dist = 0

        list_points = [Point(path["geometry"][0]["lat"], path["geometry"][0]["lon"], path["nodes"][0], elevation)]

        for i in range(1, len(path["geometry"])):

            lat = round(path["geometry"][i]["lat"], 5)
            lon = round(path["geometry"][i]["lon"], 5)
            
            x,y = tiff_file.index(lon, lat)
            elevation = band[x, y]

            current_point = Point(lat, lon, path["nodes"][i], elevation)

            if (round(center[0], 3), round(center[1], 3)) == (round(path["geometry"][i]["lat"], 3), round(path["geometry"][i]["lon"], 3)) and not start:
                start = current_point

            list_points.append(current_point)

            elevation_gain += (list_points[i-1].elevation - elevation)

            total_dist += list_points[i-1].calcul_dist(current_point)

        ratio = elevation_gain/(total_dist/1000)

        path_params = path["tags"]

        score = len(path["geometry"])
        if path_params.get("surface", None) == "aslphat":
            score -= 25
        if path_params.get("highway", None) == "tertiary":
            score -= 30
        if path_params.get("surface", None) == "dirt":
            score += 25
        if path_params.get("highway", None) == "path":
            score += 30
        if path_params.get("highway", None) == "footway":
            score += 25
        if path_params.get("highway", None) == "service":
            score -25
            
        score += 100/(abs(30-ratio)+1)
        
        graphe.add_elements(list_points)

loop_path = graphe.create_loop(start, distance)

generate_GPX(loop_path[0])