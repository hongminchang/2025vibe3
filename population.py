import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(page_title="서울시 인구 분석", layout="wide")
st.title("📊 서울시 연령별 인구 시각화")

# 파일 경로 (같은 디렉토리에 있어야 함)
TOTAL_PATH = "합계.csv"
GENDER_PATH = "남녀구분.csv"

try:
    # 파일 읽기
    df_total = pd.read_csv(TOTAL_PATH, encoding='cp949')
    df_gender = pd.read_csv(GENDER_PATH, encoding='cp949')

    # 서울시 전체만 추출
    df_total_seoul = df_total[df_total['행정구역'].str.contains("서울특별시") & ~df_total['행정구역'].str.contains("구")]
    df_gender_seoul = df_gender[df_gender['행정구역'].str.contains("서울특별시") & ~df_gender['행정구역'].str.contains("구")]

    # 연령별 컬럼 추출
    age_columns = [col for col in df_total_seoul.columns if '계_' in col and '세' in col]
    age_labels = [col.split('_')[-1] for col in age_columns]

    # 남녀 각각 컬럼
    male_columns = [col for col in df_gender_seoul.columns if '남_' in col and '세' in col]
    female_columns = [col for col in df_gender_seoul.columns if '여_' in col and '세' in col]
    age_labels_gender = [col.split('_')[-1] for col in male_columns]

    # 문자열 → 숫자 처리 함수
    def clean(series):
        return pd.to_numeric(series.fillna('0').astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)

    # 각 시리즈 정리
    total_counts = clean(df_total_seoul[age_columns].iloc[0])
    male_counts = clean(df_gender_seoul[male_columns].iloc[0])
    female_counts = clean(df_gender_seoul[female_columns].iloc[0])

    # 전체 인구 분포 시각화
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=age_labels, y=total_counts, name='전체 인구', marker_color='indigo'))
    fig1.update_layout(title="서울시 전체 인구의 연령별 분포", xaxis_title="연령", yaxis_title="인구 수")

    # 남녀 인구 분포 시각화
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=age_labels_gender, y=male_counts, name='남성', marker_color='blue'))
    fig2.add_trace(go.Bar(x=age_labels_gender, y=female_counts, name='여성', marker_color='pink'))
    fig2.update_layout(title="서울시 남성과 여성 인구의 연령별 비교", xaxis_title="연령", yaxis_title="인구 수", barmode='group')

    # 출력
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

except FileNotFoundError:
    st.error("❌ '합계.csv' 또는 '남녀구분.csv' 파일이 현재 디렉토리에 존재하지 않습니다.")
except Exception as e:
    st.error(f"⚠️ 오류 발생: {e}")
