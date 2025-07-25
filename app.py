import streamlit as st
import folium
from streamlit_folium import st_folium
import urllib.parse
import json

# 페이지 설정
st.set_page_config(page_title="📍 공유 가능한 북마크 지도", layout="wide")
st.title("📍 나만의 북마크 지도 만들기 & 공유하기")
st.markdown("장소를 북마크하고 친구와 공유할 수 있어요!")

# 북마크 디코딩 함수
def load_bookmarks_from_query():
    query_params = st.query_params  # Streamlit 1.30 이후 권장 방식
    if "data" in query_params:
        try:
            decoded_data = urllib.parse.unquote(query_params["data"])
            bookmarks = json.loads(decoded_data)
            return bookmarks
        except:
            st.warning("❌ 북마크 데이터를 불러오는 중 문제가 발생했습니다.")
            return []
    return []

# 세션 상태 초기화 (한 번만 실행)
if "bookmarks" not in st.session_state:
    st.session_state.bookmarks = load_bookmarks_from_query()

# 🧾 북마크 추가 폼
with st.form("add_bookmark_form"):
    st.subheader("➕ 북마크 추가하기")
    name = st.text_input("장소 이름")
    description = st.text_area("설명", height=60)
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("위도", format="%.6f")
    with col2:
        lon = st.number_input("경도", format="%.6f")
    submitted = st.form_submit_button("📍 북마크 추가")

    if submitted:
        if name.strip() and lat and lon:
            new_mark = {
                "name": name,
                "description": description,
                "lat": lat,
                "lon": lon
            }
            st.session_state.bookmarks.append(new_mark)
            st.success(f"✅ '{name}' 북마크가 추가되었습니다.")
        else:
            st.warning("⚠️ 모든 필드를 올바르게 입력해주세요.")

# 지도 초기 위치 설정
if st.session_state.bookmarks:
    last = st.session_state.bookmarks[-1]
    center = [last["lat"], last["lon"]]
else:
    center = [37.5665, 126.9780]  # 기본: 서울

# 지도 생성 및 마커 추가
m = folium.Map(location=center, zoom_start=12)
for mark in st.session_state.bookmarks:
    popup_html = f"<b>{mark['name']}</b><br>{mark['description']}"
    folium.Marker(
        [mark["lat"], mark["lon"]],
        tooltip=mark["name"],
        popup=popup_html,
        icon=folium.Icon(color="blue", icon="bookmark")
    ).add_to(m)

# 지도 표시
st_data = st_folium(m, height=600, width=1000)

# 북마크 목록 출력
if st.session_state.bookmarks:
    st.markdown("### 📌 북마크 목록")
    for i, bm in enumerate(st.session_state.bookmarks, 1):
        st.markdown(f"**{i}. {bm['name']}**  \n📍 ({bm['lat']}, {bm['lon']})  \n📝 {bm['description']}  \n---")

# 공유 링크 생성
if st.session_state.bookmarks:
    st.markdown("### 🔗 공유 링크 만들기")
    bookmark_json = json.dumps(st.session_state.bookmarks)
    encoded = urllib.parse.quote(bookmark_json)
    base_url = st.request.url.split("?")[0]
    share_link = f"{base_url}?data={encoded}"
    st.text_input("아래 링크를 복사하여 공유하세요:", value=share_link, label_visibility="collapsed")

# 초기화 버튼
if st.button("🗑️ 모든 북마크 삭제"):
    st.session_state.bookmarks = []
    st.success("모든 북마크가 삭제되었습니다.")
