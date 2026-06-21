import requests
import math

url = "https://overpass-api.de/api/interpreter"

def get_path(center:tuple[float, float], total_distance:float)->dict:
    radius = int(0.25*total_distance)
    overpass_request = f"""
    [out:json][timeout:20];
    (
        way["highway"](around:{radius}, {center[0]}, {center[1]});
        -
        way["highway"~"primary|service"](around:{radius}, {center[0]}, {center[1]});
    );
    out geom;"""

    response = requests.post(url, 
                             data=overpass_request, 
                             headers={
                                "Content-Type": "text/plain",
                                "User-Agent": "LoopFeature"
                                },
                            timeout=60)
    if response.status_code == 200:
        data = response.json()
        return data["elements"]
    else:
        return False
    
def calcul_dist(point1:tuple[int, int], point2:tuple[int, int])->float:
    midlat = (point1[0] + point2[0])/2
    dy = (point1[0] - point2[0]) * 110540
    dx = (point1[1] - point2[1]) * 111320 * math.cos(math.radians(midlat))

    return math.sqrt(dx**2 + dy**2)