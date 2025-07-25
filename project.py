import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import urllib.request
import os
import io

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
st.set_page_config(page_title="Barley Gene Expression Analysis", layout="wide")
st.title("🌾 Barley Gene Expression Analysis (GSE17669)")

# 실험 설명은 한글 유지
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

# Violin Plot
st.header("🎻 1. Gene Expression Distribution (Violin Plot)")
st.markdown("""
**Purpose:** Compare how a selected gene behaves under normal vs drought conditions.

**What is a Violin Plot?**  
- Combines a boxplot with a density plot.  
- Shows where expression values are concentrated.  
- Wider areas = more frequent values.

📌 Interpretation:  
- If the distribution under drought is higher → gene may be upregulated due to stress.
""")
gene = st.selectbox("🔎 Select a gene to visualize:", df.index.tolist())
gene_data = df.loc[gene]
violin_df = pd.DataFrame({
    'Sample': samples,
    'Expression': gene_data.values,
    'Condition': condition_labels
})
fig1, ax1 = plt.subplots(figsize=(5, 3), dpi=100)
sns.violinplot(x='Condition', y='Expression', data=violin_df, ax=ax1)
ax1.set_title(f'{gene} Expression by Condition')
ax1.set_xlabel("Condition")
ax1.set_ylabel("Expression Level")
buf1 = io.BytesIO()
fig1.savefig(buf1, format="png", bbox_inches='tight')
buf1.seek(0)
st.image(buf1, caption="① Gene expression by condition", use_column_width=False)

# Heatmap
st.header("🔥 2. Top Variable Genes Heatmap")
st.markdown("""
**Purpose:** Identify genes with large expression differences across conditions.

**What is a Heatmap?**  
- Color-coded matrix to show gene expression levels.  
- Rows = Genes, Columns = Samples.  
- Red = High expression / Blue = Low expression.

📌 Interpretation:  
- If color shifts by condition, gene likely responds to drought.
""")
top_var_genes = df.var(axis=1).sort_values(ascending=False).head(50).index
fig2, ax2 = plt.subplots(figsize=(8, 6), dpi=100)
sns.heatmap(df.loc[top_var_genes], cmap='coolwarm', ax=ax2, cbar_kws={'shrink': 0.6})
ax2.set_title("Top 50 Variable Genes Heatmap")
ax2.set_xlabel("Sample")
ax2.set_ylabel("Gene")
buf2 = io.BytesIO()
fig2.savefig(buf2, format="png", bbox_inches='tight')
buf2.seek(0)
st.image(buf2, caption="② Heatmap of top variable genes", use_column_width=False)

# PCA
st.header("🧬 3. PCA: Sample Similarity")
st.markdown("""
**Purpose:** Visualize how similar or different the overall gene expression patterns are between samples.

**What is PCA?**  
- Reduces thousands of gene values to 2 dimensions.  
- Each point = 1 sample.  
- Samples that cluster together have similar expression patterns.

📌 Interpretation:  
- If 'Normal' and 'Drought' samples form separate clusters → strong condition effect on gene expression.
""")
pca = PCA(n_components=2)
coords = pca.fit_transform(df.T)
pca_df = pd.DataFrame(coords, columns=['PC1', 'PC2'])
pca_df['Condition'] = condition_labels
fig3, ax3 = plt.subplots(figsize=(5.5, 4), dpi=100)
sns.scatterplot(data=pca_df, x='PC1', y='PC2', hue='Condition', s=80, ax=ax3)
explained = pca.explained_variance_ratio_ * 100
ax3.set_xlabel(f"PC1 ({explained[0]:.1f}%)")
ax3.set_ylabel(f"PC2 ({explained[1]:.1f}%)")
ax3.set_title("PCA of Samples")
buf3 = io.BytesIO()
fig3.savefig(buf3, format="png", bbox_inches='tight')
buf3.seek(0)
st.image(buf3, caption="③ PCA: sample clustering", use_column_width=False)

# Summary
st.markdown("---")
st.subheader("📊 Conclusion Summary")
st.markdown("""
1. The selected gene may show differential expression under drought stress.
2. The heatmap highlights genes with strong condition-based responses.
3. PCA confirms distinct overall patterns between normal and drought-treated samples.

➡ These results suggest that drought stress significantly alters gene expression in barley,  
   offering potential markers for drought-resilient breeding.
""")

st.markdown("📂 [Data Source: GSE17669 @ NCBI GEO](https://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE17669)")
