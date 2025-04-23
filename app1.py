import streamlit as st
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Load data
df = pd.read_csv('purchases.csv')
items_df = pd.read_csv('items.csv')  # Must have columns: item_id, item_name, image_path

# Create user-item matrix
user_item_matrix = df.pivot_table(index='user_id', columns='item_id', values='rating').fillna(0)

# Calculate similarity
item_similarity = cosine_similarity(user_item_matrix.T)
item_similarity_df = pd.DataFrame(item_similarity, index=user_item_matrix.columns, columns=user_item_matrix.columns)

# Recommendation function
def recommend_items(user_id, top_n=3):
    user_ratings = user_item_matrix.loc[user_id]
    liked_items = user_ratings[user_ratings > 3].index.tolist()
    recommended_scores = {}

    for item in liked_items:
        similar_items = item_similarity_df[item]
        for similar_item, similarity in similar_items.items():
            if similar_item not in liked_items:
                recommended_scores[similar_item] = recommended_scores.get(similar_item, 0) + similarity

    recommended_items = sorted(recommended_scores.items(), key=lambda x: x[1], reverse=True)
    return [item for item, _ in recommended_items[:top_n]]

#  Streamlit UI
st.set_page_config(page_title="Grocery Recommender", layout="wide")
st.title('🛒 Grocery Item Recommendation System')

user_id_input = st.text_input("Enter your User ID:", "Rez")

if user_id_input:
    recommendations = recommend_items(user_id_input)
    st.subheader(f"Top 3 recommendations for **{user_id_input}**:")

    cols = st.columns(3)  # 3-grid layout
    for idx, item_id in enumerate(recommendations):
        item_row = items_df[items_df['item_id'] == item_id].iloc[0]
        with cols[idx]:
            st.image(item_row['image_path'], width=200, caption=item_row['item_name'])
            st.markdown(f"<div style='text-align: center; font-weight: bold; font-size: 18px;'>{item_row['item_name']}</div>", unsafe_allow_html=True)
