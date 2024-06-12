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
        'lineid' : root.find('lineid'),
        'start_point' : root.find('startpoint'),
        'end_point' : root.find('endpoint'),
        'gap_time' : root.find('headway'),
        'firts_time' : root.find('firsttime'),
        'last_time' : root.find('endtime'),
    }
    
    return info

def get_info_by_id(bstop_id): # 버스 정류장 아이디를 입력하면 그 정류장에 대한 정보를 반환하는 함수!
    try:
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
    except :
        st.warning("해당하는 정류장에 대한 정보가 없습니다.")
        st.warning("사유 : 1. 버스들이 오지 않을경우 (막차시간 지남)")
        st.warning("      2. API서버에서 정보를 받아오지 못했을 경우(운영자에게 문의바람)")

def get_info_by_lineid(line_id, bus_num):

    response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/busInfoByRouteId?lineid={line_id}&serviceKey={key}")
    
    if response.status_code != 200:
        st.write("정보를 불러오는데 실패했습니다")
        return None
    
    xml = response.text
    root = BeautifulSoup(xml, 'lxml')

    items = root.find_all('item')
    
    st.success(f"\'{bus_num}\'번 정차 정류소")

    for i in items :
        st.write(f"- {i.bstopnm.text}")

    return items
        
