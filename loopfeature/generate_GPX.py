import rasterio

def generate_GPX(point_list:list[float, float]):
    text_GPX = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="LoopFeature" xmlns="http://www.topografix.com/GPX/1/1">
<trk>
<trkseg>"""
    
    with rasterio.open("data/france.tif") as tiff_file:
        band = tiff_file.read(1)
        for point in point_list:
            x, y = tiff_file.index(point[1], point[0])
            elevation = band[x, y]
            text_GPX += f'<trkpt lat="{point[0]}" lon="{point[1]}"><ele>{elevation}</ele></trkpt>\n'

    text_GPX += "</trkseg>\n</trk>\n</gpx>\n"
    
    with open("trace.gpx", "w") as file:
        file.write(text_GPX)