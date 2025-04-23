#Importing the python library
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd


#Loading the datasets
df = pd.read_csv("purchases.csv")

#Showing the data
#print("Purchase History")
#print(df)


user_item_matrix = df.pivot_table(index='user_id',columns= 'item_id',values='rating').fillna(0)
#Showing the user item matrix

print("user_item_matrix:")
print(user_item_matrix)


#Calculating the cosine similarities between the items
item_similarity = cosine_similarity(user_item_matrix.T)


#Converting similarity matrix to Dataframe for easier viewing
item_similarity_df = pd.DataFrame(item_similarity, index = user_item_matrix.columns ,columns = user_item_matrix.columns)

#Showing the item_similarity matrix
print("\n Item Similarity Matrix:")
print(item_similarity_df)


# Function to recommend items based on user preferences
def recommend_items(user_id, user_item_matrix, item_similarity_df, top_n=3):
    user_ratings = user_item_matrix.loc[user_id]  # Get the items that the user has rated
    liked_items = user_ratings[user_ratings > 3].index.tolist()  # Items rated greater than 3

    # Creating an empty dictionary to store the recommendation scores
    recommended_scores = {}

    # For each liked item, check the similarity with other items
    for item in liked_items:
        # Get the similarity of the current item with all other items
        similar_items = item_similarity_df[item]

        # For each similar item, update the recommended score
        for similar_item, similarity in similar_items.items():
            if similar_item not in liked_items:  # Exclude already liked items
                if similar_item not in recommended_scores:
                    recommended_scores[similar_item] = 0
                recommended_scores[similar_item] += similarity

    # Sort the recommended items by score in descending order
    recommended_items = sorted(recommended_scores.items(), key=lambda x: x[1], reverse=True)

    # Get top N recommendations
    top_recommendations = recommended_items[:top_n]

    return top_recommendations

# Example: Recommend items for user 'u1'
user_id = 'u1'  # Change this to the user you want to recommend items for
recommended_items_u1 = recommend_items(user_id, user_item_matrix, item_similarity_df, top_n=3)

# Printing the recommendations
print(f"\nRecommendations for User {user_id}:")
for item, score in recommended_items_u1:
    print(f"Item: {item}, Similarity Score: {score}")

# Function to get top-N item recommendations for a given user
def get_item_recommendations(user_id, user_item_matrix, item_similarity_df, top_n=3):
    user_ratings = user_item_matrix.loc[user_id]
    user_unrated_items = user_ratings[user_ratings == 0].index
    scores = {}

    for item in user_unrated_items:
        similar_item = item_similarity_df[item]
        user_rated = user_ratings[user_ratings > 0]
        score = sum(similar_item[user_rated.index] * user_rated)
        scores[item] = score

    sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    recommendations = [item for item, score in sorted_scores[:top_n]]
    return recommendations

# Showing the recommendations for user u1
user_id = "u1"
recommendations = get_item_recommendations(user_id, user_item_matrix, item_similarity_df)
print(f"\nTop-N Recommendations for User {user_id}: {recommendations}")

#Showing the recommendations for user u2
user_id = "u2"
recommendations = get_item_recommendations(user_id, user_item_matrix, item_similarity_df)
print(f"\nTop-N Recommendations for User {user_id}:{recommendations}")

