import os
from osmnx.io import save_graphml, load_graphml
from osmnx.graph import graph_from_place
data_dir = f'{os.path.dirname(__file__)}/maps'

def load_map(place):
    '''load map saved as Graphml file'''
    try:
        G = load_graphml(f'{data_dir}/{place}.graphml')
    except:
        G = graph_from_place(place, network_type="walk")
        save_graphml(G, f'{data_dir}/{place}.graphml')
    return G