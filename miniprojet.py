import requests
import srtm
import math

data_dplus = srtm.get_data()
# 45.0188355, 1.7942439
overpass_request = """
[out:json][timeout:25];
way["highway"~"path|footway|track"](around:2000, 45.0320272, 1.8060011);
out geom;"""

url = "https://overpass.kumi.systems/api/interpreter"

response = requests.get(url, data=overpass_request)
print(response.status_code)
print()
data_overpass = response.json()
list_path = data_overpass["elements"]
max_ratio = (0, None, None, None)
max_dplus = (None, 0, None, None)
max_dist = (None, None, 0, None)

for path in list_path:
    list_points = []

    for point in path["geometry"]:
        list_points.append((point["lat"], point["lon"]))

    dplus_total = 0
    dist_total = 0

    for i in range(1, len(list_points)):
        diff = data_dplus.get_elevation(list_points[i][0], list_points[i][1]) - data_dplus.get_elevation(list_points[i-1][0], list_points[i-1][1])

        if diff > 0:
            dplus_total += diff

        midlat = (list_points[i][0] + list_points[i-1][0])/2
        dy = (list_points[i][0] - list_points[i-1][0]) * 110540
        dx = (list_points[i][1] - list_points[i-1][1]) * 111320 * math.cos(math.radians(midlat))

        dist_total += math.sqrt(dx**2 + dy**2)
    
    ratio = dplus_total / dist_total

    if ratio > max_ratio[0]:
        max_ratio = (ratio, dplus_total, dist_total, path["id"])
    if dplus_total > max_dplus[1]:
        max_dplus = (ratio, dplus_total, dist_total, path["id"])
    if dist_total > max_dist[2]:
        max_dist = (ratio, dplus_total, dist_total, path["id"])

print("le meilleur ratio :")
print(max_ratio)
print("le plus grand D+ :")
print(max_dplus)
print("la plus grande distance :")
print(max_dist)