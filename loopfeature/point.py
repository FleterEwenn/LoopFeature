from dataclasses import dataclass
import math

@dataclass(frozen=True)
class Point:
    latitude:float
    longitude:float
    segment_id:int
    elevation:float

    def calcul_dist(self, point2)->float:
        midlat = (self.latitude + point2.latitude)/2
        dy = (self.latitude - point2.latitude) * 110540
        dx = (self.longitude - point2.longitude) * 111320 * math.cos(math.radians(midlat))

        return math.sqrt(dx**2 + dy**2)