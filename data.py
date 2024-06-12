import pandas as pd
import numpy as np
from dbfread import DBF
import folium
import streamlit as st
from streamlit_folium import st_folium


table = DBF('tl_bus_station_info.dbf', encoding='utf-8', load=True)

Busan_bus_data = pd.DataFrame(table.records)

Busan_bus_data_name = np.array(Busan_bus_data['bstopnm'].unique())

###########
def get_gps_list(bstop_name) :
    filtered_data = Busan_bus_data[Busan_bus_data['bstopnm']==bstop_name]

    gps_list = np.array(filtered_data[['gpsx', 'gpsy']])

    return gps_list
###########

###########
def find_bstop_by_gps(gpsy, gpsx) :
    filtered_data = Busan_bus_data[(Busan_bus_data['gpsy']==gpsy) & (Busan_bus_data['gpsx']==gpsx)]

    bstop_id = filtered_data.iloc[0,1]

    return bstop_id
###########

###########
def to_map_line(list, bus_num) :

    gps_list = []
    name_list = []

    for content in list :

        if not content.arsno or not content.arsno.text:
            continue  #arsno가 없을때도 있기에

        filtered_data = Busan_bus_data[Busan_bus_data['arsno'] == content.arsno.text]

        name_list.append(filtered_data['bstopnm'].values)

        gps_info = filtered_data[['gpsy', 'gpsx']].values

        for info in gps_info:
            gps_list.append(info)
            

    gps = np.array(gps_list)
    
    m = folium.Map(location=[gps[0][0], gps[0][1]], zoom_start=15)

    for [y, x], name in zip(gps, name_list) :

        folium.Marker([y,x], tooltips=f"{bus_num}번 정류장", popup=f"{name}").add_to(m)

    folium.PolyLine(locations=gps,
                    color='blue',
                    weight=5,
                    opacity=0.7,
                    tooltips=f'{bus_num}노선도').add_to(m)
        
    st_folium(m, width=700, height=500)

###########

    


