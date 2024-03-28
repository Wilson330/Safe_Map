import osmnx as ox
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy.stats 
import pickle

class KDE(scipy.stats.gaussian_kde):
    def __init__(self, dataset, bw_method = 'scott', bw_factor = 1):
        super().__init__(dataset,bw_method = bw_method)
        self.set_bandwidth(bw_method = self.factor*bw_factor)
        
def get_node_scores(nodes, kde):
    scores = {} 
    for key,node in nodes:
        scores[key] = kde([node['x'], node['y']])[0]
    return scores

def get_edge_scores(edges, node_scores):
    scores = {}
    for u,v, attr in edges:
        score = (node_scores[u]+node_scores[v])/2
        scores[(u,v)] = score
    return scores

def get_safety_scores(light_scores, monitor_scores, beta):
    safety_scores = {}
    for k in monitor_scores.keys():
        safety_scores[k] = beta*light_scores[k] + (1-beta)*monitor_scores[k]
    return safety_scores

#%% test
if __name__== '__main__ ':
    import data
    lights = data.load_data('lights')
    monitors = data.load_data('monitors')
    maps = data.load_data('maps')
    
    kde_lights =   KDE(lights[['lng','lat']].T, bw_method = 'scott', bw_factor = 0.1)
    kde_monitors = KDE(monitors[['lng','lat']].T, bw_method = 'scott', bw_factor = 0.1)
    node_scores = {
        'light':   get_node_scores(maps['Hsinchu'].nodes(data = True), kde_lights),
        'monitor': get_node_scores(maps['Hsinchu'].nodes(data = True), kde_monitors),
    }
    
    edge_scores = {
        'light':   get_edge_scores(maps['Hsinchu'].edges(data = True), node_scores['light']),
        'monitor': get_edge_scores(maps['Hsinchu'].nodes(data = True), node_scores['monitor']),
    }
    edge_scores['safety'] = get_safety_scores(edge_scores['light'],
                                              edge_scores['monitor'], 0.5)
    
    for k,v in edge_scores.items:
        with open (f'Data/scores/edge_{k}_scores.pickle', 'wb') as f:
            pickle.dump(v, f)
            #%%
    def plot_graph_kde_score(G, x=None,y=None, show_points = False, show_map = False, show_kde = True,c= {}):
        cmap = mpl.cm.magma(np.linspace(0.3,1,20))
        cmap = mpl.colors.ListedColormap(cmap[:,:-1])
        
        fig, ax = plt.subplots(figsize = (20,20), dpi = 300)
        ax.patch.set_color('#111111')
        # ax.patch.set_color((.6,.6,.6))
        if show_kde:
            sns.kdeplot(x = x, y = y, ax=ax,
                        bw_adjust = .1, thresh = 0.1,
                        cmap = cmap,  fill = True, alpha = 0.8, levels = 10, cbar = False)
        if show_map:
            ox.plot_graph(G, ax, show = False, bgcolor='#111111',
                          node_color = 'w', node_alpha = 0.8, node_size = 6,
                          edge_color='#999999', edge_linewidth = 0.8)
        
        if show_points:
            color = {
                None:None,
                'o':[0.985693, 0.528148, 0.379371],
                'b': np.array((181,219,248))/255,
                'y':[0.994524, 0.841387, 0.598983],
                'w':[0.9,0.9,0.9],
                'p':[0.569172, 0.167454, 0.504105]
            }
            ax.scatter(x, y, s = 4, alpha = 0.8,color = color[c.get('points')]) # orange
        plt.axis('off')
        return fig
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
    fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat,
                               show_points = False, show_map = True, show_kde = True)
    fig.savefig('figures/lights_kde.png',transparent = True)

    fig = plot_graph_kde_score(maps['Hsinchu'], monitors.lng, monitors.lat,
                               show_points = False, show_map = False, show_kde = True)
    fig.savefig('figures/monitors_kde.png',transparent = True)

    #%% only map
    fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat,
                               show_points = False, show_map = True, show_kde = False)
    fig.savefig('figures/map.png',transparent = True)
    
    #%% maps+kde
    fig = plot_graph_kde_score(maps['Hsinchu'], lights.lng, lights.lat,
                               show_points = False, show_map = True, show_kde = True)
    fig.savefig('figures/map+lights_kde.png',transparent = True)
    
    