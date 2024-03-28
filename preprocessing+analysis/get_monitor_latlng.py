#%%
import pandas as pd
import re
import itertools
from googlemaps import Client as GoolgeMaps


# monitor_data = pd.read_csv('data/HsinchuMonitorData.csv')
monitor_data = pd.read_json('data/HsinchuMonitorData.json')
# df_bad_ = pd.read_csv('data/address_bad_.csv', encoding = 'big5',index_col=0)

#%%
# geocode_result = geocode_result = gmaps.geocode('長興街500巷12弄口電桿朝巷內')
    
def get_monitor_pos_inform(name):
    landmark_pattern = r"(?:停車場|國小|國中|高中|大學|集會所|公園|圓環|KTV|廟)"
    road_pattern = r"(?:路|街|橋|交流道|大道|線)"
    face_road = re.findall(r'[朝向照往]+([^\d_()]*?[路街橋](?:.段|)(?:\d*[巷]|)(?:\d*[弄]|))', name)
    face_landmark = re.findall(r'[朝向照往]+([^\d_()]*?'+landmark_pattern+')', name)
    try:
        roads = re.findall(r'[^\d_()與朝向往照，、電]*?'+road_pattern+'(?:.段|)(?:\d*[巷]|)(?:\d*[弄]|)', name)
    except:
        roads = []
    
    landmark = re.findall(r'([^\d_()與朝向照往路街橋巷弄段旁，、]*?'+landmark_pattern+')前?', name)
    alley = re.findall(r'\d+[巷弄]', name)
    try:
        num = re.findall(r'\d*[號]', name)
    except:
        num = ''
    cross = any(re.findall(r'(?:口|與|橋下)\w*[朝往照向]?',name))
    mid = not any(re.findall(r'[路街巷弄][口]',name))and any(re.findall(r'[路街巷弄][中內]',name))
    result = {'name':name,         'roads': roads[:len(roads)-len(face_road)],
              'alley':alley,'num':num, 
              'face_road':face_road, 'face_landmark':face_landmark,
              'landmark':landmark, 
              'cross':cross, 'mid':mid
    }
    
    return result

def monitor_name2address(name):
    pos_inform = get_monitor_pos_inform(name)
    good = False
    address = '新竹市'
    if pos_inform['roads'] and pos_inform['num']:
        address += pos_inform['roads'][0]+pos_inform['num'][0]
        good = True
    elif len(pos_inform['roads'])>=2:
        address += '&'.join(pos_inform['roads'][:2])
        # if pos_inform['cross']:
        good = True
    elif pos_inform['cross'] and pos_inform['face_road']:
        address += '&'.join(pos_inform['roads']+pos_inform['face_road'])
        good = True
    elif pos_inform['roads'] and pos_inform['landmark']:
        address += pos_inform['roads'][0]+pos_inform['landmark'][0]
        good = True
    elif pos_inform['roads'] and pos_inform['mid']:
        address += pos_inform['roads'][0]
        good = True
    elif pos_inform['roads'] and pos_inform['alley']:
        address += pos_inform['roads'][0]
        good = True
    elif pos_inform['landmark']:
        address += pos_inform['landmark'][0]
        good = True
    else:
        address = ''
    return address, good, pos_inform

def clean_names(names):
    patterns = [
        r'\d+[重要鄰里擴充議餘園區]+\d?-?N[oO].?\d+(.*)', # 108重要-No.142
        r'\d+[-_][\d重要鄰擴餘]+[-_]\d+_?(.*)', # 106-1_159_
        r'\d+-[\d重鄰][（(][餘擴][）)]_\d+_(.*)', # 104-1（餘）_110_
        r'\d+-[\d擴]+-\d?N[oO].\d+(.*)', # 109-1擴-1NO.54
        # r'\d+\w+-NO\d(.*)', # 108重要擴充-NO2
        r'104重要(.*)',
        # r'104-2(.*)'
        # 104-2# 109-1-NO.15
    ]
    pattern_cycle = itertools.cycle(patterns)
    names_cleaned = []
    for i,name in enumerate(names):
        for count in range(len(patterns)):
            pattern = next(pattern_cycle)
            name_cleaned = re.findall(pattern,name)
            if name_cleaned:
                names_cleaned.append(name_cleaned[0])
                # print(i)
                break
            elif count == len(patterns)-1:
                print('failed cleaning:', i, name)
                names_cleaned.append(name)
    return names_cleaned
#%%
results = {'name':[],'roads':[],
           'alley':[],'num':[],
           'face_road':[], 'face_landmark':[],
           'landmark':[],'cross':[], 'mid':[],
           'address':[], 'good_address': []}
names_cleaned = clean_names(monitor_data['攝影機名稱'])

for name in names_cleaned:
    # print(name)
    # pos_inform = get_monitor_pos_inform(name)
    address, good, pos_inform = monitor_name2address(name)
    for k,v in pos_inform.items():
        results[k].append(v)
    results['address'].append(address)
    results['good_address'].append(good)
    
df = pd.DataFrame(results)

print('Adress is good:')
print(df['good_address'].value_counts())
df_bad = df[df['good_address']==False]
df_good = df[df['good_address']==True]
df_bad.to_csv('data/address_bad.csv',encoding='big5')

#%%
import json
import googlemaps
from tqdm import tqdm
def get_googlemap_coordinates(address, key='', save_name = None):
    gmaps = googlemaps.Client(key = key)
    geocode_result = gmaps.geocode(address)[0]
    formatted_address = geocode_result['formatted_address']
    coordinates = geocode_result['geometry']['location']
    #if save_name is not None:
    #    with open(f'./data/monitor/geocode/{save_name}.json', 'w') as f:
    #        json.dump(geocode_result,f)
    return {'formatted_address': formatted_address, 'coordinates': coordinates}
#%%
if True:
    geocode_results = []
    failed = []
    
    for monitor in tqdm(df_good.iloc):     
        try:
            result = get_googlemap_coordinates(monitor['address'], save_name = monitor.name,
                                               key = '') #use your own key
            geocode_results.append(result)
            # break
        except:
            print('failed: monitor',monitor.name, monitor['address'])
            failed.append(monitor.name)

    with open('./data/monitor_coordinates.json', 'w') as f:
        json.dump(geocode_results,f, indent = 2)
        # sample_result = json.load(f)