import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os

# 🔧 한글 폰트 설정 (한글 깨짐 방지, Streamlit Cloud에서는 생략 가능)
plt.rcParams['font.family'] = 'NanumGothic'

# 📥 데이터 파일 경로 및 자동 다운로드
file_path = "GSE17669_series_matrix.txt.gz"
file_url = "https://ftp.ncbi.nlm.nih.gov/geo/series/GSE17nnn/GSE17669/matrix/GSE17669_series_matrix.txt.gz"

@st.cache_data
def load_data():
    if not os.path.exists(file_path):
        urllib.request.urlretrieve(file_url, file_path)
    df = pd.read_csv(file_path, sep='\t', comment='!', skiprows=55, index_col=0)
    df.dropna(inplace=True)
    return df

# 🔍 페이지 제목
st.set_page_config(page_title="보리 유전자 발현 분석", layout="wide")
st.title("🌾 보리 유전자 발현 분석 (GSE17669)")
st.markdown("공공 데이터 GSE17669를 이용한 가뭄 스트레스 유전자 반응 분석")

# 📊 데이터 불러오기
df = load_data()
samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 스트레스'] * 12

# 🎻 바이올린 플롯
st.subheader("🎻 유전자별 발현량 바이올린 플롯")
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
st.subheader("🔥 발현량 변화 큰 유전자 히트맵 (Top 50)")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(12, 10))
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2)
ax2.set_title("Top 50 유전자 발현 히트맵")
st.pyplot(fig2)

# 🧬 PCA 시각화
st.subheader("🧬 주성분 분석 (PCA)")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['처리 조건'] = condition_labels
fig3, ax3 = plt.subplots()
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='처리 조건', s=100, ax=ax3)
ax3.set_title("PCA로 본 샘플 간 유사도")
st.pyplot(fig3)

# ✅ 출처 정보
st.markdown("---")
st.markdown("🔗 데이터 출처: [GSE17669 @ NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
