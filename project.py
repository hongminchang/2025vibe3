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

# Streamlit 페이지 설정
st.set_page_config(page_title="보리 유전자 발현 분석", layout="wide")
st.title("🌾 보리 유전자 발현 분석 (GSE17669)")

# 실험 배경과 설명
with st.expander("🔍 실험 배경, 목적, 사전 설명"):
    st.markdown("""
### 📘 실험 개요

**항목** | **내용**
--|--
🌾 **실험 배경** | 보리는 주요 곡물 작물로, 가뭄에 강한 품종 개발이 매우 중요합니다. 식물의 생존력은 유전자 수준에서 결정되기 때문에 유전자 발현 분석이 필요합니다.
🚀 **실험 목적** | 보리를 정상 조건과 가뭄 조건으로 나눠 유전자 발현을 비교하고, 가뭄 스트레스에 민감하게 반응하는 유전자를 찾는 것이 목적입니다.
🌐 **데이터 출처** | NCBI GEO의 공개 데이터셋 GSE17669 (보리 샘플 총 24개, 12개는 정상, 12개는 가뭄)
🧬 **유전자 발현이란?** | 유전자가 단백질을 만들어내는 활동 정도를 의미합니다. 많이 발현될수록 활발히 기능하고 있는 것입니다.
""")

# 데이터 로드
df = load_data()
samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 조건'] * 12

# 1. 바이올린 플롯
st.header("🎻 1. 유전자별 발현량 비교 (Violin Plot)")
st.markdown("""
**목적:** 선택한 유전자가 '정상 조건'과 '가뭄 조건'에서 얼마나 다르게 활동하는지 확인합니다.

**Violin Plot이란?**  
- 유전자 발현값의 분포를 시각적으로 보여줍니다.  
- 진짜 '바이올린'처럼 생겼다고 해서 붙여진 이름이에요.  
- 중간 선은 중간값, 양옆 넓이는 값이 많이 몰려 있는 곳을 뜻해요.  
- 조건에 따라 위로 올라가면 발현량이 높다는 뜻이에요!

📌 해석 팁:  
- 가뭄 조건 쪽이 위로 길거나 더 넓다면 → 발현 증가 → 스트레스 반응 유전자일 가능성!
""")
gene = st.selectbox("🔎 분석할 유전자를 선택하세요:", df.index.tolist())
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
st.image(buf1, caption="① 선택 유전자 발현량 비교", use_column_width=False)

# 2. 히트맵
st.header("🔥 2. 발현량 변동 큰 유전자 히트맵")
st.markdown("""
**목적:** 발현 변화가 큰 유전자들을 색상으로 표현해 조건별 반응을 확인합니다.

**히트맵이란?**  
- 데이터 값의 크기를 색으로 보여주는 그래프예요.  
- **빨간색**: 발현량 높음 / **파란색**: 발현량 낮음  
- 세로축: 유전자 / 가로축: 샘플

📌 해석 팁:  
- 특정 유전자가 조건마다 확연히 색이 다르면 → 가뭄 반응 유전자일 가능성!
""")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=100)
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2, cbar_kws={'shrink': 0.6})
ax2.set_title("Top 50 유전자 발현 히트맵")
buf2 = io.BytesIO()
fig2.savefig(buf2, format="png", bbox_inches='tight')
buf2.seek(0)
st.image(buf2, caption="② 상위 발현 변화 유전자 히트맵", use_column_width=False)

# 3. PCA 시각화
st.header("🧬 3. PCA(주성분 분석) 시각화")
st.markdown("""
**목적:** 전체 유전자 발현 패턴을 축소해 샘플 간 유사성을 시각화합니다.

**PCA란? (Principal Component Analysis)**  
- 유전자 수천 개의 정보를 2개의 축으로 요약합니다.  
- 점 하나 = 보리 샘플 하나  
- 같은 조건의 샘플들이 가까이 모이면 → 발현 패턴이 비슷하다는 뜻입니다!

📌 해석 팁:  
- '정상 조건'과 '가뭄 조건' 점들이 확연히 떨어져 있다면 → 조건에 따라 유전자 발현 패턴이 다르다는 뜻입니다.
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
st.image(buf3, caption="③ 유전자 발현 패턴 비교 (PCA)", use_column_width=False)

# 결론 요약
st.markdown("---")
st.subheader("📊 최종 분석 결론 요약")
st.markdown("""
1. **선택 유전자**가 가뭄 조건에서 확연히 다른 발현량을 보이면, 이는 가뭄에 민감하게 반응하는 유전자로 추정됩니다.
2. **히트맵**을 통해 조건 변화에 민감한 유전자들이 색상 차이로 나타났습니다.
3. **PCA**에서 샘플들이 조건별로 잘 구분된다면, 전체적으로 유전자 발현 패턴이 조건에 따라 달라진다는 뜻입니다.

👉 결론적으로, **가뭄 스트레스는 보리의 유전자 발현에 큰 영향을 미쳤으며**,  
이 데이터를 통해 **가뭄에 강한 유전자 후보를 발굴**할 수 있습니다.
""")

# 출처
st.markdown("📂 [GSE17669 데이터 출처 @ NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
st.markdown("🛠️ 분석 도구: Python, Streamlit, Pandas, Seaborn, Scikit-learn")
