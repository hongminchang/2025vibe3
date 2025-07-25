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
🌾 **실험 배경** | 보리(Barley)는 식량 및 사료 작물로 중요한 식물이며, 가뭄은 생장에 큰 영향을 주는 스트레스 요인입니다. 가뭄 상황에서의 생존력은 유전자 수준에서의 적응과 관련이 있습니다.
🚀 **실험 목적** | 정상 조건과 가뭄 조건에서 보리의 유전자 발현 차이를 분석하여, 가뭄에 강한 유전자를 찾고 작물 품종 개선에 응용 가능한 정보를 얻습니다.
🌐 **실험 방법 요약** | NCBI GEO의 공개 데이터(GSE17669)를 활용하여 보리 샘플의 유전자 발현량 데이터를 수집하고, 다양한 시각화 기법을 통해 조건별 유전자 반응을 분석합니다.
🧬 **유전자 발현이란?** | 세포가 유전자의 정보를 바탕으로 단백질을 만들어내는 과정을 의미합니다. 어떤 유전자가 얼마나 활발하게 기능하는지를 나타내는 지표로 활용됩니다.
""")

# 데이터 로드
df = load_data()
samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 조건'] * 12

# 유전자 발현량 비교 시각화
st.header("🎻 1. 유전자별 발현량 비교 (Violin Plot)")
st.markdown("""
**분석 목적:** 특정 유전자가 가뭄에 반응하여 발현량이 증가하거나 감소하는지를 시각적으로 확인합니다.

**Violin Plot이란?**
- 박스플롯과 KDE(확률 밀도 함수)를 결합한 그래프입니다.
- 유전자 발현값이 어느 범위에 얼마나 몰려 있는지 확인할 수 있어 분포 파악에 용이합니다.
- 양쪽 날개가 대칭적으로 퍼져 있다면 정규분포에 가까운 데이터입니다.
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
**분석 목적:** 발현량의 변화가 큰 유전자들을 추려내어 어떤 유전자가 조건 변화(가뭄)에 민감하게 반응하는지를 확인합니다.

**히트맵이란?**
- 행과 열에 따라 색상을 매핑해 데이터를 시각적으로 표현한 그래프입니다.
- 색상으로 데이터의 크기를 직관적으로 표현할 수 있습니다.
- 붉은색은 발현량이 높은 유전자, 파란색은 발현량이 낮은 유전자를 나타냅니다.
- 유전자 간 유사한 반응 패턴을 확인하는 데 유용합니다.
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
**분석 목적:** 전체 유전자 발현 패턴을 축소하여 샘플 간의 유사성과 차이를 시각화합니다.

**PCA(주성분 분석)란?**
- 수천 개의 유전자 정보를 소수의 축으로 요약하는 기법입니다.
- 데이터의 분산이 가장 큰 방향을 찾아 새로운 축(주성분)으로 변환합니다.
- 서로 다른 조건의 샘플들이 다른 위치에 존재하면, 발현 양상이 다르다는 뜻입니다.
- 가까운 점들은 유사한 유전자 발현 패턴을 보입니다.
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
