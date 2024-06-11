import pandas as pd
import numpy as np
from dbfread import DBF

table = DBF('tl_bus_station_info.dbf', encoding='utf-8', load=True)

Busan_bus_data = pd.DataFrame(table.records)

Busan_bus_data_name = np.array(Busan_bus_data['bstopnm'].unique())

def get_gps_list(bstop_name) :
    filtered_data = Busan_bus_data[Busan_bus_data['bstopnm']==bstop_name]

    gps_list = np.array(filtered_data[['gpsx', 'gpsy']])

    return gps_list

def find_bstop_by_gps(gpsy, gpsx) :
    filtered_data = Busan_bus_data[(Busan_bus_data['gpsy']==gpsy) & (Busan_bus_data['gpsx']==gpsx)]

    bstop_id = filtered_data.iloc[0,1]

    return bstop_id


