import osmnx as ox
import networkx as nx
# import numpy as np
import time
from . import maps, scores
import numpy as np
import matplotlib.pyplot as plt
# import maps
# import scores
# from .maps.utils import get_subgraph, get_bbox

MAX_LENGTH = 3393.4990000000007
MAX_LIGHT_SCORE = 1045.0936000466504 
MAX_MONITOR_SCORE = 12602.059664336644 
MAX_SAFETY_SCORE = 6489.245010093811
# with open ('Data/lights/light_edge_scores.pickle', 'rb') as f:
#     light_edge_scores = pickle.load(f)
# with open ('Data/monitor/monitor_edge_scores.pickle', 'rb') as f:
#     monitor_edge_scores = pickle.load(f)

def safest_path(org, dst, method='bidijkstra', 
                map_width_factor = 1.0, alpha = 0.5, beta = 0.5, return_latlng = True, 
                strip = 0,max_length = None, map_preload=None,**kargs
                ):
    '''
    Compute shortest paths in the graph, based on the safety (density of streetlights and monitors).
    
    Parameters
    ----------
    org, dst : tuple
        origin and the distination
        (latitude, longtitude)
    alpha: float between [0,1]
        The factor that controls the weights of distance and saftey, when selecting the optimal path.
    beta: float between [0,1]
        The factor that controls the coposition of saftey, which the larger beta is, 
        the more weight is on the streetlights and less on the monitors.
        
    Returns 
    -------
    path: list
        A list of nodes composing the safest path from the origin to the distination.

    '''
    if map_preload is None:
        print('loading map...')
        map_preload = maps.load_map('Hsinchu Taiwan')
        print('Done!')
    bbox = maps.utils.get_bbox(org,dst,map_width_factor = map_width_factor)
    Map = maps.utils.get_subgraph(map_preload, bbox)
    # Map = ox.graph.graph_from_bbox(*bbox, network_type="walk")
    
    astar_heuristic = (lambda a,b: alpha*node_dist(Map,a,b)/MAX_LENGTH)
    path_search_methods = {
    'dijkstra'  : nx.dijkstra_path,
    'bidijkstra': lambda *args,**kargs: nx.bidirectional_dijkstra(*args, **kargs)[1],
    'astar'     : lambda *args,**kargs: nx.astar_path(*args, **kargs,heuristic = astar_heuristic),
    }
    assert (method in path_search_methods.keys()), '"method" should be one of "dijkstra","bidijkstra" or "astar".'

    edge_monitor_scores = scores.load_score('monitor')
    edge_light_scores = scores.load_score('light')
    edge_safety_scores = scores.load_score('safety')
    
    source_node = ox.distance.nearest_nodes(Map, org[1], org[0])
    target_node = ox.distance.nearest_nodes(Map, dst[1], dst[0])
    
    attributes_add = {} 
    for u, v, k, data in Map.edges(data=True, keys=True):
        F_distance = data["length"] / MAX_LENGTH
        F_light    = edge_light_scores[(u, v)] / MAX_LIGHT_SCORE
        F_monitor  = edge_monitor_scores[(u, v)] / MAX_MONITOR_SCORE
        # F_safety = edge_safety_scores[(u, v)] / MAX_SAFETY_SCORE
        weight = (1-alpha)*F_distance + alpha*(beta*(1-F_light)+(1-beta)*(1-F_monitor))
        attributes_add[(u, v, k)] = {
            "lights"  : edge_light_scores[(u, v)],
            "monitors": edge_monitor_scores[(u, v)],
            # "safety"  : edge_safety_scores[(u, v)],
            "weight"  : weight
        }
    nx.set_edge_attributes(Map, attributes_add)
    
    print(f'running {method} algorithm...')
    start = time.time()
    route = path_search_methods[method](Map, source_node, target_node, weight='weight')
    print(f'run time = {time.time()-start}')
    print('path length:', len(route))
    
    if kargs.get('debug'):
        print(f'total edges: {len(Map.edges)}')
        print(f'total nodes: {len(Map.nodes)}')
        
    if kargs.get('debug_plot'):
        from . import osm_plot
        route_short = nx.bidirectional_dijkstra(Map, source_node, target_node, weight='length')[1]
        fig, ax = plt.subplots(figsize = (8,8),dpi = 100)
        fig.patch.set_color('#111111')
        osm_plot.plot_graph_with_score(Map, edge_safety_scores, lw=3, ax = ax)
        ax.scatter(org[1], org[0], label = 'origin', s = 30)
        ax.scatter(dst[1], dst[0], label = 'destination', s = 30)
        osm_plot.plot_route(Map, route_short, ax=ax, c='w', lw=3, ls=':', label = 'shortest', alpha = 1)
        osm_plot.plot_route(Map, route, ax=ax, c = (0.2,0.95,0.90), lw=3, ls='--', label = 'safe path',alpha = 1)
        plt.axis(False)
        plt.legend()
        plt.savefig('debug.png')
        plt.close()
    
    if strip:        
        route = strip_route(Map, route, th = strip , max_length=max_length)
        print('stripped path length:', len(route))
    elif return_latlng:
        route = extend_route(Map, route)
        print('extended path length:', len(route))
        return route
    print('Done!')
    if return_latlng:
        # latlng = [(Map.nodes[i]['y'],Map.nodes[i]['x']) for i in route]
        latlng = [id2latlng(Map,id) for id in route]
        return latlng
    return route

def node_dist(G, a, b):
    lng1, lat1 = G._node[a]['x'], G._node[a]['y']
    lng2, lat2 = G._node[b]['x'], G._node[b]['y']
    return ox.distance.great_circle_vec(lat1,lng1,lat2,lng2)
    # return ((((x1 - x2)*101775.45) ** 2 + ((y1 - y2)*110936.2) ** 2) ** 0.5)/m*alpha

def route_dist(route):
    '''
    Compute shortest paths in the graph, based on the safety (density of streetlights and monitors).
    
    Parameters
    ----------
    G : osm graph
    route: list
        a list of (lat,long), or list of node ids(Not implemented yet)
    
    Returns 
    -------
    distance: float
        distance to destination
    
    '''
    dist = 0
    for (lat1,lng1),(lat2,lng2) in zip(route[:-1], route[1:]):
        dist += ox.distance.great_circle_vec(lat1,lng1,lat2,lng2)
    return dist
    

def id2latlng(G, node_id):
    """return lat,lng"""
    node = G.nodes[node_id]
    return node['y'], node['x']

def extend_route(G,route):
    route_ = []
    for u, v in zip(route[:-1], route[1:]):
    # if there are parallel edges, select the shortest in length
        data = min(G.get_edge_data(u, v).values(), key=lambda d: d["length"])
        if "geometry" in data:
            # if geometry attribute exists, add all its coords to list
            xs, ys = data["geometry"].xy
            route_.extend(list(zip(ys,xs)))
        else:
            # otherwise, the edge is a straight line from node to node
            route_.append(id2latlng(G, u))
    return route_

def strip_route(G, route, th = 5, max_length = None, step = 1):
    if max_length is None:
        max_length = len(route)
    while True:
        route_=[]
        for a,b in zip(route[:-1],route[1:]):
            if node_dist(G,a,b)>=th:
                route_.append(a)
        route = route_
        if len(route)<=max_length:
            break
    return route
#%%
if __name__ == '__main__':
    org = (24.7916987, 120.99242952395865)
    dst = (24.7952997, 120.980283)
    print(safest_path(org, dst, strip = 20, method = 'astar'))