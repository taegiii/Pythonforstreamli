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

    if bstop_name:
        try :
            gps_list = data.get_gps_list(bstop_name)

            st.write("위치를 골라주세요.")

            center = [gps_list[0][1], gps_list[0][0]]

            m = folium.Map(location=center, zoom_start=18)

            for [x, y] in gps_list :
                folium.Marker([y,x], tooltip="정류장", popup=f"{bstop_name}").add_to(m)

            selected = st_folium(m, width=700, height=500)

            if selected['last_object_clicked'] != None:
                selected_gpsy = selected['last_object_clicked']['lat']
                selected_gpsx = selected['last_object_clicked']['lng']

                bstop_id = data.find_bstop_by_gps(selected_gpsy, selected_gpsx)

                fc.get_info_by_id(bstop_id)
        except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            st.write("해당하는 정류장에 대한 정보가 없습니다.")
    

if kind == "버스 정보" :
    st.header("버스 정보🤩")
    st.text("원하는 버스의 정보를 볼 수 있는 시스템이다.")

    bus_num = st.text_input('버스 번호를 입력해주세요', placeholder='번호를 입력하세요')

    if bus_num :
        try:
            bus_info = fc.get_bus_info_by_num(bus_num) #버스 정보를 받아오고

            lineid = bus_info['lineid'] # 거기서 노선아이디를 받아온다음

            items = fc.get_info_by_lineid(lineid) # 정류장들을 나열하고 item리스트를 받아온다.

            data.to_map_pin(items, bus_num) #안에서 지도를 그린다.

            st.success(f"\'{bus_num}\'번 정차 정류소")

            bstop_list = []

            for i in items :
                bstop_list.append(i.bstopnm.text)

            bstopnm = st.radio(
                "정류장을 선택하면 도착정보가 표시됩니다.", bstop_list, index=None) #받아온 정류장들을 radio형식으로 띄운다.
            
            if bstopnm: #선택하면 해당하는 정류소의 도착정보를 볼 수 있도록 한다.
                    gps_list = data.get_gps_list(bstopnm)

                    center = [gps_list[0][1], gps_list[0][0]]

                    t = folium.Map(location=center, zoom_start=18)

                    for [x, y] in gps_list :
                            folium.Marker([y,x], tooltip="정류장", popup=f"{bstopnm}").add_to(t)
                    
                    st.write("알고싶은 정류장 위치를 골라주세요")
                    selected = st_folium(t, width=700, height=500)

                    if selected['last_object_clicked'] != None:
                        selected_gpsy = selected['last_object_clicked']['lat']
                        selected_gpsx = selected['last_object_clicked']['lng']

                        bstop_id = data.find_bstop_by_gps(selected_gpsy, selected_gpsx)

                        with st.expander(f"{bstopnm} 정류장의 도착정보입니다."):
                            st.write(f"{bstopnm} 정류장 도착 정보입니다.")

                            fc.get_info_by_id(bstop_id)
        except Exception as e:    # 모든 예외의 에러 메시지를 출력할 때는 Exception을 사용
            st.write("해당하는 버스에 대한 정보가 없습니다.")
    


       
            

        

        

         



        

        








