# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
destination_rating = pd.read_csv('Dataset/rating.csv')
destination = pd.read_csv(r'E:\TUBES NLP\Streamlit Rekomendasi\Dataset\tourism_with_id_1.csv')
 
 # Tambahkan CSS untuk styling chatbot
st.markdown("""
    <style>
    .back-button {
        display: inline-block;
        font-size: 24px; /* Ukuran ikon */
        text-decoration: none;
        color: black; /* Warna ikon */
        padding: 8px 16px; /* Padding di sekitar ikon */
        border-radius: 8px; /* Radius border untuk styling */
        background-color: #ffffff; /* Warna latar belakang tombol */
        transition: background-color 0.3s, transform 0.2s; /* Efek hover */
    }
    .back-button:hover {
        background-color: #e0e0e0; /* Warna latar saat hover */
        transform: scale(1.1); /* Efek zoom saat hover */
    }
    </style>
""", unsafe_allow_html=True)

# Tombol Back ke Home
st.markdown('<a href="/" class="back-button">⬅️ </a>', unsafe_allow_html=True)

# Streamlit layout
col1, col2 = st.columns([1, 4])

with col1:
    st.image("images/loggo.png", width=300)
with col2:
    st.title("REKOMENDASI WISATA DI TASIKMALAYA")

# Peta gambar manual
image_mapping = {
     'Gunung Galunggung': 'images/slider/Galunggung.jpg',
    'Kebun Teh Taraju': 'images/rekomendasi/Kebun Teh Taraju.jpg',
    'Bukit Panyangrayan': 'images/rekomendasi/panyang.jpg',
    'Arga Hot Spring Cisayong': 'images/rekomendasi/Arga Hot Spring Cisayong.jpg',
    'Bukit Garuda Ngupuk': 'images/rekomendasi/Bukit Garuda Ngupuk.jpeg',
    'Batu Mahpar': 'images/rekomendasi/Batu Mahpar.jpeg',
    'Situ Gede': 'images/rekomendasi/Situ Gede.jpeg',
    'Ikon Taraju': 'images/rekomendasi/ikon_taraju.jpg',
    'Kawah Gunung Galunggung': 'images/rekomendasi/Kawah Gunung Galunggung.jpeg',
    'Bukit Cisanta': 'images/rekomendasi/Bukit Cisanta.jpeg',
    'Pangangonan Hill': 'images/rekomendasi/pang.jpg',
    'Pantai Karangtawulan': 'images/rekomendasi/karangtawulan.jpg',
    'Pantai Cemara Pangkalan': 'images/rekomendasi/cemarapangkalan.jpg',
    'Pantai Citoe': 'images/rekomendasi/citoe.jpg',
    'Pantai Pamayangsari': 'images/rekomendasi/pam.jpg',
    'Pantai Sindangkerta': 'images/rekomendasi/sindangkerta.jpg',
    'Pantai Cipatujah': 'images/rekomendasi/Pantai Cipatujah.jpg',
    'Curug Batu Hanoman Cisayong': 'images/rekomendasi/Curug Batu Hanoman.jpg',
    'Curug Sawer': 'images/rekomendasi/sawer.jpg',
    'Curug Panetean': 'images/rekomendasi/panetean.jpg',
    'Curug Dengdeng': 'images/rekomendasi/dengdeng.jpg',
    'Curug Ciparay': 'images/rekomendasi/ciparay.jpg',
    'Curug Batu Black': 'images/rekomendasi/batu.jpg',
    'Curug Pamutuh': 'images/rekomendasi/Curug Pamutuh.jpg',
    'Curug Cikoja': 'images/rekomendasi/Curug Cikoja.jpeg',
    'Cipanas Cipacing' :'images/rekomendasi/Cipanas Cipacing.jpeg',
    'Kampung Naga': 'images/rekomendasi/kampung_naga.jpg',
    'Makam Syech Tubagus Anggariji' : 'images/rekomendasi/Makam Syekh Tubagus.jpeg',
    'Pamijahan' : 'images/rekomendasi/Pamijahan.jpeg',
    'Waterpark Ampera' : 'images/rekomendasi/Waterpark Ampera.jpg',
    'Pasir Kirisik' : 'images/rekomendasi/Pasir Kirisik.jpg',
    'Danau Lemona' : 'images/rekomendasi/Danau Lemona.jpg',
    'Taman Rekreasi Mangkubumi' : 'images/rekomendasi/Taman Rekreasi Mangkubumi.jpg',
    'Pongpet Cilangla' : 'images/rekomendasi/Pongpet Cilangla.jpeg',
    'Curug Cimedang' : 'images/rekomendasi/Curug Cimedang.jpeg',
    'Curug Agung Galunggung' : 'images/rekomendasi/Curug Agung Galunggung.jpg',
    'Taman Mangkubumi Indah' : 'images/rekomendasi/Taman Mangkubumi Indah.jpeg',
    'Waterpark Karang Resik' : 'images/rekomendasi/Waterpark Karang Resik.jpeg',
    'Teejay Waterpark' : 'images/rekomendasi/Teejay Waterpark.jpeg',
    'Masjid Agung Kota Tasikmalaya' : 'images/rekomendasi/Masjid Agung Kota Tasikmalaya.jpeg',
    'Tempat ziarah Walisongo Goa Safarwadi' : 'images/rekomendasi/Pamijahan.jpeg',
    'Bendungan Leuwikeris' : 'images/rekomendasi/Bendungan Leuwikeris.jpeg',
    'Alun-alun Kota Tasikmalaya' : 'images/rekomendasi/Alun-alun Kota Tasikmalaya.jpeg',
    'Alun-alun Singaparna' : 'images/rekomendasi/Alun-alun Singaparna.jpeg',
    'Mesjid Agung Singaparna Gebu' : 'images/rekomendasi/Mesjid Agung Singaparna Gebu.jpeg',
    'Pasir Pataya' : 'images/rekomendasi/Pasir Pataya.jpg',
    'Situ Sanghiyang' : 'images/rekomendasi/Situ Sanghiyang.jpg',
    'Tonjong Canyon' : 'images/rekomendasi/Tonjong Canyon.jpg',
    'Bukit Nangela' : 'images/rekomendasi/Bukit Nangela.jpg',
    'Kawah Karaha Bodas' : 'images/rekomendasi/Kawah Karaha Bodas.jpg',
    'Bukit Pujiningrum' : 'images/rekomendasi/Bukit Pujiningrum.jpg',
    'Bukit Panyangrayan' : 'images/rekomendasi/Bukit Panyangrayan.jpg',
    'Bukit kacapi' : 'images/rekomendasi/Bukit kacapi.jpg',
    'Cipanas Citiis' : 'images/rekomendasi/Cipanas Citiis.jpeg',
    'Bukit Pujiningrum' : 'images/rekomendasi/Bukit Pujiningrum.jpg',
}

# Bersihkan dan gabungkan data
tourism_cleaned = destination[['Place_Id', 'Place_Name', 'Category', 'Description', 'Rating', 'Address', 'Google Maps', 'Facility', 'entry fee']].dropna()
ratings_merged = pd.merge(destination_rating, tourism_cleaned, on='Place_Id', how='inner')

# Rata-rata rating
destination_grouped = ratings_merged.groupby(['Place_Id', 'Place_Name', 'Category', 'Description', 'Rating', 'Address', 'Google Maps', 'Facility', 'entry fee'], as_index=False).agg({'Rating': 'mean'})
destination_grouped = destination_grouped.sort_values(by='Rating', ascending=False)

# TF-IDF Vectorizer
data = destination[['Place_Id', 'Place_Name', 'Category']].dropna()
tf = TfidfVectorizer()
tfidf_matrix = tf.fit_transform(data['Category'])
cosine_sim = cosine_similarity(tfidf_matrix)
cosine_sim_df = pd.DataFrame(cosine_sim, index=data['Place_Name'], columns=data['Place_Name'])

# Fungsi rekomendasi berdasarkan Cosine Similarity
def top_n_recommendations(nama_destinasi, similarity_data=cosine_sim_df, items=data[['Place_Name', 'Category']], n=10):
    index = similarity_data.loc[:, nama_destinasi].to_numpy().argpartition(range(-1, -n, -1))
    closest = similarity_data.columns[index[-1:-(n+2):-1]]
    closest = closest.drop(nama_destinasi, errors='ignore')
    return pd.DataFrame(closest).merge(items, left_on=0, right_on='Place_Name').head(n)

# Fungsi rekomendasi berdasarkan kategori dan nama tempat
def get_recommendations_by_category_and_name(category_keyword, place_keyword, data, top_n=10):
    filtered_data = data[data['Category'].str.contains(category_keyword, case=False, na=False)]
    
    # Filter by place name keyword
    if place_keyword:
        filtered_data = filtered_data[filtered_data['Place_Name'].str.contains(place_keyword, case=False, na=False)]
    
    recommended = filtered_data.sort_values(by='Rating', ascending=False).head(top_n)
    return recommended


def get_recommendations_by_search(keyword, data, top_n=10):
    # Memisahkan kategori dan nama tempat (misalnya: "Pantai Gunung Galunggung")
    filtered_data = data[
        data['Category'].str.contains(keyword, case=False, na=False) | 
        data['Place_Name'].str.contains(keyword, case=False, na=False)
    ]
    recommended = filtered_data.sort_values(by='Rating', ascending=False).head(top_n)
    return recommended

# Fungsi untuk menampilkan rating dengan ikon bintang
def display_rating_with_stars(rating):
    """Mengonversi rating menjadi ikon bintang HTML dengan angka di sebelahnya."""
    full_stars = int(rating)  # Jumlah bintang penuh
    half_star = 1 if (rating - full_stars) >= 0.5 else 0  # Bintang setengah
    empty_stars = 5 - full_stars - half_star  # Bintang kosong

    stars_html = ("★" * full_stars) + ("☆" * empty_stars)  # Format bintang
    stars_with_rating = (
        f'<span style="color: gold; font-size: 1.2em;">{stars_html}</span> '
        f'<span style="color: black; font-size: 1.1em;">({rating:.1f})</span>'
    )
    return f'<b>Rating :</b> {stars_with_rating}'

# Input gabungan kategori dan nama tempat wisata
search_keyword = st.text_input("Masukkan kata kunci untuk kategori atau nama tempat wisata (Kategori: Alam, Pantai, Air Terjun, Pemandian Air Panas, Budaya, Taman Rekreasi, Wahana Rekreasi, Wisata Religi, Wisata Umum.):")

def get_recommendations_by_search(keyword, data, top_n=10):
    # Memfilter data berdasarkan kategori atau nama tempat yang mengandung kata kunci
    filtered_data = data[
        data['Category'].str.contains(keyword, case=False, na=False) | 
        data['Place_Name'].str.contains(keyword, case=False, na=False)
    ]
    recommended = filtered_data.sort_values(by='Rating', ascending=False).head(top_n)
    return recommended

if st.button("Tampilkan Rekomendasi"):
    # Menggunakan fungsi untuk mendapatkan rekomendasi berdasarkan kata kunci
    recommendations = get_recommendations_by_search(search_keyword, destination_grouped)
    
    if not recommendations.empty:
        for _, row in recommendations.iterrows():
            st.subheader(row['Place_Name'])
            # Menampilkan gambar setelah Place_Name
            image_path = image_mapping.get(row['Place_Name'], None)
            if image_path:
                st.image(image_path, caption=row['Place_Name'], width=400)
            
            st.write(f"Kategori: {row['Category']}")
            # Menampilkan rating dengan ikon bintang dan angka
            st.markdown(display_rating_with_stars(row['Rating']), unsafe_allow_html=True)
            st.write(f"Deskripsi: {row['Description']}")
            st.write(f"Fasilitas: {row['Facility']}")
            st.write(f"Biaya Masuk: {row['entry fee']}")
            st.write(f"Alamat: {row['Address']}")
            st.write(f"Google Maps: {row['Google Maps']}")
    else:
        st.write("Tidak ada rekomendasi yang sesuai dengan kata kunci Anda.")

# Tambahkan footer
st.write("Masukkan kata kunci untuk mendapatkan rekomendasi wisata terbaik di Kabupaten Tasikmalaya.")