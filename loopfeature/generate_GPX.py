import rasterio

def generate_GPX(point_list:list[float, float]):
    text_GPX = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="LoopFeature" xmlns="http://www.topografix.com/GPX/1/1">
<trk>
<trkseg>"""
    
    with rasterio.open("loopfeature/data/france.tif") as tiff_file:
        band = tiff_file.read(1)
        print(point_list)
        for point in point_list:
            print(point)
            x, y = tiff_file.index(point.longitude, point.latitude)
            elevation = band[x, y]
            text_GPX += f'<trkpt lat="{point.latitude}" lon="{point.longitude}"><ele>{elevation}</ele></trkpt>\n'

    text_GPX += "</trkseg>\n</trk>\n</gpx>\n"
    
    with open("trace.gpx", "w") as file:
        file.write(text_GPX)