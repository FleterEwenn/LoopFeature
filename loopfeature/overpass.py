import requests

url = "https://overpass-api.de/api/interpreter"

def get_path(center:tuple[float, float], total_distance:float)->dict:
    radius = int(0.3*total_distance)
    overpass_request = f"""
    [out:json][timeout:20];
    (
        way["highway"](around:{radius}, {center[0]}, {center[1]});
        -
        way["highway"~"primary"](around:{radius}, {center[0]}, {center[1]});
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