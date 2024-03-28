from flask import Flask
from flask import request
import matplotlib.pyplot as plt
# import time
# import numpy as np
import safemap

app = Flask(__name__)
DEBUG = True
print('loading map...')
map_preload = safemap.maps.load_map('Hsinchu Taiwan')
print('Done!')
def path(origin, destin, alpha, beta): 
    global map_preload
    if None in (origin,destin,alpha):
        return {'latlng':[]}
    else:
        origin = list(map(float,origin.split(',')))
        destin = list(map(float,destin.split(',')))
        alpha = float(alpha)/100
        beta = 0.5
    print('origin',origin)
    print('destin',destin)
    print('alpha',alpha)
    print('beta',beta)
    
    route = safemap.distance.safest_path(
        origin, destin, method='bidijkstra', 
        map_width_factor = 1.0, alpha = alpha, beta = beta, 
        return_latlng = True, strip = 0, max_length=25, map_preload=map_preload,
        debug_plot = False, 
    )
    
    distance = safemap.distance.route_dist(route)
    if DEBUG:
        for latlng in route:
            print('{'+f'lat:{latlng[0]}, lng: {latlng[1]}'+'},')
            print('distance=',distance)
    return {'latlng':route,'distance':round(distance), 'duration':round(distance/5)}

@app.route("/data", methods=['GET'])
def index():
    origin = request.args.get("origin")
    destin = request.args.get("destination")
    alpha = request.args.get("weights")
    beta = 0.5
    # print('origin',origin)
    # print('destin',destin)
    # print('alpha',alpha)
    # print(origin, destin)
    # print(type(origin))
    # print(origin[0],origin[1])
    
    return path(origin, destin, alpha, beta)

app.run()
