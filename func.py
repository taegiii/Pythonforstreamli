import requests
from bs4 import BeautifulSoup
import json
import xmltodict
import streamlit as st

key = 'xGzPl%2BpHZ%2BQsevCT%2FWyI4ryEPHeNHW5CEWmg83w2RgP%2F1rqZ7fhRVEF9a0Y8nSLeQ9JYuNZk8orw6Uy2hQEQTQ%3D%3D'

def get_bus_arrival_info(id):
    response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/stopArrByBstopid?serviceKey={key}&Bstopid={id}")

    if response.status_code != 200:
        print("API 호출 실패: ", response.status_code)
        return None, None
    
    xml = response.text
    root = BeautifulSoup(xml, 'xml')

    bus_number = root.find_all('lineno')
    #left_station = root.find_all('station1')

    if not bus_number:
        print("데이터를 찾을 수 없습니다.")
        return None, None

    for num in bus_number:
        print(f"버스 번호: {num.text}")

    return bus_number
    
def get_bus_info_by_num(bus_num) :

    response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/busInfo?lineno={bus_num}&serviceKey={key}")

    if response.status_code != 200:
        print("API 호출 실패: ", response.status_code)
        return None
    
    xml = response.text
    root = BeautifulSoup(xml, 'xml')

    info = {
        'start_point' : root.find('startpoint'),
        'end_point' : root.find('endpoint'),
        'gap_time' : root.find('headway'),
        'firts_time' : root.find('firsttime'),
        'last_time' : root.find('endtime'),
    }
    
    return info