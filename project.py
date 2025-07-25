import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

# 데이터 다운로드 설정
file_path = "GSE17669_series_matrix.txt.gz"
file_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17669/matrix/GSE17669_series_matrix.txt.gz"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(file_url, file_path)
    df = pd.read_csv(file_path, sep='\t', comment='!', skiprows=55, index_col=0)
    df.dropna(inplace=True)
    return df

# 페이지 설정
st.set_page_config(page_title="보리 유전자 발현 분석", layout="wide")
st.title("🌾 보리 유전자 발현 분석 (GSE17669)")
st.markdown("---")

# 실험 개요 설명
with st.expander("🔍 실험 개요 및 배경 설명"):
    st.markdown("""
### 📌 연구 목적
보리 식물을 **가뭄 스트레스 조건**과 **정상 조건**으로 나누어 유전자 발현량을 측정하고,  
스트레스에 반응하는 유전자들을 발굴하는 것이 목적입니다.

### 🧪 데이터 정보
- GEO 데이터셋: GSE17669  
- 샘플 수: 24개 (정상 조건 12, 가뭄 조건 12)  
- 데이터 형식: 유전자 × 샘플의 발현 수치 행렬 (마이크로어레이 기반)
""")

# 데이터 불러오기
df = load_data()
samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 스트레스'] * 12

# 바이올린 플롯
st.header("🎻 1. 유전자별 발현량 바이올린 플롯")
st.markdown("특정 유전자의 발현량 분포를 조건별로 비교하여 시각화합니다.")
gene = st.selectbox("유전자를 선택하세요", df.index.tolist())
gene_data = df.loc[gene]
violin_df = pd.DataFrame({
    '샘플': samples,
    '발현량': gene_data.values,
    '처리 조건': condition_labels
})
fig1, ax1 = plt.subplots(figsize=(6, 4))  # 더 작고 보기 쉽게
sns.violinplot(x='처리 조건', y='발현량', data=violin_df, ax=ax1)
ax1.set_title(f'{gene} 유전자 발현 비교')
st.pyplot(fig1)

# 히트맵
st.header("🔥 2. 발현량 변화 큰 유전자 히트맵")
st.markdown("상위 50개의 발현 변화 큰 유전자들을 색상으로 비교합니다.")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(10, 8))  # 크기 줄임
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2, cbar_kws={'shrink': 0.5})
ax2.set_title("Top 50 유전자 발현 히트맵")
st.pyplot(fig2)

# PCA
st.header("🧬 3. 주성분 분석(PCA) 시각화")
st.markdown("유전자 전체 발현 패턴을 2차원으로 축소해 샘플 간 유사성을 시각화합니다.")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['처리 조건'] = condition_labels
fig3, ax3 = plt.subplots(figsize=(6, 5))  # 컴팩트하게
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='처리 조건', s=80, ax=ax3)
ax3.set_title("PCA: 샘플 간 유사도 분석")
st.pyplot(fig3)

# 출처
st.markdown("---")
st.markdown("📂 데이터 출처: [GSE17669 (NCBI GEO)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
st.markdown("🔧 분석 도구: Python · Pandas · Streamlit · Scikit-learn · Seaborn")
