import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울시 인구 분석", layout="wide")
st.title("📊 서울시 연령별 인구 시각화")

# 파일 업로드
total_file = st.file_uploader("▶ 합계.csv 파일 업로드", type="csv")
gender_file = st.file_uploader("▶ 남녀구분.csv 파일 업로드", type="csv")

if total_file and gender_file:
    # 파일 읽기
    df_total = pd.read_csv(total_file, encoding='cp949')
    df_gender = pd.read_csv(gender_file, encoding='cp949')

    # 서울시 전체만 추출 (구 제외)
    df_total_seoul = df_total[df_total['행정구역'].str.contains("서울특별시") & ~df_total['행정구역'].str.contains("구")]
    df_gender_seoul = df_gender[df_gender['행정구역'].str.contains("서울특별시") & ~df_gender['행정구역'].str.contains("구")]

    # 연령 컬럼
    age_columns = [col for col in df_total_seoul.columns if '계_' in col and '세' in col]
    age_labels = [col.split('_')[-1] for col in age_columns]

    # 남녀 컬럼
    male_columns = [col for col in df_gender_seoul.columns if '남_' in col and '세' in col]
    female_columns = [col for col in df_gender_seoul.columns if '여_' in col and '세' in col]
    age_labels_gender = [col.split('_')[-1] for col in male_columns]

    # 숫자 처리 함수
    def clean(series):
        return pd.to_numeric(series.fillna('0').astype(str).str.replace(',', ''), errors='coerce').fillna(0).astype(int)

    # 인구 수 추출
    total_counts = clean(df_total_seoul[age_columns].iloc[0])
    male_counts = clean(df_gender_seoul[male_columns].iloc[0])
    female_counts = clean(df_gender_seoul[female_columns].iloc[0])

    # 시각화 1: 전체 인구
    fig1 = go.Figure()
    fig1.add_trace(go.Bar(x=age_labels, y=total_counts, name='전체 인구', marker_color='indigo'))
    fig1.update_layout(title="서울시 전체 인구의 연령별 분포", xaxis_title="연령", yaxis_title="인구 수")

    # 시각화 2: 남녀 인구
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=age_labels_gender, y=male_counts, name='남성', marker_color='blue'))
    fig2.add_trace(go.Bar(x=age_labels_gender, y=female_counts, name='여성', marker_color='pink'))
    fig2.update_layout(title="서울시 남성과 여성 인구의 연령별 비교", xaxis_title="연령", yaxis_title="인구 수", barmode='group')

    # 출력
    st.plotly_chart(fig1, use_container_width=True)
    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("👆 좌측에서 두 CSV 파일을 업로드해주세요.")
