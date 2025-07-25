import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os
import io

# 📌 한글 폰트 설정
plt.rcParams['font.family'] = 'NanumGothic'
plt.rcParams['axes.titlesize'] = 11
plt.rcParams['axes.labelsize'] = 9
plt.rcParams['xtick.labelsize'] = 8
plt.rcParams['ytick.labelsize'] = 8

# 📁 데이터 자동 다운로드
file_path = "GSE17669_series_matrix.txt.gz"
file_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17669/matrix/GSE17669_series_matrix.txt.gz"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(file_url, file_path)
    df = pd.read_csv(file_path, sep='\t', comment='!', skiprows=55, index_col=0)
    df.dropna(inplace=True)
    return df

# 🔧 페이지 설정
st.set_page_config(page_title="보리 유전자 발현 분석", layout="wide")
st.title("🌾 보리 유전자 발현 분석 (GSE17669)")
st.markdown("---")

# 🔍 배경 설명
with st.expander("🔬 실험 배경 및 목적"):
    st.markdown("""
**보리(Barley)**는 주요 곡물 작물로, 가뭄과 같은 환경 스트레스에 어떻게 반응하는지 유전자 수준에서 연구됩니다.  
이 실험(GSE17669)은 보리 식물을 정상 조건과 **가뭄 스트레스 조건**으로 나누고, 유전자 발현 데이터를 수집했습니다.

**분석 목적:**
- 스트레스에 민감한 유전자를 발굴
- 샘플 간 유사성 파악
- 환경 반응 메커니즘 탐색
""")

# 📊 데이터 로딩
df = load_data()
samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 스트레스'] * 12

# 🎻 바이올린 플롯
st.header("🎻 1. 유전자별 발현량 바이올린 플롯")
st.markdown("조건별 발현 분포 차이를 통해, 선택 유전자가 가뭄 스트레스에 민감한지 확인합니다.")

gene = st.selectbox("분석할 유전자를 선택하세요", df.index.tolist())
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
st.image(buf1, caption="바이올린 플롯", use_column_width=False)

# 🔥 히트맵
st.header("🔥 2. 유전자 발현 히트맵 (Top 50)")
st.markdown("가장 발현 변화가 큰 50개 유전자를 색상으로 표현합니다.")

top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=100)
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2, cbar_kws={'shrink': 0.6})
ax2.set_title("상위 50개 유전자 발현 히트맵")
buf2 = io.BytesIO()
fig2.savefig(buf2, format="png", bbox_inches='tight')
buf2.seek(0)
st.image(buf2, caption="히트맵", use_column_width=False)

# 🧬 PCA
st.header("🧬 3. 주성분 분석 (PCA) 시각화")
st.markdown("발현 패턴이 비슷한 샘플들이 가깝게 표현됩니다.")

pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['처리 조건'] = condition_labels

fig3, ax3 = plt.subplots(figsize=(5.5, 4), dpi=100)
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='처리 조건', s=80, ax=ax3)
ax3.set_title("PCA: 샘플 간 유사도 시각화")
buf3 = io.BytesIO()
fig3.savefig(buf3, format="png", bbox_inches='tight')
buf3.seek(0)
st.image(buf3, caption="PCA 플롯", use_column_width=False)

# 📎 마무리
st.markdown("---")
st.markdown("📂 데이터 출처: [GSE17669 (NCBI GEO)](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
st.markdown("🛠️ 사용 도구: Python, Streamlit, Matplotlib, Seaborn, Scikit-learn")
