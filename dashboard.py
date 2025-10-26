import streamlit as st
import pandas as pd
import plotly.express as px
import json
import numpy as np

st.title("Reddit Comments Analysis Dashboard")


@st.cache_data
def load_data():
    df = pd.read_parquet("deduped_analysis.parquet")
    df['mentions'] = df['mentions'].apply(lambda x: x if isinstance(x, dict) else {
                                          'brands': [], 'products': []})
    return df


df = load_data()

# Sidebar filters (from local df)
subreddits = sorted(df['subreddit'].unique().tolist())
subreddit = st.sidebar.selectbox("Subreddit", ['All'] + subreddits)
sentiment = st.sidebar.selectbox("Sentiment", sorted(
    df['sentiment_label'].unique().tolist()))
min_enth = st.sidebar.slider("Min Enthusiasm", 0.0, 1.0, 0.0)

# Filter data
filtered_df = df[df['subreddit'] == subreddit] if subreddit != 'All' else df
filtered_df = filtered_df[(filtered_df['sentiment_label'] == sentiment) & (
    filtered_df['enthusiasm'] >= min_enth)]

st.sidebar.info(
    f"Loaded {len(filtered_df)} comments from {len(filtered_df['subreddit'].unique())} subreddits")

# Metrics (fixed: convert NumPy to list before +)


def safe_mention_count(x):
    brands = x.get('brands', []) if isinstance(x.get('brands', []), list) else x.get(
        'brands', []).tolist() if hasattr(x.get('brands', []), 'tolist') else []
    products = x.get('products', []) if isinstance(x.get('products', []), list) else x.get(
        'products', []).tolist() if hasattr(x.get('products', []), 'tolist') else []
    return len(brands + products)


col1, col2, col3 = st.columns(3)
col1.metric("Comments", len(filtered_df))
col2.metric("Avg Enthusiasm", filtered_df['enthusiasm'].mean().round(2))
col3.metric("Unique Mentions", filtered_df['mentions'].apply(
    safe_mention_count).sum())

st.subheader("Top Mentions")
all_mentions = []
for sublist in filtered_df['mentions']:
    brands = sublist.get('brands', []) if isinstance(sublist.get('brands', []), list) else sublist.get(
        'brands', []).tolist() if hasattr(sublist.get('brands', []), 'tolist') else []
    products = sublist.get('products', []) if isinstance(sublist.get('products', []), list) else sublist.get(
        'products', []).tolist() if hasattr(sublist.get('products', []), 'tolist') else []
    all_mentions.extend(brands + products)
mention_counts = pd.Series(all_mentions).value_counts().head(10)
fig2 = px.bar(y=mention_counts.index, x=mention_counts.values,
              orientation='h', title='Top Mentions')
st.plotly_chart(fig2)

st.subheader("Enthusiasm by Subreddit")
sub_enth = filtered_df.groupby(
    'subreddit')['enthusiasm'].mean().sort_values(ascending=False).head(10)
fig3 = px.bar(y=sub_enth.index, x=sub_enth.values,
              title='Avg Enthusiasm by Subreddit')
st.plotly_chart(fig3)

# Sample
st.subheader("Sample Comments")
st.dataframe(filtered_df[['cleaned', 'enthusiasm',
             'mentions', 'dedupe_score', 'subreddit']].head(5))
