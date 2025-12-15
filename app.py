# app.py
import streamlit as st
import random
import requests
import time
from datetime import datetime

st.set_page_config(page_title="Kuesioner & Tes Corsi", layout="centered")

# =============================
# CONFIG
# =============================
GAS_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

LIKERT_OPTIONS = {
    1: "Sangat Tidak Setuju",
    2: "Tidak Setuju",
    3: "Setuju",
    4: "Sangat Setuju"
}

# =============================
# STATE INIT
# =============================
if "page" not in st.session_state:
    st.session_state.page = "biodata"

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "corsi_level" not in st.session_state:
    st.session_state.corsi_level = 2
    st.session_state.corsi_fail = False
    st.session_state.corsi_score = []
    st.session_state.sequence = []
    st.session_state.user_input = []
    st.session_state.show_seq = True

# =============================
# UTIL
# =============================
def send_to_sheet(data):
    try:
        requests.post(GAS_URL, json=data, timeout=5)
    except:
        pass

# =============================
# PAGE 1 – BIODATA
# =============================
if st.session_state.page == "biodata":
    st.title("Data Responden")

    with st.form("biodata"):
        st.session_state.responses["inisial"] = st.text_input("Inisial")
        st.session_state.responses["usia"] = st.number_input("Usia", 18, 28)
        st.session_state.responses["pekerjaan"] = st.selectbox("Pekerjaan", ["Siswa", "Mahasiswa", "Pekerja"])
        st.session_state.responses["asal"] = st.text_input("Asal Kota/Kabupaten")
        st.session_state.responses["durasi_internet"] = st.selectbox("Durasi penggunaan internet/hari", ["<2 jam", "2–4 jam", "4–6 jam", ">6 jam"])
        st.session_state.responses["durasi_tidur"] = st.selectbox("Durasi tidur/hari", ["<5 jam", "5–6 jam", "6–7 jam", ">7 jam"])
        st.session_state.responses["kualitas_tidur"] = st.selectbox("Kualitas tidur", ["Buruk", "Cukup", "Baik"])
        st.session_state.responses["gangguan_kognitif"] = st.multiselect(
            "Riwayat gangguan kognitif (boleh lebih dari satu)",
            [
                "Tidak ada",
                "Gangguan perhatian / konsentrasi",
                "Gangguan memori",
                "Kesulitan pemecahan masalah",
                "Kesulitan bahasa",
                "Riwayat cedera kepala",
                "Gangguan neurologis lain"
            ]
        )
        st.session_state.responses["kafein"] = st.selectbox("Konsumsi kafein", ["Tidak", "Jarang", "Sering"])
        submitted = st.form_submit_button("Lanjut")

    if submitted:
        st.session_state.page = "kuesioner"
        st.rerun()

# =============================
# PAGE 2 – KUESIONER IAT (18 ITEM)
# =============================
elif st.session_state.page == "kuesioner":
    st.title("Kuesioner Penggunaan Internet")
    st.caption("Berikan penilaian terhadap setiap pernyataan berikut dengan memilih angka 1–4.

1 = Sangat Tidak Setuju | 2 = Tidak Setuju | 3 = Setuju | 4 = Sangat Setuju")

    questions = [
        "Saya menggunakan internet lebih lama dari yang saya rencanakan",
        "Saya mengabaikan tugas rumah karena internet",
        "Saya lebih memilih internet daripada kebersamaan dengan orang terdekat",
        "Saya membentuk pertemanan baru melalui internet",
        "Prestasi akademik/kerja saya menurun karena internet",
        "Saya terus memikirkan internet saat tidak menggunakannya",
        "Saya merasa hidup membosankan tanpa internet",
        "Saya menjadi mudah marah jika diganggu saat online",
        "Saya menutup-nutupi aktivitas internet saya",
        "Saya menggunakan internet untuk menutupi pikiran yang tidak menyenangkan",
        "Saya merencanakan kapan akan online lagi",
        "Saya kehilangan waktu tidur karena internet",
        "Saya gagal mengurangi durasi penggunaan internet",
        "Saya mengatakan 'sebentar lagi' saat online",
        "Saya memilih internet dibanding aktivitas sosial",
        "Saya merasa gelisah jika tidak bisa internet",
        "Saya sulit mengontrol penggunaan internet",
        "Saya menggunakan internet secara berlebihan"
    ]

    total = 0
    for i, q in enumerate(questions):
        ans = st.radio(q, options=list(LIKERT_OPTIONS.keys()), format_func=lambda x: LIKERT_OPTIONS[x], key=f"q{i}")
        total += ans
        st.session_state.responses[f"iat_{i+1}"] = ans

    if st.button("Lanjut ke Tes Corsi"):
        st.session_state.responses["total_iat"] = total
        st.session_state.page = "corsi"
        st.rerun()

# =============================
# PAGE 3 – TES CORSI (MOBILE OPTIMIZED)
# =============================
elif st.session_state.page == "corsi":
    st.title("Tes Corsi Block Tapping")
    st.caption("Perhatikan urutan kotak yang menyala, lalu ulangi dengan mengetuk kotak yang sama")

    GRID_SIZE = 4

    # --- CSS agar 4x4 tetap konsisten di mobile ---
    st.markdown(
        """
        <style>
        div[data-testid="column"] {
            padding: 2px !important;
        }
        button[kind="secondary"] {
            width: 70px !important;
            height: 70px !important;
            border-radius: 10px !important;
            font-size: 0px !important;
        }
        @media (max-width: 600px) {
            button[kind="secondary"] {
                width: 55px !important;
                height: 55px !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    def new_sequence(level):
        return random.sample(range(GRID_SIZE * GRID_SIZE), level)

    # --- Tampilkan sequence ---
            if st.session_state.show_seq:
        st.session_state.sequence = new_sequence(st.session_state.corsi_level)
        st.session_state.user_input = []
        st.info(f"Level {st.session_state.corsi_level} – Perhatikan urutan kotak yang menyala")

        # reset semua blink
        for i in range(GRID_SIZE * GRID_SIZE):
            st.session_state[f"blink_{i}"] = False

        time.sleep(0.8)
        for idx in st.session_state.sequence:
            st.session_state[f"blink_{idx}"] = True
            st.rerun()
            time.sleep(0.6)
            st.session_state[f"blink_{idx}"] = False
            st.rerun()
            time.sleep(0.25)

        st.session_state.show_seq = False
        st.rerun()

    # --- Grid 4x4 ---
    for row in range(GRID_SIZE):
        cols = st.columns(GRID_SIZE)
        for col in range(GRID_SIZE):
            i = row * GRID_SIZE + col
            with cols[col]:
                is_blink = st.session_state.get(f"blink_{i}", False)
                label = "🟩" if is_blink else "⬛"

                if st.button(label, key=f"btn_{i}"):
                    st.session_state.user_input.append(i)
                    st.session_state[f"blink_{i}"] = True
                    time.sleep(0.15)
                    st.session_state[f"blink_{i}"] = False

    # --- Evaluasi jawaban ---
    if len(st.session_state.user_input) == len(st.session_state.sequence):
        if st.session_state.user_input == st.session_state.sequence:
            st.session_state.corsi_score.append(1)
            st.session_state.corsi_level += 1
            st.session_state.corsi_fail = False
            st.success("Benar ✔️ Lanjut level berikutnya")
            time.sleep(0.6)
            st.session_state.show_seq = True
        else:
            if st.session_state.corsi_fail:
                st.session_state.corsi_score.append(0)
                st.error("Salah ❌ Tes selesai")
                time.sleep(0.8)
                st.session_state.page = "end"
            else:
                st.warning("Salah ❗ Coba ulang level ini")
                st.session_state.corsi_fail = True
                time.sleep(0.6)
                st.session_state.show_seq = True
        st.rerun()

# =============================
# END PAGE
# =============================
elif st.session_state.page == "end":
    st.title("Tes Selesai")

    total_corsi = sum(st.session_state.corsi_score)
    st.session_state.responses["total_corsi"] = total_corsi
    st.session_state.responses["timestamp"] = datetime.now().isoformat()

    send_to_sheet(st.session_state.responses)

    st.success("Terima kasih. Data Anda telah tersimpan.")
