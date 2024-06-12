import requests
from bs4 import BeautifulSoup
import xmltodict
import streamlit as st
import data
import folium
from streamlit_folium import st_folium


key = 'xGzPl%2BpHZ%2BQsevCT%2FWyI4ryEPHeNHW5CEWmg83w2RgP%2F1rqZ7fhRVEF9a0Y8nSLeQ9JYuNZk8orw6Uy2hQEQTQ%3D%3D'
    
def get_bus_info_by_num(bus_num) : #버스 번호로 도착정보 찾아오기

    response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/busInfo?lineno={bus_num}&serviceKey={key}")

    if response.status_code != 200:
        print("API 호출 실패: ", response.status_code)
        return None
    
    xml = response.text
    root = BeautifulSoup(xml, 'lxml')
    
    items = root.find_all('item')

    for content in items :
        if bus_num != content.buslinenum.text:
            continue

        else :
            info = {
                    'lineid' : content.lineid.text,
                    'start_point' : content.startpoint.text,
                    'end_point' : content.endpoint.text,
                    'gap_time' : content.headwaynorm.text,
                    'firts_time' : content.firsttime.text,
                    'last_time' : content.endtime.text,
                    }
    
    return info

def get_info_by_arsno(arsno) : #arsno로 버스 정류장 도착정보 찾아오기
    try:
        response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/bitArrByArsno?arsno={arsno}&serviceKey={key}")

        if response.status_code != 200:
            st.write("정보를 불러오는데 실패했습니다. 호출코드 :",response.status_code)
            return None
        
        xml = response.text
        root = BeautifulSoup(xml, 'lxml')
        
        items = root.find_all('item')

        for content in items :

            if not content.min1 or not content.station1:
                continue

            st.divider()
            st.write(f"버스 번호 : {content.lineno.text}")
            st.write(f"{content.min1.text}분 후 도착예정")
            st.write(f"버스가 {content.station1.text}정거장 전에 있습니다.")
            st.divider()
    except :
        st.warning("해당하는 정류장에 대한 정보가 없습니다.")
        st.warning("사유 : \n 1. 버스정보가 없을 경우\n2. 버스들이 오지 않을경우 (막차시간 지남)\n3. API서버에서 정보를 받아오지 못했을 경우(운영자에게 문의바람)")
        


def get_info_by_id(bstop_id): # 버스 정류장 아이디를 입력하면 그 정류장에 대한 정보를 반환하는 함수!
    try:
        response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/stopArrByBstopid?serviceKey={key}&bstopid={bstop_id}")

        if response.status_code != 200:
            st.write("정보를 불러오는데 실패했습니다. 호출코드 :",response.status_code)
            return None
        
        xml = response.text
        root = BeautifulSoup(xml, 'lxml')
        
        items = root.find_all('item')
        
        for content in items :

            if not content.min1 or not content.station1:
                continue

            st.divider()
            st.write(f"버스 번호 : {content.lineno.text}")
            st.write(f"{content.min1.text}분 후 도착예정")
            st.write(f"버스가 {content.station1.text}정거장 전에 있습니다.")
            st.divider()
    except :
        st.warning("해당하는 정류장에 대한 정보가 없습니다.")
        st.warning("사유 : \n 1. 버스정보가 없을 경우\n2. 버스들이 오지 않을경우 (막차시간 지남)\n3. API서버에서 정보를 받아오지 못했을 경우(운영자에게 문의바람)")

def get_info_by_lineid(line_id):

    response = requests.get(f"http://apis.data.go.kr/6260000/BusanBIMS/busInfoByRouteId?lineid={line_id}&serviceKey={key}")
    
    if response.status_code != 200:
        st.write("정보를 불러오는데 실패했습니다")
        return None
    
    xml = response.text
    root = BeautifulSoup(xml, 'lxml')

    items = root.find_all('item')
    
    return items
        
def to_show_bus_info(list, bstopnm) : #바로 위에 함수에 넣어줄려고 만든 함수
    
    for content in list:
        if content.bstopnm.text == bstopnm :

            if not content.arsno.text:
                st.write("죄송합니다. 해당하는 정류소의 정보가 없습니다.")
                break 
            else :   
                arsno = content.arsno.text
                break
    
    get_info_by_arsno(arsno)
        
