from overpass import get_path
from graph import Graph
from point import Point
from segment import Segment
from generate_GPX import generate_GPX
from loop import create_loop
from srtm import get_tile
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
dict_id_point = {}

filename = get_tile(center)

with rasterio.open(f"loopfeature/data/{filename}") as tiff_file:
    band = tiff_file.read(1)

    for path in list_path:
        
        elevation_gain_FtoL = 0
        elevation_gain_LtoF = 0
        total_dist = 0

        x,y = tiff_file.index(path["geometry"][0]["lon"], path["geometry"][0]["lat"])
        elevation = band[x, y]
        first_point = Point(round(path["geometry"][0]["lat"], 5), round(path["geometry"][0]["lon"], 5), path["nodes"][0], elevation)
        list_points = [first_point]

        current_segment = Segment(0, path["id"], first_point, None, 0, 0, 0, False)

        for i in range(1, len(path["geometry"])):

            lat = round(path["geometry"][i]["lat"], 5)
            lon = round(path["geometry"][i]["lon"], 5)
            
            x,y = tiff_file.index(lon, lat)
            elevation = band[x, y]

            current_point = Point(lat, lon, path["nodes"][i], elevation)

            dict_id_point[path["nodes"][i]] = dict_id_point.get(path["nodes"][i], []) + [current_segment]

            if (round(center[0], 3), round(center[1], 3)) == (round(path["geometry"][i]["lat"], 3), round(path["geometry"][i]["lon"], 3)) and not start:
                start = current_point

            list_points.append(current_point)

            diff_elevation = elevation - list_points[i-1].elevation
            if diff_elevation >= 0:
                elevation_gain_FtoL += diff_elevation
            else:
                elevation_gain_LtoF -= diff_elevation

            total_dist += list_points[i-1].calcul_dist(current_point)

        current_segment.last_point = current_point
        current_segment.distance = total_dist
        current_segment.elev_gain_FtoL = elevation_gain_FtoL
        current_segment.elev_gain_LtoF = elevation_gain_LtoF

        path_params = path["tags"]

        score = 0.3*(len(path["geometry"])**1.5)
        if path_params.get("highway") == "residential":
            score -= 200
        if path_params.get("surface") == "aslphat":
            score -= 150
        if path_params.get("highway") == "tertiary":
            score -= 200
        if path_params.get("surface") == "dirt":
            score += 200
        if path_params.get("highway") == "path":
            score += 100
        if path_params.get("highway") == "footway":
            score += 100
        if path_params.get("highway") == "service":
            score -= 100
            current_segment.is_service = True

        current_segment.score = score
        
        graphe.add_elements(list_points, other_params=current_segment)

        dict_id_point[path["nodes"][0]] = dict_id_point.get(path["nodes"][0], []) + [current_segment]

loop_path = create_loop(graphe, start, distance, dict_id_point)

generate_GPX(loop_path[0])