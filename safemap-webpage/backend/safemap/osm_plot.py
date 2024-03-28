# -*- coding: utf-8 -*-
"""
Created on Fri Jan  6 04:06:47 2023

@author: ess512
"""
#
import osmnx as ox
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib as mpl
from osmnx.plot import utils_graph

def plot_route(G,route,ax=None,c=None,ls='-',lw=2, alpha=0.8,**kargs):
    if ax is None:
        fig, ax = plt.subplots(figsize = (8,6), dpi = 300)
    x,y,x_,y_ = [],[],[],[]
    for u, v in zip(route[:-1], route[1:]):
        # if there are parallel edges, select the shortest in length
        data = min(G.get_edge_data(u, v).values(), key=lambda d: d["length"])
        if "geometry" in data:
            # if geometry attribute exists, add all its coords to list
            xs, ys = data["geometry"].xy
            x.extend(xs)
            y.extend(ys)
        else:
            # otherwise, the edge is a straight line from node to node
            x.extend((G.nodes[u]["x"], G.nodes[v]["x"]))
            y.extend((G.nodes[u]["y"], G.nodes[v]["y"]))
            x_.append(G.nodes[u]["x"])
            y_.append(G.nodes[v]["y"])
    ax.plot(x, y, ls=ls, lw=lw, c=c, alpha=alpha, label = kargs.get('label'))
    if kargs.get('scatter'):
        ax.scatter(x,y)
def plot_graph_with_score(G,scores, ls='-', lw=2, ax = None,cmap = None):
    if cmap is None:
        cmap = mpl.cm.magma(np.linspace(0.3,1,20))
        # cmap = mpl.colors.ListedColormap(cmap[:,:-1])

    df = pd.DataFrame({'score':scores.values()},
                      index=pd.MultiIndex.from_tuples(scores.keys()))
    df['score_cut'], bins = pd.qcut(df.score, q = 10,labels = False,retbins=True)
    if ax is None:
        fig, ax = plt.subplots(figsize = (8,6), dpi = 300)

    colors = cmap[df['score_cut'].loc[G.edges()]]
    gdf_edges = utils_graph.graph_to_gdfs(G, nodes=False)["geometry"]
    ax = gdf_edges.plot(ax=ax, color=colors, ls = ls, lw=lw, alpha=0.8, zorder=1,)
    ax.ticklabel_format(useOffset = False)
    return ax

def plot_graph_kde_score(G, x=None,y=None, show_points = False, show_map = False, show_kde = True,c= {},cmap = None):
    import seaborn as sns
    if cmap is None:
        cmap = mpl.cm.magma(np.linspace(0.3,1,20))
        cmap = mpl.colors.ListedColormap(cmap[:,:-1])
    
    fig, ax = plt.subplots(figsize = (20,20), dpi = 300)
    ax.patch.set_color('#111111')
    # ax.patch.set_color((.6,.6,.6))
    if show_kde:
        sns.kdeplot(x = x, y = y, ax=ax,
                    bw_adjust = .1, thresh = 0.1,
                    cmap = cmap,  fill = True, alpha = 0.8, levels = 10)
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

def show_result(G, org=None,dst = None, routes={}, ax=None, route_c = {}, route_lw=3, route_ls=':',**kargs):
    if ax is None:
        fig, ax = plt.subplots(figsize = (8,6), dpi = 300)
    fig, ax = plt.subplots(figsize = (8,8),dpi = 300)
    fig.patch.set_color('#111111')
    if kargs.get('scores'):
        plot_graph_with_score(G, kargs.get('scores'), lw=3, ax = ax)
    else:
        ox.plot_graph(G, ax, show = False, bgcolor='none',
                      node_color = 'w', node_alpha = 0, node_size = 0,
                      edge_color='none', edge_linewidth = 3)
    ax.scatter(org[1], org[0], label = 'origin', s = 30)
    ax.scatter(dst[1], dst[0], label = 'destination', s = 30)
    for k, route in routes.items():
        plot_route(G, route, ax=ax, c=route_c.get(k), 
                   lw=route_lw, ls=route_ls, label = k, alpha = 1)
    plt.axis(False)
    plt.legend()
    return ax
# def plot_kde_scores(G, kde)
#%%
