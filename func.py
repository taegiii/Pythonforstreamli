import requests
from bs4 import BeautifulSoup
import xmltodict
import streamlit as st

key = 'xGzPl%2BpHZ%2BQsevCT%2FWyI4ryEPHeNHW5CEWmg83w2RgP%2F1rqZ7fhRVEF9a0Y8nSLeQ9JYuNZk8orw6Uy2hQEQTQ%3D%3D'
    
def get_bus_info_by_num(bus_num) :

    response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/busInfo?lineno={bus_num}&serviceKey={key}")

    if response.status_code != 200:
        print("API 호출 실패: ", response.status_code)
        return None
    
    xml = response.text
    root = BeautifulSoup(xml, 'lxml')

    info = {
        'start_point' : root.find('startpoint'),
        'end_point' : root.find('endpoint'),
        'gap_time' : root.find('headway'),
        'firts_time' : root.find('firsttime'),
        'last_time' : root.find('endtime'),
    }
    
    return info

def get_info_by_id(bstop_id):
    
    response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/stopArrByBstopid?serviceKey={key}&bstopid={bstop_id}")

    if response.status_code != 200:
        st.write("정보를 불러오는데 실패했습니다. 호출코드 :",response.status_code)
        return None
    
    xml = response.text
    root = BeautifulSoup(xml, 'lxml')

    busNum = root.find_all('lineno')
    left_time_1 = root.find_all('min1')
    left_bstop_1 = root.find_all('station1')

    for num, time, stop in zip(busNum, left_time_1, left_bstop_1) :
        st.divider()
        st.write(f"버스 번호 : {num.text}")
        st.write(f"{time.text}분 후 도착예정")
        st.write(f"버스가 {stop.text}정거장 전에 있습니다.")
        st.divider()


    
