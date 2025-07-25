import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os
import io

# 한국어 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

# 데이터 다운로드 파일 설정
file_path = "GSE17669_series_matrix.txt.gz"
file_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17669/matrix/GSE17669_series_matrix.txt.gz"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(file_url, file_path)
    df = pd.read_csv(file_path, sep='\t', comment='!', skiprows=55, index_col=0)
    df.dropna(inplace=True)
    return df

# Streamlit 페이지 설정
st.set_page_config(page_title="보리 유전자 발현 분석", layout="wide")
st.title("🌾 보리 유전자 발현 분석 (GSE17669)")

# 실험 배경과 설명
with st.expander("🔍 실험 배경, 목적, 사전 설명"):
    st.markdown("""
### 쉽게 이해할 수 있는 실험 개요

**항목** | **내용**
--|--
🌾 **실험 배경** | 보리(Barley)는 식량 및 사료 작물로 중요한 식물이며, 가뭄은 생장에 큰 영향을 주는 스트레스 요인입니다.
🚀 **실험 목적** | 정상 조건과 가뭄 조건에서 보리의 유전자 발현 차이를 파악하여 가뭄 저항 유전자를 탐색합니다.
🌐 **실험 방법 요약** | NCBI GEO의 공개 데이터(GSE17669)를 활용해 보리 유전자의 발현량을 수집하고, 시각화를 통해 가뭄 스트레스에 반응하는 유전자를 분석합니다.
""")

# 데이터 로드
df = load_data()
samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 조건'] * 12

# 유전자 발현량 비교 시각화
st.header("🎻 1. 유전자별 발현량 비교 (Violin Plot)")
st.markdown("""
**목적:** 특정 유전자가 가뭄에 영향을 받는지를 시각적으로 확인합니다.
- 분포가 뚜렷이 다르면 스트레스 반응 유전자일 수 있습니다.
""")
gene = st.selectbox("비교할 유전자를 선택하세요:", df.index.tolist())
gene_data = df.loc[gene]
violin_df = pd.DataFrame({
    '샘플': samples,
    '발현량': gene_data.values,
    '처리 조건': condition_labels
})
fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
sns.violinplot(x='처리 조건', y='발현량', data=violin_df, ax=ax1)
ax1.set_title(f'{gene} 유전자 발현 비교')
buf1 = io.BytesIO()
fig1.savefig(buf1, format="png", bbox_inches='tight')
buf1.seek(0)
st.image(buf1, caption="유전자 발현량 분포 비교 (Violin Plot)", use_column_width=False)

# 히트맵 시각화
st.header("🔥 2. 발현 변동이 큰 유전자 히트맵")
st.markdown("""
**목적:** 발현량 변화가 큰 유전자들을 한눈에 비교하여 가뭄 반응 후보 유전자를 탐색합니다.
- 붉은색: 발현량 높음
- 파란색: 발현량 낮음
""")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=100)
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2, cbar_kws={'shrink': 0.6})
ax2.set_title("Top 50 유전자 발현 히트맵")
buf2 = io.BytesIO()
fig2.savefig(buf2, format="png", bbox_inches='tight')
buf2.seek(0)
st.image(buf2, caption="상위 유전자 발현 히트맵", use_column_width=False)

# PCA 시각화
st.header("🧬 3. PCA(주성분 분석) 시각화")
st.markdown("""
**목적:** 전체 유전자 발현 패턴을 2차원으로 축소하여 샘플 간 유사성 분석
- 가까운 점일수록 유사한 발현 패턴
""")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['처리 조건'] = condition_labels
fig3, ax3 = plt.subplots(figsize=(5.5, 4), dpi=100)
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='처리 조건', s=80, ax=ax3)
explained = pca.explained_variance_ratio_ * 100
ax3.set_xlabel(f"PC1 ({explained[0]:.1f}%)")
ax3.set_ylabel(f"PC2 ({explained[1]:.1f}%)")
ax3.set_title("PCA: 샘플 간 유사도 시각화")
buf3 = io.BytesIO()
fig3.savefig(buf3, format="png", bbox_inches='tight')
buf3.seek(0)
st.image(buf3, caption="PCA 시각화 (유사도 시각 표현)", use_column_width=False)

# 출처 및 정보
st.markdown("---")
st.markdown("📂 [GSE17669 데이터 출처 @ NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
st.markdown("🛠️ 분석 도구: Python, Streamlit, Pandas, Seaborn, Scikit-learn")
