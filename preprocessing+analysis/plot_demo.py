import pickle
import numpy as np
import seaborn as sns
import matplotlib as mpl
import matplotlib.pyplot as plt
import osmnx as ox
import networkx as nx

import data
import scores
from osm_plot import plot_graph_kde_score, plot_graph_with_score
#%%
lights = data.load_data('lights')
monitors = data.load_data('monitors')
maps = data.load_data('maps')

kde_lights =   scores.KDE(lights[['lng','lat']].T, bw_method = 'scott', bw_factor = 0.1)
kde_monitors = scores.KDE(monitors[['lng','lat']].T, bw_method = 'scott', bw_factor = 0.1)
node_scores = {
    'light':   scores.get_node_scores(maps['Hsinchu'].nodes(data = True), kde_lights),
    'monitor': scores.get_node_scores(maps['Hsinchu'].nodes(data = True), kde_monitors),
}

edge_scores = {
    'light':   scores.get_edge_scores(maps['Hsinchu'].edges(data = True), node_scores['light']),
    'monitor': scores.get_edge_scores(maps['Hsinchu'].edges(data = True), node_scores['monitor']),
}
edge_scores['safety'] = scores.get_safety_scores(edge_scores['light'],
                                          edge_scores['monitor'], 0.5)

for k,v in edge_scores.items():
    with open (f'Data/scores/edge_{k}_scores.pickle', 'wb') as f:
        pickle.dump(v, f)
#%%

#%%
for c in ['o','b','y','w','p']:
    fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat, c = {'points':c},
                               show_points = True, show_map = True, show_kde = False)
    
    fig.savefig(f'figures/lights/lights_{c}.png',transparent = True)
    
    fig = plot_graph_kde_score(maps['Hsinchu'], monitors.lng, monitors.lat, c = {'points':c},
                               show_points = True, show_map = False, show_kde = False)
    fig.savefig(f'figures/monitors/monitors_{c}.png',transparent = True)
    
    fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat, c = {'points':c},
                               show_points = True, show_map = True, show_kde = False)
    fig.savefig(f'figures/map+lights/map+lights_{c}.png',transparent = True)
    
    fig = plot_graph_kde_score(maps['Hsinchu'], monitors.lng, monitors.lat, c = {'points':c},
                               show_points = True, show_map = True, show_kde = False)
    fig.savefig(f'figures/map+monitors/map+monitors_{c}.png',transparent = True)

#%% kde plot
cmap = mpl.cm.magma(np.linspace(0.4,1,20))
cmap = mpl.colors.ListedColormap(cmap[:,:-1])
cmap = None
fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat,
                           show_points = False, show_map = False, show_kde = True, cmap = cmap)
fig.savefig('figures/lights_kde_v1.png',transparent = True)

fig = plot_graph_kde_score(maps['Hsinchu'], monitors.lng, monitors.lat,
                           show_points = False, show_map = False, show_kde = True, cmap = cmap)
fig.savefig('figures/monitors_kde_v1.png',transparent = True)

#%% only map
fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat,
                           show_points = False, show_map = True, show_kde = False)
fig.savefig('figures/map.png',transparent = True)

#%% maps+kde
fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat,
                           show_points = False, show_map = True, show_kde = True)
fig.savefig('figures/map+lights_kde.png',transparent = True)

#%%
cmap = mpl.cm.magma(np.linspace(0.4,1,20))
save_dir = 'figures/map_with_scores'
fig, ax = plt.subplots(figsize = (20,20), dpi = 300)
plot_graph_with_score(maps['Hsinchu'],edge_scores['light'],ax=ax,
                      ls='-', lw=2.5, cmap = cmap)
plt.axis('off')
fig.savefig(f'{save_dir}/map_with_light_scores_v2.png',transparent = True)
#---------------
fig, ax = plt.subplots(figsize = (20,20), dpi = 300)
plot_graph_with_score(maps['Hsinchu'],edge_scores['monitor'],ax=ax,
                      ls='-', lw=2.5, cmap = cmap)
plt.axis('off')
fig.savefig(f'{save_dir}/map_with_monitor_scores_v2.png',transparent = True)
#---------------
fig, ax = plt.subplots(figsize = (20,20), dpi = 300)
plot_graph_with_score(maps['Hsinchu'],edge_scores['safety'],ax=ax,
                      ls='-', lw=2.5, cmap = cmap)
plt.axis('off')
fig.savefig(f'{save_dir}/map_with_safety_scores_v2.png',transparent = True)