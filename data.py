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

    gps_list = np.array(filtered_data[['gpsx', 'gpsy']].values)

    return gps_list
###########

###########
def find_bstop_by_gps(gpsy, gpsx) :
    filtered_data = Busan_bus_data[(Busan_bus_data['gpsy']==gpsy) & (Busan_bus_data['gpsx']==gpsx)]

    bstop_id = filtered_data.iloc[0,1]

    return bstop_id
###########

###########
def to_map_pin(list, bus_num) :

    gps_list1 = [] #정류장에 핀꽂을때 사용하는 gps

    for content in list :

        if not content.bstopnm or not content.bstopnm.text:
            continue  #arsno가 없을때도 있어서 그걸 처리하기 위해서
        
        gps_data = get_gps_list(content.bstopnm.text)
            

        for [x, y] in gps_data :
            gps_list1.append([y, x])
    
    gps_list1 = np.array(gps_list1)
    
    m = folium.Map(location=[gps_list1[0][0], gps_list1[0][1]], zoom_start=15)

    for [y, x] in gps_list1 :

        folium.Marker([y,x], tooltips=f"{bus_num}번 정류장", popup="").add_to(m)
        
    st_folium(m, width=700, height=500)

###########

    


