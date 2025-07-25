import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os
import io

# 시각화에서 한글 폰트 제거 (깨짐 방지)
plt.rcParams['font.family'] = 'DejaVu Sans'

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

# 설명
with st.expander("🔍 실험 배경 및 설명"):
    st.markdown("""
**프로젝트 설명**  
보리 유전자 발현 데이터를 바탕으로 정상 조건과 가뭄 조건 간의 유전적 반응 차이를 분석하고, 이를 시각화(PCA, 히트맵 등)하여 조건에 따른 유전자 표현 차이를 파악함.

**데이터 출처**  
- GEO Dataset ID: GSE17669
- 샘플 수: 24개 (정상 12, 가뭄 12)
""")

df = load_data()
samples = df.columns.tolist()
condition_labels = ['Normal'] * 12 + ['Drought'] * 12

# 1. Violin Plot
st.header("🎻 1. 유전자별 발현량 비교")
gene = st.selectbox("🔎 분석할 유전자를 선택하세요:", df.index.tolist())
gene_data = df.loc[gene]
violin_df = pd.DataFrame({
    'Sample': samples,
    'Expression': gene_data.values,
    'Condition': condition_labels
})
fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
sns.violinplot(x='Condition', y='Expression', data=violin_df, ax=ax1)
ax1.set_title(f'{gene} Expression Comparison')  # 영어로 수정
ax1.set_xlabel("Condition")
ax1.set_ylabel("Expression Level")
buf1 = io.BytesIO()
fig1.savefig(buf1, format="png", bbox_inches='tight')
buf1.seek(0)
st.image(buf1, caption="① 유전자 발현량 분포 비교", use_column_width=False)

# 2. Heatmap
st.header("🔥 2. 발현량 변동 큰 유전자 히트맵")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=100)
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2, cbar_kws={'shrink': 0.6})
ax2.set_title("Top 50 Genes Expression Heatmap")  # 영어로 수정
ax2.set_xlabel("Sample")
ax2.set_ylabel("Gene")
buf2 = io.BytesIO()
fig2.savefig(buf2, format="png", bbox_inches='tight')
buf2.seek(0)
st.image(buf2, caption="② 상위 유전자 발현 히트맵", use_column_width=False)

# 3. PCA
st.header("🧬 3. PCA (주성분 분석)")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['Condition'] = condition_labels
fig3, ax3 = plt.subplots(figsize=(5.5, 4), dpi=100)
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Condition', s=80, ax=ax3)
explained = pca.explained_variance_ratio_ * 100
ax3.set_title("PCA: Sample Similarity")  # 영어로 수정
ax3.set_xlabel(f"PC1 ({explained[0]:.1f}%)")
ax3.set_ylabel(f"PC2 ({explained[1]:.1f}%)")
buf3 = io.BytesIO()
fig3.savefig(buf3, format="png", bbox_inches='tight')
buf3.seek(0)
st.image(buf3, caption="③ PCA 시각화", use_column_width=False)

# 최종 요약
st.markdown("---")
st.subheader("📊 최종 분석 결론")
st.markdown("""
- 선택 유전자가 가뭄 조건에서 발현 차이를 보이면, 스트레스 반응 유전자로 작용할 가능성이 있음  
- 히트맵을 통해 조건 변화에 민감한 유전자 패턴을 시각적으로 확인  
- PCA 분석 결과, 두 조건 간 유전자 발현 양상이 뚜렷이 구분됨 → 유전체 수준에서 반응 차이 존재

➡ 이 결과는 보리의 **가뭄 저항성 품종 개발에 활용 가능한 유전자 탐색**에 기초 자료로 활용될 수 있습니다.
""")

st.markdown("📂 [데이터 출처: NCBI GEO GSE17669](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
