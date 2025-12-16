# app.py
# Aplikasi Streamlit: Data Responden + Kuesioner IAT (Likert 1-4) + Corsi Block Tapping
# Dibuat ringkas & modular untuk pemula

import streamlit as st
import random
import requests
import time

st.set_page_config(page_title="Kuesioner & Tes Corsi", layout="centered")

# =============================
# KONFIGURASI
# =============================
GAS_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"
GRID_SIZE = 4
MAX_LEVEL = 9

# =============================
# STATE
# =============================
if "page" not in st.session_state:
    st.session_state.page = 1

if "responses" not in st.session_state:
    st.session_state.responses = {}

if "corsi_level" not in st.session_state:
    st.session_state.corsi_level = 2
    st.session_state.corsi_fail = False
    st.session_state.sequence = []
    st.session_state.user_input = []
    st.session_state.corsi_score = []

# =============================
# HELPER
# =============================
def send_to_sheet(payload):
    try:
        requests.post(GAS_URL, json=payload, timeout=5)
    except:
        pass

# =============================
# HALAMAN 1 – DATA RESPONDEN
# =============================
if st.session_state.page == 1:
    st.title("Data Responden")

    st.session_state.responses.update({
        "inisial": st.text_input("Inisial"),
        "usia": st.number_input("Usia (18–28)", 18, 28),
        "pekerjaan": st.selectbox("Pekerjaan", ["Mahasiswa", "Pekerja", "Siswa"]),
        "asal": st.text_input("Asal Kota/Kabupaten"),
        "durasi_internet": st.selectbox("Durasi penggunaan internet / hari", ["<2 jam", "2–4 jam", "4–6 jam", ">6 jam"]),
        "durasi_tidur": st.selectbox("Durasi tidur / hari", ["<5 jam", "5–6 jam", "6–7 jam", ">7 jam"]),
        "kualitas_tidur": st.selectbox("Kualitas tidur", ["Baik", "Cukup", "Buruk"]),
        "gangguan_kognitif": st.selectbox("Riwayat gangguan kognitif", ["Tidak", "Ada"]),
        "kafein": st.selectbox("Konsumsi kafein", ["Tidak", "Kadang", "Sering"])
    })

    if st.button("Lanjut ke Kuesioner"):
        st.session_state.page = 2

# =============================
# HALAMAN 2 – KUESIONER IAT
# =============================
elif st.session_state.page == 2:
    st.title("Kuesioner Penggunaan Internet")
    st.write("**Petunjuk:** Pilih jawaban yang paling sesuai dengan kondisi Anda")
    st.write("1 = Tidak Pernah | 2 = Jarang | 3 = Sering | 4 = Selalu")

    items = [
        "Saya menggunakan internet lebih lama dari yang saya rencanakan",
        "Saya mengabaikan kewajiban karena internet",
        "Saya lebih memilih internet daripada berinteraksi langsung",
        "Saya sulit menghentikan penggunaan internet",
        "Saya merasa gelisah jika tidak menggunakan internet",
        "Penggunaan internet mengganggu produktivitas saya",
        "Saya memikirkan internet meskipun sedang tidak menggunakannya",
        "Saya menggunakan internet untuk melarikan diri dari masalah",
        "Saya mencoba mengurangi penggunaan internet namun gagal",
        "Saya merasa waktu berlalu sangat cepat saat online",
        "Saya mengorbankan waktu tidur demi internet",
        "Saya menyembunyikan durasi penggunaan internet saya",
        "Saya merasa hidup membosankan tanpa internet",
        "Saya menjadi mudah marah saat terganggu ketika online",
        "Saya memilih internet dibanding kegiatan sosial",
        "Saya mengatakan \"sebentar lagi\" saat diminta berhenti",
        "Saya menggunakan internet untuk memperbaiki suasana hati",
        "Saya kesulitan mengontrol penggunaan internet"
    ]

    total = 0
    for i, q in enumerate(items):
        val = st.radio(q, [1, 2, 3, 4], horizontal=True, key=f"q{i}")
        total += val
        st.session_state.responses[f"IAT_{i+1}"] = val

    st.session_state.responses["total_iat"] = total

    if st.button("Lanjut ke Tes Corsi"):
        send_to_sheet(st.session_state.responses)
        st.session_state.page = 3

# =============================
# HALAMAN 3 – TES CORSI
# =============================
elif st.session_state.page == 3:
    st.title("Tes Corsi Block Tapping")

    if not st.session_state.sequence:
        st.session_state.sequence = random.sample(range(GRID_SIZE**2), st.session_state.corsi_level)
        st.session_state.user_input = []

        for idx in st.session_state.sequence:
            r, c = divmod(idx, GRID_SIZE)
            st.session_state[f"blink_{idx}"] = True
            time.sleep(0.6)
            st.session_state[f"blink_{idx}"] = False

    cols = st.columns(GRID_SIZE)
    for i in range(GRID_SIZE**2):
        col = cols[i % GRID_SIZE]
        color = "🟩" if st.session_state.get(f"clicked_{i}") else "⬜"
        if col.button(color, key=f"btn_{i}"):
            st.session_state.user_input.append(i)
            st.session_state[f"clicked_{i}"] = True

    if len(st.session_state.user_input) == len(st.session_state.sequence):
        if st.session_state.user_input == st.session_state.sequence:
            st.session_state.corsi_score.append(1)
            st.session_state.corsi_level += 1
            st.session_state.sequence = []
        else:
            if st.session_state.corsi_fail:
                st.session_state.corsi_score.append(0)
                st.session_state.responses["total_corsi"] = sum(st.session_state.corsi_score)
                send_to_sheet(st.session_state.responses)
                st.success("Tes selesai. Terima kasih")
                st.stop()
            else:
                st.session_state.corsi_fail = True
                st.session_state.sequence = []
