def dijkstra(graphe:dict, start:tuple[int, int])-> dict:
    dijkstra_dict = {n:(float("inf"), None) for n in graphe}

    dijkstra_dict[start] = (0, start)

    file = [(0, start)]

    while len(file) > 0:
        current_dist, current_node = file.pop(0)

        if not current_dist > dijkstra_dict[current_node][0]:

            for neighbor, neighbor_dist in graphe[current_node]:
                new_dist = current_dist + neighbor_dist
                
                if new_dist < dijkstra_dict[neighbor][0]:
                    dijkstra_dict[neighbor] = (new_dist, current_node)

                    file.append((new_dist, neighbor))
    
    return dijkstra_dict