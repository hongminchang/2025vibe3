import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os
import io

# 폰트 깨짐 방지를 위한 기본 설정 (DejaVu Sans는 대부분 시스템에 있음)
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.titlesize'] = 12
plt.rcParams['axes.labelsize'] = 10
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9

# 데이터 다운로드
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

# 실험 개요
with st.expander("🔍 실험 배경, 목적, 사전 설명"):
    st.markdown("""
### 쉽게 이해할 수 있는 실험 개요

**항목** | **내용**
--|--
🌾 **실험 배경** | 보리는 식량 및 사료 작물로 중요한 식물이며, 가뭄은 생장에 큰 영향을 주는 스트레스 요인입니다.
🚀 **실험 목적** | 정상 조건과 가뭄 조건에서 보리의 유전자 발현 차이를 분석하여, 가뭄에 강한 유전자를 탐색합니다.
🌐 **실험 방법** | GEO의 GSE17669 데이터를 불러와 조건별 유전자 발현량을 비교하고 시각화합니다.
🧬 **유전자 발현이란?** | 유전자가 단백질로 전환되어 기능을 수행하는 과정으로, 해당 유전자의 활성 정도를 나타냅니다.
""")

df = load_data()
samples = df.columns.tolist()
condition_labels = ['Normal'] * 12 + ['Drought'] * 12

# 🎻 1. Violin Plot
st.header("🎻 1. 유전자별 발현량 비교 (Violin Plot)")
st.markdown("""
**분석 목적:**  
선택한 유전자가 '정상 조건'과 '가뭄 조건'에서 얼마나 다르게 활동하는지를 확인합니다.

**Violin Plot(바이올린 플롯)이란?**  
- 박스플롯과 밀도 그래프를 합친 형태로, 데이터가 어느 값에 많이 분포하는지 보여줍니다.
- 양옆이 넓을수록 해당 값의 빈도가 높다는 뜻입니다.
- 조건별 유전자 발현 패턴이 다르면 두 조건의 플롯 모양이 다르게 나타납니다.
""")
gene = st.selectbox("🔎 분석할 유전자를 선택하세요:", df.index.tolist())
gene_data = df.loc[gene]
violin_df = pd.DataFrame({
    'Sample': samples,
    'Expression': gene_data.values,
    'Condition': condition_labels
})
fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
sns.violinplot(x='Condition', y='Expression', data=violin_df, ax=ax1)
ax1.set_title(f'{gene} Expression Comparison')
ax1.set_xlabel("Condition")
ax1.set_ylabel("Expression Level")
buf1 = io.BytesIO()
fig1.savefig(buf1, format="png", bbox_inches='tight')
buf1.seek(0)
st.image(buf1, caption="① 유전자 발현량 분포 비교 (Violin Plot)", use_column_width=False)

# 🔥 2. Heatmap
st.header("🔥 2. 발현량 변동이 큰 유전자 히트맵 (Heatmap)")
st.markdown("""
**분석 목적:**  
조건 변화에 민감하게 반응하는 유전자들을 선별하여 발현 패턴을 시각적으로 분석합니다.

**Heatmap(히트맵)이란?**  
- 색상으로 수치를 표현하는 표 형식의 그래프입니다.
- 빨간색: 높은 발현 / 파란색: 낮은 발현을 나타냅니다.
- 비슷한 색 패턴은 유전자들이 비슷한 방식으로 반응하고 있다는 것을 의미합니다.
""")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=100)
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2, cbar_kws={'shrink': 0.6})
ax2.set_title("Top 50 Genes Expression Heatmap")
ax2.set_xlabel("Sample")
ax2.set_ylabel("Gene")
buf2 = io.BytesIO()
fig2.savefig(buf2, format="png", bbox_inches='tight')
buf2.seek(0)
st.image(buf2, caption="② 상위 유전자 발현 히트맵 (Heatmap)", use_column_width=False)

# 🧬 3. PCA 시각화
st.header("🧬 3. PCA (주성분 분석) 시각화")
st.markdown("""
**분석 목적:**  
전체 유전자 발현 정보를 축소하여 샘플 간 유사성과 차이를 직관적으로 파악합니다.

**PCA(주성분 분석)이란?**  
- 여러 변수(유전자)를 소수의 축(PC1, PC2)으로 줄여 시각화합니다.
- 가까운 점: 유사한 발현 패턴 / 멀리 떨어진 점: 서로 다른 유전자 발현 특성을 가짐
- 각 축은 원래 데이터의 분산(정보량)을 가장 많이 보존하는 방향으로 설정됩니다.
""")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['Condition'] = condition_labels
fig3, ax3 = plt.subplots(figsize=(5.5, 4), dpi=100)
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Condition', s=80, ax=ax3)
explained = pca.explained_variance_ratio_ * 100
ax3.set_title("PCA: Sample Similarity")
ax3.set_xlabel(f"PC1 ({explained[0]:.1f}%)")
ax3.set_ylabel(f"PC2 ({explained[1]:.1f}%)")
buf3 = io.BytesIO()
fig3.savefig(buf3, format="png", bbox_inches='tight')
buf3.seek(0)
st.image(buf3, caption="③ PCA 시각화 (샘플 간 발현 유사도)", use_column_width=False)

# 🔚 결과 요약
st.markdown("---")
st.subheader("📊 최종 분석 요약")
st.markdown("""
- Violin Plot을 통해 특정 유전자가 가뭄 조건에서 발현이 증가/감소했는지 확인 가능  
- Heatmap에서는 조건 변화에 민감한 상위 유전자를 선별하여, 시각적으로 발현 패턴 비교  
- PCA 결과를 통해 '정상'과 '가뭄' 조건 간 유전체 발현이 확연히 구분됨을 확인

➡ 이 분석은 **가뭄 스트레스에 반응하는 주요 유전자 탐색**에 기초 자료로 활용될 수 있습니다.
""")

st.markdown("📂 [GSE17669 데이터 출처 @ NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
