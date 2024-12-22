import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Chatbot Informasi Wisata", page_icon="🤖", layout="wide")

# Tambahkan CSS untuk styling chatbot
st.markdown("""
    <style>
    .main-container { 
        display: flex; 
        flex-direction: column; 
        height: 10vh; 
    }
    .chat-container { 
        flex: 1; 
        overflow-y: auto; 
        padding: 20px; 
        background-color: #f5f5f5; 
        border-radius: 10px; 
        display: flex;
        flex-direction: column;
        justify-content: flex-end;
    }
    .message { 
        margin: 10px 0; 
        padding: 10px 15px; 
        border-radius: 15px; 
        max-width: 75%; 
    }
    .user-message { 
        background-color: #d1e7dd; 
        align-self: flex-end; 
        color: #0f5132; 
        text-align: right;
    }
    .bot-message { 
        background-color: #e2e3e5; 
        align-self: flex-start; 
        color: #41464b; 
    }
    .input-container { 
        padding: 10px; 
        background-color: white; 
        border-top: 1px solid #ccc; 
        display: flex;
        gap: 10px;
        position: sticky;
        bottom: 0;
        z-index: 1;
    }
    .text-input { 
        flex: 1; 
        padding: 10px; 
        border-radius: 5px; 
        border: 1px solid #ccc; 
    }
    .send-button { 
        background-color: #6c757d; 
        color: white; 
        border: none; 
        padding: 10px 20px; 
        border-radius: 5px; 
        cursor: pointer; 
    }
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

# Load dataset
@st.cache_data
def load_dataset():
    dataset_path = r'E:\TUBES NLP\Streamlit Rekomendasi\Dataset\ChatbotNEW.csv'
    df = pd.read_csv(dataset_path)
    return df

df = load_dataset()

# Ambil kolom pertanyaan, jawaban, dan lokasi
questions = df['Question'].values
answers = df['Answer'].values
locations = df.get('Location', pd.Series([None] * len(df)))  # Jika tidak ada kolom Location, isi dengan None

# Vectorisasi data pertanyaan
@st.cache_resource
def preprocess_data():
    vectorizer = TfidfVectorizer()
    question_vectors = vectorizer.fit_transform(questions)
    return vectorizer, question_vectors

vectorizer, question_vectors = preprocess_data()

# Fungsi chatbot untuk mencari jawaban
def chatbot_response(user_input):
    # Vectorize user input
    user_vector = vectorizer.transform([user_input])
    
    # Calculate similarity
    similarity_scores = cosine_similarity(user_vector, question_vectors)
    
    # Get the best match
    max_index = similarity_scores.argmax()
    max_score = similarity_scores[0, max_index]
    
    # Threshold untuk menentukan apakah cocok
    if max_score > 0.5:
        response = answers[max_index]
        location = locations[max_index]
        if pd.notna(location):
            response += f"\n<a href=\"{location}\" target=\"_blank\">Buka di Google Maps</a>"
        return response
    else:
        return "Maaf Loly tidak mengerti."

# Tampilkan percakapan awal
if "conversation" not in st.session_state:
    st.session_state.conversation = [
        {"sender": "bot", "message": "Halo! Saya Loly, asisten wisata Anda. Tanyakan tentang pantai, curug, atau tempat wisata lainnya!"}
    ]

def process_user_input():
    user_input = st.session_state.text_input.strip()  # Ambil input pengguna
    if user_input:  # Jika input tidak kosong
        # Tambahkan pesan pengguna ke percakapan
        st.session_state.conversation.append({"sender": "user", "message": user_input})
        # Dapatkan respon bot
        bot_response = chatbot_response(user_input)
        st.session_state.conversation.append({"sender": "bot", "message": bot_response})
        # Reset input text
        st.session_state.text_input = ""  # Kosongkan input setelah diproses

# Kontainer utama
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Kontainer percakapan
st.markdown('<div class="chat-container">', unsafe_allow_html=True)
for chat in st.session_state.conversation:
    if chat["sender"] == "user":
        st.markdown(f'<div class="message user-message">{chat["message"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="message bot-message">{chat["message"]}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Kontainer input pengguna
with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)
    user_input = st.text_input("", key="text_input", placeholder="Tanyakan sesuatu...", label_visibility="collapsed")
    if st.button("Kirim", on_click=process_user_input):
        pass
    st.markdown('</div>', unsafe_allow_html=True)

# Akhiri kontainer utama
st.markdown('</div>', unsafe_allow_html=True)