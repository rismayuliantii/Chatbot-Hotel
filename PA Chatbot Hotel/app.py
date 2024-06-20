import pickle
from flask import Flask, render_template, request, jsonify
import json
import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random

nltk.download('punkt')

app = Flask(__name__)

# Load data
with open('DATASET/databot.json') as f:
    data = json.load(f)

# Ekstraksi semua lokasi unik dari dataset
def get_unique_locations(data):
    locations = set()
    for hotel in data:
        alamat = hotel.get('alamat', '').lower()
        for token in word_tokenize(alamat):
            locations.add(token)
    return locations

unique_locations = get_unique_locations(data)

# Ekstraksi fitur
features = ['kategori_hotel', 'klasifikasi_hotel', 'rating_hotel', 'fasilitas']

# Gabung fitur-fitur teks menjadi satu teks
def combine_features(row):
    return ' '.join([str(row[feature]) for feature in features])

# Buat matriks fitur
tfidf = TfidfVectorizer()
feature_matrix = tfidf.fit_transform([combine_features(row) for row in data])

# Fungsi untuk merekomendasikan hotel
def recommend_hotels(user_preference, num_recommendations=3):
    # Ekstraksi fitur dari preferensi pengguna
    user_feature_matrix = tfidf.transform([user_preference])

    # Hitung kemiripan antara preferensi pengguna dengan setiap hotel
    similarities = cosine_similarity(user_feature_matrix, feature_matrix)

    # Urutkan indeks hotel berdasarkan kemiripan
    hotel_indices = similarities.argsort()[0][::-1][:num_recommendations]

    # Ambil data hotel yang direkomendasikan
    recommended_hotels = [data[idx] for idx in hotel_indices]

    return recommended_hotels

# Fungsi untuk memberikan respons chatbot
def chatbot_response(user_input):
    # Tokenisasi kalimat pengguna
    tokens = word_tokenize(user_input.lower())
    
    # Identifikasi preferensi pengguna
    user_preference = ' '.join(tokens)
    
    recommended_hotels = recommend_hotels(user_preference)
    
    responses = [
        "Berikut adalah rekomendasi hotel untuk Anda:\n",
        "Ini adalah beberapa pilihan hotel yang mungkin Anda sukai:\n",
        "Saya telah menemukan beberapa hotel yang cocok untuk Anda:\n"
    ]
    
    response = random.choice(responses)  # Memilih respons secara acak dari daftar respons yang tersedia
  
     # Memperbaiki jumlah hotel yang ditampilkan
    max_hotels = 3
    recommended_hotels = recommended_hotels[:max_hotels]

    response = "\nBerikut adalah rekomendasi hotel untuk Anda:\n"
    for idx, hotel in enumerate(recommended_hotels, 1):
        response += f"{idx}. {hotel['nama_hotel']}\n"
        response += f"   Kategori: {hotel['kategori_hotel']}, Klasifikasi: {hotel['klasifikasi_hotel']}\n"
        response += f"   Rating: {hotel['rating_hotel']}\n"
        response += f"   Alamat: {hotel['alamat']}\n"
        response += f"   Harga: Rp {hotel['range_harga']['min']:,} - Rp {hotel['range_harga']['max']:,}\n"
        response += f"   Fasilitas: {', '.join(hotel['fasilitas'])}\n\n"
    
    return response


# Fungsi untuk memberikan rekomendasi hotel berdasarkan lokasi
def extract_criteria(user_input):
    criteria = {}
    tokens = word_tokenize(user_input.lower())

    for idx, token in enumerate(tokens):
        if token == "lokasi":
            criteria['lokasi'] = tokens[idx + 2] if idx + 2 < len(tokens) else None
        elif token == "fasilitas":
            criteria['fasilitas'] = tokens[idx + 2:] if idx + 2 < len(tokens) else None
        elif token == "harga":
            min_price_idx = idx + 2 if idx + 2 < len(tokens) and tokens[idx + 2].isdigit() else None
            max_price_idx = idx + 4 if idx + 4 < len(tokens) and tokens[idx + 4].isdigit() else None
            min_price = int(tokens[min_price_idx]) if min_price_idx is not None else None
            max_price = int(tokens[max_price_idx]) if max_price_idx is not None else None
            criteria['harga'] = {'min': min_price, 'max': max_price}
        elif token == "rating":
            criteria['rating'] = float(tokens[idx + 2]) if idx + 2 < len(tokens) and tokens[idx + 2].replace('.', '').isdigit() else None

    return criteria

# Fungsi untuk memberikan rekomendasi hotel berdasarkan kriteria
def recommend_hotels_response(criteria):
    location = criteria.get('lokasi')
    facilities = criteria.get('fasilitas')
    price_range = criteria.get('harga')
    rating = criteria.get('rating')

    filtered_hotels = data

    if location:
        filtered_hotels = [hotel for hotel in filtered_hotels if location.lower() in hotel['alamat'].lower()]
    
    if facilities:
        for facility in facilities:
            filtered_hotels = [hotel for hotel in filtered_hotels if facility.lower() in hotel['fasilitas'].lower()]
    
    if price_range:
        min_price = price_range.get('min', 0)
        max_price = price_range.get('max', float('inf'))
        filtered_hotels = [hotel for hotel in filtered_hotels if min_price <= hotel['range_harga']['min'] <= max_price]

    if rating:
        filtered_hotels = [hotel for hotel in filtered_hotels if hotel['rating_hotel'] >= rating]

    if not filtered_hotels:
        return "Maaf, tidak ada hotel yang sesuai dengan kriteria yang Anda masukkan."

    response = "Berikut adalah beberapa hotel yang sesuai dengan kriteria Anda:\n"
    for idx, hotel in enumerate(filtered_hotels, 1):
        response += f"{idx}. {hotel['nama_hotel']}\n"
        response += f"   Kategori: {hotel['kategori_hotel']}, Klasifikasi: {hotel['klasifikasi_hotel']}\n"
        response += f"   Rating: {hotel['rating_hotel']}\n"
        response += f"   Alamat: {hotel['alamat']}\n"
        response += f"   Harga: Rp {hotel['range_harga']['min']:,} - Rp {hotel['range_harga']['max']:,}\n"
        response += f"   Fasilitas: {', '.join(hotel['fasilitas'])}\n\n"

    return response


# Route for handling chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.form['user_input']
    
    # Identifikasi jenis pertanyaan atau perintah dari pengguna
    if "rekomendasi" in user_input.lower() and "hotel" in user_input.lower():
        response = chatbot_response(user_input)  # Panggil fungsi untuk memberikan rekomendasi hotel
    elif "fasilitas" in user_input.lower():
        # Tanggapi permintaan rekomendasi hotel berdasarkan kriteria fasilitas
        criteria = extract_criteria(user_input)
        if criteria.get('fasilitas'):
            response = recommend_hotels_response(criteria)
        else:
            response = "Maaf, saya tidak dapat menemukan fasilitas yang Anda maksud. Mohon sebutkan fasilitas yang lebih spesifik."
    elif "lokasi" in user_input.lower():
    # Tanggapi permintaan rekomendasi hotel berdasarkan lokasi
        criteria = extract_criteria(user_input)
        if criteria.get('lokasi'):
            response = recommend_hotels_response(criteria)
            # Perbaiki jumlah hotel yang ditampilkan berdasarkan lokasi
            max_hotels = 3
            response = response.strip().split('\n\n')  # Pisahkan masing-masing hotel
            response = '\n\n'.join(response[:max_hotels])  # Ambil maksimum 3 hotel
        else:
        # Tanggapi input yang tidak dikenali
            response = "Maaf, saya tidak mengerti pertanyaan Anda. Apakah ada yang lain yang dapat saya bantu?"
    elif "halo" in user_input.lower():
        response = "Halo! HORECO siap membantu ✨🤖 "
    elif "terima kasih" in user_input.lower():
        response = "😊 Semoga Anda menemukan yang Anda cari! Kalau ada pertanyaan lain atau butuh bantuan lebih lanjut, jangan ragu untuk bertanya"
    else:
        # Tanggapi input yang tidak dikenali
        response = "Maaf, saya tidak mengerti pertanyaan Anda. Apakah ada yang lain yang dapat saya bantu?"

    return jsonify({'response': response})

# Fungsi untuk mengekstrak lokasi dari input pengguna
def extract_location(user_input):
    # Tokenisasi kalimat pengguna
    tokens = word_tokenize(user_input.lower())
    # Gunakan lokasi unik yang diekstraksi dari dataset
    for token in tokens:
        if token in unique_locations:
            return token
    return None


# Route for about page
@app.route('/')
def index():
    return render_template('home.html')

@app.route('/home.html')
def home():
    return render_template('home.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

# Route for chatbot page
@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')

# Route for contact page
@app.route('/contact.html')
def contact():
    return render_template('contact.html')

# Route for feature page
@app.route('/feature.html')
def feature():
    return render_template('feature.html')

# Route for login page
@app.route('/login.html')
def login():
    return render_template('login.html')

# Route for testimonials page
@app.route('/testimonials.html')
def testimonials():
    return render_template('testimonials.html')

if __name__ == '__main__':
    app.run(debug=True)
