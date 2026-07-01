from graph import Graph
from point import Point
from segment import Segment

def create_loop(graph:Graph, start:Point, dist_max:float, dict_segment:dict[int, list[Segment]])->tuple[list[Point], float]:
        graph.construct_dijkstra(start)
        
        node = start
        passed = [start]
        total_dist = 0
        passed_edge = set()

        while total_dist + graph.get_shortest_path(node)[0] < dist_max:
            neighbors : list[tuple[Point, float, Segment]] = graph.get_neighbors(node)
            best_score = float("-inf")
            best_node = None
            best_dist = 0
            best_edge = None

            ditance_node_to_start = node.calcul_dist(start)

            for neighbor, curr_dist, segment in neighbors:
                real_cul_de_sac = segment.is_service and(len(graph.get_neighbors(segment.last_point)) <= 1 or len(graph.get_neighbors(segment.first_point)) <= 1)
                if real_cul_de_sac:
                    continue
                
                best_new_segment_score = float("-inf")
                for new_segment in dict_segment[neighbor.id]:
                    if new_segment.id != segment.id:
                        real_cul_de_sac = new_segment.is_service and (len(graph.get_neighbors(new_segment.last_point)) <= 1 or len(graph.get_neighbors(new_segment.first_point)) <= 1)
                        if real_cul_de_sac:
                            continue

                        current_segment_score = new_segment.score 
                        current_segment_score += 1000/(abs(26.5-max([new_segment.elev_gain_FtoL, new_segment.elev_gain_LtoF])/(new_segment.distance/1000))+1)**1.2
                        current_segment_score += len(graph.get_neighbors(new_segment.first_point)) + len(graph.get_neighbors(new_segment.last_point)) - 2
                        
                        if current_segment_score > best_new_segment_score:
                            best_new_segment_score = current_segment_score

                distance_neighbor_to_start = neighbor.calcul_dist(start)

                edge = tuple(sorted((node.id, neighbor.id)))

                delta = distance_neighbor_to_start - ditance_node_to_start

                score = segment.score*5

                if not len(graph.get_neighbors(segment.last_point)) > 1 or not len(graph.get_neighbors(segment.first_point)) > 1:
                    score -= 200

                if neighbor not in passed:
                    score += delta*5

                if edge in passed_edge:
                    score -= passed.index(neighbor)*2
                    score -= 1000
                else:
                    score += 600

                diff = neighbor.elevation - node.elevation
                if neighbor in passed:
                    score -= 1000 * passed.count(neighbor)
                else:
                    score += 500
                
                if diff > 0:
                    elevation_gain = diff
                else:
                    elevation_gain = 0
                score += 700/(abs(26.5-elevation_gain/(segment.distance/1000))+1)**1.2

                if best_new_segment_score > float("-inf"):
                    score += best_new_segment_score*4

                if score > best_score:
                    best_score = score
                    best_node = neighbor
                    best_dist = curr_dist
                    best_edge = edge
            
            node = best_node
            total_dist += best_dist
            passed.append(node)
            passed_edge.add(best_edge)

        total_dist += graph.get_shortest_path(node)[0]

        while node != start:
            node = graph.get_shortest_path(node)[1]
            passed.append(node)
        
        return passed, total_dist