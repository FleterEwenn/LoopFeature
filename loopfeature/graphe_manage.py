from overpass import calcul_dist
import random

def create_graphe(list_path:list[dict])->dict:
    graphe = {}
    list_point = []
    for path in list_path:
        list_point = [(pt["lat"], pt["lon"]) for pt in path["geometry"]]

        for i in range(1, len(list_point)):
            point1 = (round(list_point[i-1][0], 5), round(list_point[i-1][1], 5))
            point2 = (round(list_point[i][0], 5), round(list_point[i][1], 5))
            dist = calcul_dist(point1, point2)
            graphe[point1] = graphe.get(point1, []) + [(point2, dist)]
            graphe[point2] = graphe.get(point2, []) + [(point1, dist)]
    
    return graphe

def create_loop(start:tuple, shortly_distance:dict, graphe:dict, distance_wanted:int)->tuple[list, int]:
    max = distance_wanted
    dist = 0
    point = start
    passed = [start]

    while dist + shortly_distance[point][0] < max:
        if len(graphe[point]) > 2:
            list_available_point = [p for p in graphe[point] if p[0] not in passed[-3:]] + [p for p in graphe[point] if p[0] not in passed]
        elif len(graphe[point]) > 1:
            list_available_point = [p for p in graphe[point] if p[0] not in passed[-2:]] + [p for p in graphe[point] if p[0] not in passed]
        else:
            list_available_point = graphe[point]
        random.shuffle(list_available_point)
        point, curr_dist = random.choice(list_available_point)

        dist += curr_dist
        passed.append(point)

    dist += shortly_distance[point][0]

    while point != start:
        point = shortly_distance[point][1]
        passed.append(point)
    
    return passed, dist
