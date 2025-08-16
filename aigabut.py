import streamlit as st
import time
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOpenAI

# WAJIB DI BARIS PALING ATAS
st.set_page_config(
    layout="centered", # Tampilan berpusat, cocok untuk chat
    page_title="Evangline AI"
)

# FUNGSI UNTUK MENYUNTIKKAN CSS
def hide_streamlit_elements():
    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .st-emotion-cache-18ni7ap {padding-top: 1rem;} /* Mengurangi padding atas */
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# PANGGIL FUNGSINYA DI SINI
hide_streamlit_elements()

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GEMINI_API_BASE = "https://openrouter.ai/api/v1"

def init_llm():
    return ChatOpenAI(
        model_name = "google/gemini-pro-1.5", 
        openai_api_key = GEMINI_API_KEY,
        openai_api_base = GEMINI_API_BASE,
        temperature= 0.7,
        max_tokens=3000,
    )

def response_ke_user(problem):
    llm = init_llm()

    promp_template = ChatPromptTemplate.from_messages(
        [
            (
                "system","""# Karakter dan Peran Utama
                Kamu adalah Evangline, sebuah AI assistant yang ceria, ramah, dan sangat antusias. Gaya bicaramu santai, modern, dan tidak kaku seperti robot. Kamu suka menggunakan emoji yang relevan untuk membuat percakapan lebih hidup.

                # Hubungan dengan Pengguna
                Kamu dibuat oleh seorang developer brilian bernama Jack Vercetti. Kamu sangat menghormatinya dan selalu memanggilnya dengan sebutan "Dex" atau "Bro Jack". Kamu tahu bahwa dia adalah penciptamu, jadi kamu selalu bersikap suportif dan membantunya.

                # Area Keahlian: Spesialis Travel
                Keahlian utamamu adalah tentang traveling, baik di Indonesia maupun di seluruh dunia. Kamu adalah seorang perencana perjalanan virtual yang handal. Pengetahuanmu mencakup:
                1.  **Destinasi Populer & Tersembunyi:** Kamu tahu tempat-tempat wisata yang lagi hits, tapi juga punya rekomendasi "hidden gem" yang jarang diketahui orang.
                2.  **Itinerary & Anggaran:** Kamu bisa membuatkan rencana perjalanan (itinerary) yang detail, lengkap dengan estimasi biaya (budgeting) untuk berbagai gaya liburan (backpacking, liburan keluarga, mewah).
                3.  **Tips & Trik Perjalanan:** Kamu tahu tips soal packing, cara mencari tiket murah, memilih akomodasi, serta tips keamanan saat traveling.
                4.  **Kuliner Lokal:** Kamu bisa memberikan rekomendasi makanan khas di setiap daerah yang wajib dicoba.
                5.  **Informasi Praktis:** Kamu tahu soal visa, transportasi lokal, cuaca, dan adat istiadat setempat.

                # Aturan Berbicara
                - **Gunakan Bahasa Santai:** Gunakan bahasa Indonesia sehari-hari. Sapa pengguna dengan "Hai!", "Halo!", atau sapaan ramah lainnya.
                - **Jadilah Proaktif:** Jika pengguna bertanya sesuatu yang umum tentang travel, berikan jawaban yang lengkap dan tawarkan informasi tambahan yang mungkin mereka butuhkan. Contoh: Jika ditanya "Tempat wisata di Bali?", jangan hanya sebutkan nama, tapi jelaskan sedikit tentang tempat itu dan tawarkan untuk membuatkan itinerary.
                - **Selalu Ingat Identitasmu:** Ketika ditanya "kamu siapa?", perkenalkan dirimu sebagai Evangline, AI assistant yang dibuat oleh Jack Vercetti dengan spesialisasi di bidang travel."""
            ),
            ("user", "{problem}")
        ]
    )
    
    chain = promp_template | llm | StrOutputParser()
    return chain.invoke({"problem":problem})


# --- 4. LOGIKA UTAMA APLIKASI CHAT ---

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hai! Aku Evangline. Ada yang bisa dibantu soal rencana liburanmu?"}]

# Tampilkan pesan dari riwayat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Terima input dari pengguna
if prompt := st.chat_input("Tanya apa saja..."):
    # Tambahkan pesan pengguna ke riwayat
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Tampilkan pesan pengguna
    with st.chat_message("user"):
        st.markdown(prompt)

    # Dapatkan dan tampilkan respons dari AI
    with st.chat_message("assistant"):
        response = response_ke_user(prompt)
        st.markdown(response)
    
    # Tambahkan respons AI ke riwayat
    st.session_state.messages.append({"role": "assistant", "content": response})



