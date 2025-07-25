import streamlit as st
import folium
from streamlit_folium import st_folium

# 페이지 설정
st.set_page_config(page_title="📍 나만의 북마크 지도", layout="wide")

st.title("📍 나만의 북마크 지도 만들기")
st.markdown("원하는 장소를 북마크하여 지도에 표시해보세요!")

# 세션 상태 초기화
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = []

# 입력 폼
with st.form("bookmark_form"):
    st.subheader("➕ 장소 추가")
    name = st.text_input("장소 이름")
    description = st.text_area("설명", height=70)
    lat = st.number_input("위도", format="%.6f")
    lon = st.number_input("경도", format="%.6f")
    submitted = st.form_submit_button("추가하기")

    if submitted:
        if name and lat and lon:
            st.session_state.bookmarks.append({
                "name": name,
                "description": description,
                "lat": lat,
                "lon": lon
            })
            st.success(f"✅ '{name}' 장소가 지도에 추가되었습니다!")
        else:
            st.error("⚠️ 장소 이름과 좌표를 모두 입력해주세요.")

# 지도 생성
m = folium.Map(location=[37.5665, 126.9780], zoom_start=12)  # 기본 위치: 서울

# 북마크 마커 추가
for bm in st.session_state.bookmarks:
    popup_content = f"<b>{bm['name']}</b><br>{bm['description']}"
    folium.Marker(
        location=[bm["lat"], bm["lon"]],
        popup=popup_content,
        tooltip=bm["name"],
        icon=folium.Icon(color="blue", icon="info-sign")
    ).add_to(m)

# 지도 표시
st_folium(m, width=1000, height=600)

# 북마크 리스트
if st.session_state.bookmarks:
    st.markdown("### 📌 북마크 목록")
   for i in range(len(my_list)):
    print(i)
