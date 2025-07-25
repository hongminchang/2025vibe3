import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

st.title("🌾 보리 유전자 발현 분석 시각화")
st.markdown("데이터 출처: GSE17669 (가뭄 스트레스 실험)")

# 데이터 불러오기
df = pd.read_csv("GSE17669_series_matrix.txt.gz", sep='\t', comment='!', skiprows=55, index_col=0)
df.dropna(inplace=True)

samples = df.columns.tolist()
condition_labels = ['정상 조건'] * 12 + ['가뭄 스트레스'] * 12

st.subheader("📈 특정 유전자 바이올린 플롯")
gene = st.selectbox("유전자를 선택하세요", df.index.tolist())
gene_data = df.loc[gene]
violin_df = pd.DataFrame({
    '샘플': samples,
    '발현량': gene_data.values,
    '처리 조건': condition_labels
})
fig1 = sns.violinplot(x='처리 조건', y='발현량', data=violin_df)
st.pyplot(fig1.figure)

st.subheader("🔥 발현량 변화 큰 유전자 히트맵")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(12, 10))
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2)
st.pyplot(fig2)

st.subheader("🧬 PCA 시각화 (샘플 유사도)")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['처리 조건'] = condition_labels
fig3 = sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='처리 조건', s=100)
st.pyplot(fig3.figure)
