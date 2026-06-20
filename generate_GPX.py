import requests

def generate_GPX(point_list:list[float, float]):
    text_GPX = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="LoopFeature" xmlns="http://www.topografix.com/GPX/1/1">
<trk>
<trkseg>"""
    
    for point in point_list:
        request_srtm = f"https://api.open-elevation.com/api/v1/lookup?locations={point[0]},{point[1]}"
        response = requests.get(request_srtm)
        elevation = response.json()["results"][0]["elevation"]
        text_GPX += f'<trkpt lat="{point[0]}" lon="{point[1]}"><ele>{elevation}</ele></trkpt>\n'

    text_GPX += "</trkseg>\n</trk>\n</gpx>\n"
    
    with open("trace.gpx", "w") as file:
        file.write(text_GPX)