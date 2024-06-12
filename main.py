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

st.title("버스 도착 정보시스템 😎")
st.divider()

kind = st.sidebar.selectbox("기능", ("정류장 정보", "버스 정보"))

if kind == '정류장 정보' :
    st.header("버스정류장 정보")
    st.text("원하는 정류장의 정보를 볼 수 있는 시스템이다.")
    bstop_name = st.selectbox("정류장을 입력해주세요.",data.Busan_bus_data_name, placeholder="정류장 이름을 입력해주세요...")

    if 'page' not in st.session_state:

        st.session_state.page = 0

    if bstop_name:
        gps_list = data.get_gps_list(bstop_name)

        st.write("위치를 골라주세요.")

        center = [gps_list[st.session_state.page][1], gps_list[st.session_state.page][0]]

        m = folium.Map(location=center, zoom_start=18)

        for [x, y] in gps_list :
            folium.Marker([y,x], tooltip="정류장", popup=f"{bstop_name}").add_to(m)

        selected = st_folium(m, width=700, height=500)

        if selected['last_object_clicked'] != None:
            selected_gpsy = selected['last_object_clicked']['lat']
            selected_gpsx = selected['last_object_clicked']['lng']

            bstop_id = data.find_bstop_by_gps(selected_gpsy, selected_gpsx)

            fc.get_info_by_id(bstop_id)

if kind == "버스 정보" :
    st.header("버스 정보🤩")
    st.text("원하는 버스의 정보를 볼 수 있는 시스템이다.")

    bus_num = st.text_input('버스 번호를 입력해주세요', 68, placeholder='번호를 입력하세요')

    if bus_num :
        try:
            bus_info = fc.get_bus_info_by_num(bus_num) #버스 정보를 받아오고

            lineid = bus_info['lineid'].text # 거기서 노선아이디를 받아온다음

            items = fc.get_info_by_lineid(lineid, bus_num) # 정류장들을 나열하고 item리스트를 받아온다.

            data.to_map_line(items, bus_num) #안에서 지도를 그린다.

        except : # 없는 버스 번호를 입력하였을때.
            st.error("해당하는 번호의 버스에 대한 내용이 없습니다.")

        

        

         



        

        








