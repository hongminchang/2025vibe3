import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os

# 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'

# 파일 다운로드
file_path = "GSE17669_series_matrix.txt.gz"
file_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17669/matrix/GSE17669_series_matrix.txt.gz"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(file_url, file_path)
    df = pd.read_csv(file_path, sep='\t', comment='!', skiprows=55, index_col=0)
    df.dropna(inplace=True)
    return df

# 🏠 페이지 설정
st.set_page_config(page_title="보리 유전자 발현 분석", layout="wide")
st.title("🌾 보리 유전자 발현 분석 (GSE17669)")
st.markdown("---")

# 📘 실험 배경 설명
with st.expander("🔍 실험 개요 및 배경 설명"):
    st.markdown("""
### 📌 연구 주제
보리 식물은 대표적인 작물로, **가뭄 스트레스(drought stress)**는 생장과 생산성에 큰 영향을 미칩니다.  
이 연구에서는 보리 식물을 **정상 조건(대조군)**과 **가뭄 처리 조건(실험군)**으로 나누어,  
각각에서 유전자 발현량을 측정하여 **환경 스트레스에 반응하는 유전자들을 찾는 것**이 목적입니다.

### 🧪 실험 데이터 설명
- 데이터셋 이름: **GSE17669 (NCBI GEO)**
- 측정 방식: **마이크로어레이 실험**
- 샘플 수: 총 24개 (정상 조건 12개 + 가뭄 처리 조건 12개)
- 측정 대상: 수천 개의 유전자 발현 수치

### 🎯 분석 목적
- 어떤 유전자가 가뭄에 반응하는가?
- 조건에 따라 발현량이 얼마나 달라지는가?
- 전체 샘플들은 어떤 특징을 기준으로 그룹화되는가?
""")

# 데이터 불러오기
df = load_data()
samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 스트레스'] * 12

# 🎻 바이올린 플롯
st.header("🎻 1. 유전자별 발현량 바이올린 플롯")
st.markdown("""
특정 유전자 1개를 선택하여,  
**'정상 조건'과 '가뭄 스트레스 조건'에서 발현량 분포가 어떻게 다른지** 시각화합니다.

- **좁고 긴 분포**: 특정 샘플에서만 강하게 발현
- **넓은 분포**: 샘플 간 차이 큼
""")
gene = st.selectbox("유전자를 선택하세요", df.index.tolist())
gene_data = df.loc[gene]
violin_df = pd.DataFrame({
    '샘플': samples,
    '발현량': gene_data.values,
    '처리 조건': condition_labels
})
fig1, ax1 = plt.subplots()
sns.violinplot(x='처리 조건', y='발현량', data=violin_df, ax=ax1)
ax1.set_title(f'{gene} 유전자 발현량 비교')
st.pyplot(fig1)

# 🔥 히트맵
st.header("🔥 2. 발현량 변화 큰 유전자 히트맵")
st.markdown("""
**발현 변화가 큰 상위 50개 유전자**를 선별하여 그들의 발현량을 색상으로 표현합니다.  

- **빨간색**: 발현량이 높음  
- **파란색**: 발현량이 낮음  
- 열 = 샘플, 행 = 유전자  
""")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(12, 10))
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2)
ax2.set_title("Top 50 유전자 발현 히트맵")
st.pyplot(fig2)

# 🧬 PCA
st.header("🧬 3. 주성분 분석(PCA) 시각화")
st.markdown("""
전체 유전자 발현 패턴을 2차원으로 줄여서 샘플들을 시각화합니다.  
**유사한 발현 패턴을 가진 샘플끼리 가까이 위치**합니다.

- 같은 조건(색깔)이 뭉쳐있다면 → 유전자 발현 경향이 비슷하다는 의미!
""")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['처리 조건'] = condition_labels
fig3, ax3 = plt.subplots()
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='처리 조건', s=100, ax=ax3)
ax3.set_title("PCA: 샘플 간 유사도 분석")
st.pyplot(fig3)

# ✅ 출처 및 마무리
st.markdown("---")
st.markdown("📂 데이터 출처: [GSE17669 (NCBI GEO)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
st.markdown("🔧 분석 도구: Python · Pandas · Streamlit · Scikit-learn · Seaborn")
