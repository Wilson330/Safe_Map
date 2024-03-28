import os
import json
import numpy as np
import pandas as pd
import pickle
data_dir = f'{os.path.dirname(__file__)}'+'/data'
from osmnx.io import save_graphml, load_graphml
from osmnx.graph import graph_from_place

def load_data(dataset):
    data = eval(f'_load_{dataset}')()
    return data

def _load_monitors():
    with open(f'{data_dir}/monitor/geocode/monitor_coordinates.json', 'r') as f:
        monitors = json.load(f)
    monitors = pd.json_normalize(monitors)
    monitors = monitors.rename(columns = {'coordinates.lat':'lat','coordinates.lng':'lng'})
    monitors = monitors[np.logical_and(24.7<monitors.lat,monitors.lat<24.9)]
    monitors = monitors[np.logical_and(120.8<monitors.lng,monitors.lng<121.04)]
    return monitors

def _load_lights():
    lights = pd.read_json('{data_dir}/HsinchuStreetLightData.json')
    lights = lights.drop(index = [6269,18416,22134], columns = lights.columns[1:-2])
    lights = lights.replace('', np.nan).dropna()
    lights = lights.rename(columns = {'WGS84_N':'lat','WGS84_E':'lng'})
    lights.lat = lights.lat.apply(float)
    lights.lng = lights.lng.apply(float)
    lights = lights[np.logical_and(24.7<lights.lat,lights.lat<24.9)]
    lights = lights[np.logical_and(120.8<lights.lng,lights.lng<121.04)]
    return lights

def _load_maps():
    import osmnx as ox
    maps = {}
    for name in ['Hsinchu','E_district','N_district','X_district']:        
        try:
            with open(f'{data_dir}/maps/{name}.pickle', 'rb') as f:
                maps[name] = pickle.load(f)
        except:
            place = {
                'Hsinchu':'Hsinchu Taiwan',
                'E_district': 'East district, Hsinchu Taiwan',
                'N_district': 'North district, Hsinchu Taiwan',
                'X_district': 'XiangShan district, Hsinchu Taiwan'
            }
            maps[name] = graph_from_place(place[name], network_type="walk")
            with open(f'{data_dir}/maps/{name}.pickle', 'wb') as f:
                pickle.dump(maps[name], f)
    return maps

def load_map(place):
    '''load map saved as Graphml file'''
    try:
        G = load_graphml(f'{data_dir}/maps/{place}.graphml')
    except:
        G = graph_from_place(place, network_type="walk")
        save_graphml(f'{data_dir}/maps/{place}.graphml')
    return G
    
    