import safemap
import matplotlib.pyplot as plt
# import opencv
map_preload = safemap.maps.load_map('Hsinchu Taiwan')
org=  [24.797308, 120.995583] # 機車塔
dst = [24.7968636, 120.9983978] # 立晉豆花

for method in ['astar', 'dijkstra', 'bidijkstra']:
    route = safemap.distance.safest_path(
        org, dst, alpha = 0.5, strip = 5, 
        method = method, map_preload=map_preload)
#%%
import safemap
from safemap.osm_plot import plot_graph_with_score, plot_route
route = safemap.distance.safest_path(
    org, dst, alpha = 0.5, strip = 0, 
    method = 'astar', map_preload=map_preload, return_latlng=False,debug_plot = True)
#%%
route_short = safemap.distance.safest_path(
    org, dst, alpha = 1., strip = 0, 
    method = 'bidijkstra', map_preload=map_preload, return_latlng=False)
safety_scores = safemap.scores.load_score('safety')

bbox = safemap.maps.utils.get_bbox(org,dst,map_width_factor = 0.8)
Map = safemap.maps.utils.get_subgraph(map_preload, bbox, )
fig, ax = plt.subplots(figsize = (8,8),dpi = 300)
fig.patch.set_color('#111111')
plot_graph_with_score(Map, safety_scores, lw=3, ax = ax)
ax.scatter(org[1], org[0], label = 'origin', s = 30)
ax.scatter(dst[1], dst[0], label = 'destination', s = 30)
plot_route(Map, route_short, ax=ax, c='w', lw=3, ls=':', label = 'shortest', alpha = 1)
plot_route(Map, route, ax=ax, c = (0.2,0.95,0.90), lw=3, ls='--', label = 'safe path',alpha = 1)
plt.axis(False)
plt.legend()
plt.show()
fig.savefig(f'safemap_demo.png',transparent = True)
