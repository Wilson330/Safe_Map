----------Data-------------------
HsinchuMonitorData.json 
(some addresses(攝影機名稱) have been modified, to enable our preprocessing code to work)
scource: https://data.gov.tw/dataset/67490

HsinchuStreetLightData.json (raw data)
scource: https://opendata.hccg.gov.tw/OpenDataDetail.aspx?n=1&s=159

monitor_coordinates.json
output of get_monitor_latlng.py, coordinates (lat,lng) of the monitors.

----------Preprocessing----------
get_monitor_latlng.py - get address from HsinchuMonitorData.json and convert to lat,lng with google api.

scores.py - calculate scores of nodes and edges with Kernel Density Estimation (with scipy).

----------Analysis---------------
comparison.py - comparison of different searching algorithms.

plot_demo.py, osm_plot.py - plot for presentation and analysis.