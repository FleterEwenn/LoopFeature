from overpass import calcul_dist
import random

def create_graphe(list_path:list[dict])->dict:
    graphe = {}
    for path in list_path:
        list_point = [(pt["lat"], pt["lon"]) for pt in path["geometry"]]

    for i in range(1, len(list_point)):
        point1 = (round(list_point[i-1][0], 5), round(list_point[i-1][1], 5))
        point2 = (round(list_point[i][0], 5), round(list_point[i][1], 5))
        dist = calcul_dist(point1, point2)
        graphe[point1] = graphe.get(point1, []) + [(point2, dist)]
        graphe[point2] = graphe.get(point2, []) + [(point1, dist)]
    
    return graphe

def create_loop(start:tuple, shortly_distance:dict, graphe:dict)->tuple[list, int]:
    max = 3000
    dist = 0
    point = start
    passed = [start]

    while dist + shortly_distance[point][0] < max:
        point, curr_dist = graphe[point][random.randint(0, len(graphe[point])-1)]
        dist += curr_dist
        passed.append(point)

    dist += shortly_distance[point][0]

    while point != start:
        point = shortly_distance[point][1]
        passed.append(point)
    
    return passed, dist
