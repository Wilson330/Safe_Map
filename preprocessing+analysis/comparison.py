import safemap
map_preload = safemap.maps.load_map('Hsinchu Taiwan')
org=  [24.797308, 120.995583] # 機車塔
dst = [24.7968636, 120.9983978] # 立晉豆花
for method in ['astar', 'dijkstra', 'bidijkstra']:
    route = safemap.distance.safest_path(org, dst, alpha = 0.5, strip = 5, 
                                         method = method, map_preload=map_preload,
                                         debug = True)
'''
機車塔->立晉豆花
total edges: 624
total nodes: 205
path length: 13

astar: run time = 0.0059833526611328125
dijkstra: run time = 0.0009970664978027344
'''
#%%
org = [24.794295, 120.9653557] # 南大
dst = [24.7741843, 121.0479195] # 工研院
for method in ['astar', 'dijkstra', 'bidijkstra']:
    route = safemap.distance.safest_path(org, dst, alpha = 0.5, strip = 5, 
                                         method = method, map_preload=map_preload,
                                         debug = True)
'''
南大->工研院
total edges: 43548
total nodes: 15382
path length: 94

astar: run time = 0.4308469295501709
dijkstra: run time = 0.12267208099365234
'''
#%%
import safemap
org = [24.7961217, 120.9966699]#清大
dst = [24.8020976, 120.9667146]#山田麻糬製造所
'''
# 清大->山田麻糬製造所
total edges: 28342
total nodes: 9797
path length = 47
astar: run time = 0.19946718215942383
dijkstra: run time = 0.06781864166259766
'''
for method in ['dijkstra']:
    route = safemap.distance.safest_path(org, dst, alpha = 0.05, strip = 5, 
                                         method = method, map_preload=map_preload,
                                         debug = True, debug_plot = True)
    
