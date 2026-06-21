from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    longitude:float
    latitude:float