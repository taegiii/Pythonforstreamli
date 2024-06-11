import streamlit as st
import pandas as pd
import numpy as np
import func as fc
import folium
from streamlit_folium import st_folium
import data


import requests
from bs4 import BeautifulSoup
import xmltodict #여기는 API서버에서 불러오고 데이터를 처리하는데 필요한 모듈

from func import get_bus_arrival_info

st.title("버스 도착 정보시스템 😎")
st.divider()

st.header("버스정류장 정보")
st.text("원하는 정류장의 정보를 볼 수 있는 시스템이다.")
bstop_name = st.selectbox("정류장을 입력해주세요.",data.Busan_bus_data_name, placeholder="정류장 이름을 입력해주세요...")

if 'page' not in st.session_state:
   st.session_state.page = 0

if bstop_name:
    gps_list = data.get_gps_list(bstop_name)

    if st.session_state.page < len(gps_list) :
        st.write('여기가 맞나요?')

        map_container = st.container()

        center = [gps_list[st.session_state.page][1], gps_list[st.session_state.page][0]]

        m = folium.Map(location=center, zoom_start=20)

        folium.Marker([gps_list[st.session_state.page][1], gps_list[st.session_state.page][0]], tooltip='정류장', popup=f'{bstop_name}').add_to(m)
        with map_container:
            st_folium(m, width=700, height=500)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("예"):
                map_container.empty()  # 지도 제거
                st.session_state.page = 0  # 초기화 또는 원하는 동작으로 설정
        with col2:
            if st.button("아니요"):
                st.session_state.page += 1  # 다음 정류장 정보로 이동
                st.experimental_rerun()  # 페이지 새로고침하여 다음 지도를 표시

    else:
        st.write("더 이상 정류장이 없습니다.")


         



        

        








