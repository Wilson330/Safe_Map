from osmnx.truncate import truncate_graph_polygon
from osmnx.utils_geo import bbox_to_poly
import numpy as np

def get_subgraph(G, bbox):
    poly_b = bbox_to_poly(*bbox)
    subG = truncate_graph_polygon(G, poly_b)
    return subG

def get_bbox(pt1,pt2, map_width_factor = 0.5):
    mid_point = np.mean([[pt1, pt2],[pt1, pt2]],1)
    d_max = np.max(list(map(lambda x: np.abs(np.diff(x)), zip(pt1, pt2))))
    bbox = np.add(mid_point.T.flatten(),np.array([1,-1,1,-1])*d_max*map_width_factor)
    return bbox