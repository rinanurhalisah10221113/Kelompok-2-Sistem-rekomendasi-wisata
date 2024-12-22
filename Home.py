import streamlit as st

# Konfigurasi halaman
st.set_page_config(page_title="Destinasik", page_icon="🌄", layout="wide")

# Header dengan logo dan teks
col1, col2 = st.columns([3, 20])  # Atur proporsi kolom

# Menampilkan gambar besar di bagian atas
st.image("images/slider/Galunggung.jpg", use_container_width=True)  # Ganti dengan path gambar Anda

with col1:
    st.image("images/loggo.png", use_container_width=True)  # Ganti dengan path logo Anda

with col2:
    st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center; height: 100%; margin-top: 20px;">
            <h1 style="font-family: Arial, sans-serif; color: #448c9d; text-align: center; font-size: 90px;">
            Destinasik
            </h1>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Header aplikasi
st.markdown(
    """
    <div style="display: flex; justify-content: center; align-items: center; height: 100%; margin-bottom: 20px;">
        <h1 style="font-family: Arial, sans-serif; color: #448c9d; text-align: center;">
            OUR SERVICE
        </h1>
    </div>

    <div style="display: flex; justify-content: center; align-items: center; height: 100%; margin-bottom: 40px;">
      <p style="font-size: 25px; text-align: center; font-family: Arial, sans-serif;">
    Destinasik membantu Anda untuk mendapatkan rekomendasi dan informasi tempat wisata di Tasikmalaya. 
    Destinasik memiliki dua layanan, yaitu Rekomendasi Wisata di Tasikmalaya dan Chatbot Informasi Wisata di Tasikmalaya.
    </p>
    </div>
    """,
    unsafe_allow_html=True
)

# Kolom untuk navigasi
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <a href="./Rekomendation" target="_self" style="text-decoration: none;">
            <div style="text-align: center; border: 2px solid #448c9d; border-radius: 10px; padding: 10px; margin: 10px;">
                <img src="data:image/png;base64,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" alt="Rekomendasi" style="width: 50%; border-radius: 10px;">
                <p style="font-family: Arial, sans-serif; font-size: 30px; color: #448c9d; margin-top: 10px;">
                    Rekomendasi Tempat Wisata
                </p>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <a href="./Chatbot" target="_self" style="text-decoration: none;">
            <div style="text-align: center; border: 2px solid #448c9d; border-radius: 10px; padding: 10px; margin: 10px;">
                <img src="https://th.bing.com/th/id/OIP.__LVSLYSkNJdp4usnMM0LwAAAA?pid=ImgDet&w=178&h=178&c=7&dpr=1,5" alt="Chatbot" style="width: 50%; border-radius: 10px;">
                <p style="font-family: Arial, sans-serif; font-size: 30px; color: #448c9d; margin-top: 10px;">
                    Chatbot
                </p>
            </div>
        </a>
        """,
        unsafe_allow_html=True,
    )

# Footer
st.write("---")
st.markdown("<p style='text-align: center;'>© 2024 Destinasik</p>", unsafe_allow_html=True)
