import json
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')

# Load data
with open('DATASET/databot.json') as f:
    data = json.load(f)

# Ekstraksi fitur
features = ['kategori_hotel', 'klasifikasi_hotel', 'rating_hotel', 'fasilitas']

def combine_features(row):
    return ' '.join([str(row[feature]) for feature in features])

tfidf = TfidfVectorizer()
feature_matrix = tfidf.fit_transform([combine_features(row) for row in data])

# Fungsi untuk merekomendasikan hotel
def recommend_hotels(user_preference, num_recommendations=3):
    user_feature_matrix = tfidf.transform([user_preference])
    similarities = cosine_similarity(user_feature_matrix, feature_matrix)
    hotel_indices = similarities.argsort()[0][::-1][:num_recommendations]
    recommended_hotels = [data[idx] for idx in hotel_indices]
    return recommended_hotels

# Fungsi evaluasi model
def evaluate_model(user_queries, true_recommendations):
    mrr_total = 0
    for query, true_rec in zip(user_queries, true_recommendations):
        recommended_hotels = recommend_hotels(query)
        recommended_hotel_names = [hotel['nama_hotel'] for hotel in recommended_hotels]
        for rank, hotel_name in enumerate(recommended_hotel_names):
            if hotel_name in true_rec:
                mrr_total += 1 / (rank + 1)
                break
    mrr = mrr_total / len(user_queries)
    return mrr

# Contoh penggunaan evaluasi model
user_queries = [
    "hotel dengan kolam renang dan Wi-Fi gratis",
    "hotel dekat pantai dengan rating tinggi",
    "penginapan murah dengan sarapan gratis di Bandung"
]

true_recommendations = [
    ["Hotel A", "Hotel B", "Hotel C"],
    ["Hotel D", "Hotel E"],
    ["Hotel F", "Hotel G", "Hotel H"]
]

if __name__ == '__main__':
    mrr_score = evaluate_model(user_queries, true_recommendations)
    print(f"Mean Reciprocal Rank (MRR): {mrr_score}")
