import streamlit as st
import random
import requests
import time
from datetime import datetime

# URL Webhook Google Sheet Anda
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

st.set_page_config(
    page_title="Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja",
    layout="centered"
)

# -------------------------------------------------------------
# CSS Styling untuk Tombol Corsi
# -------------------------------------------------------------
st.markdown("""
<style>
    /* Membuat tombol terlihat kotak dan besar */
    div[data-testid="stButton"] button {
        width: 100%;
        aspect-ratio: 1 / 1;
        border-radius: 8px;
        border: 2px solid #CBD5E0;
        background-color: #E2E8F0;
        transition: all 0.2s;
    }
    /* Efek hover */
    div[data-testid="stButton"] button:hover {
        border-color: #2B6CB0;
        background-color: #BEE3F8;
    }
    /* Efek ketika tombol diklik (Active) */
    div[data-testid="stButton"] button:active {
        background-color: #2B6CB0 !important;
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# 18 ITEM IAT
# -------------------------------------------------------------
QUESTIONS = [
    "Saya bermain internet lebih lama dari yang saya rencanakan.",
    "Saya membentuk pertemanan baru melalui internet.",
    "Saya merahasiakan aktivitas saya di internet dari orang lain.",
    "Saya menutupi pikiran yang mengganggu dengan memikirkan hal menyenangkan tentang internet.",
    "Saya takut hidup tanpa internet akan membosankan atau kosong.",
    "Saya marah jika ada yang mengganggu saat saya bermain internet.",
    "Saya terus memikirkan internet ketika tidak sedang bermain.",
    "Saya lebih memilih internet daripada beraktivitas dengan orang lain.",
    "Saya merasa gelisah jika tidak bermain internet, dan tenang kembali setelah bermain.",
    "Saya mengabaikan pekerjaan rumah demi bermain internet.",
    "Waktu belajar atau nilai akademik saya menurun akibat internet.",
    "Kinerja saya di sekolah/rumah terganggu karena internet.",
    "Saya sering kurang tidur karena bermain internet.",
    "Saya berusaha mengurangi waktu internet tetapi gagal.",
    "Saya sering berkata 'sebentar lagi' saat bermain internet.",
    "Saya berusaha menyembunyikan durasi bermain internet.",
    "Saya mengabaikan kegiatan penting demi internet.",
    "Saya merasa sulit berhenti ketika sedang bermain internet."
]

# -------------------------------------------------------------
# HELPER
# -------------------------------------------------------------
def send_to_webhook(payload):
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, str(e)

# -------------------------------------------------------------
# FORM IDENTITAS
# -------------------------------------------------------------
def render_identity_form():
    st.header("Data Responden")
    st.info("Data Anda bersifat rahasia dan hanya digunakan untuk kepentingan akademik.")

    with st.form("identity_form"):
        col1, col2 = st.columns(2)
        with col1:
            inisial = st.text_input("Inisial (wajib)")
            umur = st.number_input("Umur", min_value=17, max_value=28, step=1)
            gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
            pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
            kota = st.text_input("Domisili (Kota/Kabupaten)")
        
        with col2:
            durasi = st.selectbox("Durasi layar per hari", ["Pilih...", "<1 jam", "1–2 jam", "2–4 jam", "4–6 jam", ">6 jam"])
            aktivitas = st.selectbox("Aktivitas utama", ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])
            sebelum_tidur = st.radio("Gawai sebelum tidur?", ["Ya", "Tidak"])
            kualitas_tidur = st.selectbox("Kualitas tidur", ["Pilih...", "Baik", "Sedang", "Buruk"])
            durasi_tidur = st.selectbox("Durasi tidur", ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])

        st.markdown("---")
        gangguan_fokus = st.selectbox("Riwayat gangguan fokus", ["Pilih...", "Tidak ada", "ADHD", "Slow learner", "Gangguan bahasa", "Kesulitan pendengaran"])
        riwayat_kognitif = st.selectbox("Riwayat medis kognitif", ["Pilih...", "Tidak ada", "Cedera kepala", "Riwayat kejang", "Obat fokus"])
        kafein = st.selectbox("Konsumsi kafein hari ini", ["Pilih...", "Tidak pernah", "1x", "2x", "3x atau lebih"])

        submit = st.form_submit_button("Lanjut ke Kuesioner")

        if submit:
            required = [
                inisial.strip(), kota.strip(), pendidikan != "Pilih...",
                durasi != "Pilih...", aktivitas != "Pilih...", kualitas_tidur != "Pilih...",
                durasi_tidur != "Pilih...", gangguan_fokus != "Pilih...",
                riwayat_kognitif != "Pilih...", kafein != "Pilih..."
            ]
            
            if not all(required):
                st.error("Mohon lengkapi semua data.")
            else:
                st.session_state.identity_data = {
                    "inisial": inisial, "umur": int(umur), "jenis_kelamin": gender,
                    "pendidikan": pendidikan, "kota": kota, "durasi_layar": durasi,
                    "aktivitas_gawai": aktivitas, "sebelum_tidur": sebelum_tidur,
                    "kualitas_tidur": kualitas_tidur, "durasi_tidur": durasi_tidur,
                    "riwayat_gangguan_fokus": gangguan_fokus,
                    "riwayat_kognitif": riwayat_kognitif, "kafein": kafein
                }
                st.session_state.identity_completed = True
                st.rerun()

# -------------------------------------------------------------
# KUESIONER IAT
# -------------------------------------------------------------
def render_questionnaire():
    st.header("Bagian 1 — Kuesioner Internet Addiction")
    st.write("1 = Sangat Tidak Setuju | 4 = Sangat Setuju")

    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        st.write(f"**{i}. {q}**")
        answers[f"Q{i}"] = st.radio(f"Label {i}", [1,2,3,4], horizontal=True, label_visibility="collapsed", key=f"q_new_{i}")
        st.write("") # Spacer

    if st.button("Selesai & Mulai Tes Memori"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()

# -------------------------------------------------------------
# BLINK VISUAL (PERBAIKAN)
# -------------------------------------------------------------
def blink_visual(sequence, positions):
    # Container untuk visual blink agar tidak menggeser layout
    ph = st.empty()
    
    # Tampilkan Grid Kosong Dulu
    with ph.container():
        st.markdown("<h3 style='text-align: center;'>Perhatikan Urutan!</h3>", unsafe_allow_html=True)
        # Kita render HTML visual saja untuk blink karena lebih cepat render-nya daripada st.button
        html = "<div style='display:grid;grid-template-columns:repeat(4,70px);gap:10px;justify-content:center;margin-top:20px;'>"
        for p in range(1, 17): # 1 sampai 16
             html += "<div style='width:70px;height:70px;background:#E2E8F0;border-radius:8px;'></div>"
        html += "</div>"
        st.markdown(html, unsafe_allow_html=True)
    
    time.sleep(1) # Jeda sebelum mulai

    # Mulai Blinking
    for target in sequence:
        with ph.container():
            st.markdown("<h3 style='text-align: center;'>Perhatikan Urutan!</h3>", unsafe_allow_html=True)
            html = "<div style='display:grid;grid-template-columns:repeat(4,70px);gap:10px;justify-content:center;margin-top:20px;'>"
            for p in range(1, 17):
                # Warna Biru jika target, Abu jika bukan
                color = "#2B6CB0" if p == target else "#E2E8F0"
                # Sedikit efek shadow jika target
                shadow = "box-shadow: 0 0 10px #2B6CB0;" if p == target else ""
                html += f"<div style='width:70px;height:70px;background:{color};border-radius:8px;{shadow}'></div>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
        
        time.sleep(0.65) # Durasi nyala
        
        # Blank/Jeda antar kedipan (penting agar jika kotak sama muncul 2x berturut2 terlihat bedanya)
        with ph.container():
            st.markdown("<h3 style='text-align: center;'>Perhatikan Urutan!</h3>", unsafe_allow_html=True)
            html = "<div style='display:grid;grid-template-columns:repeat(4,70px);gap:10px;justify-content:center;margin-top:20px;'>"
            for p in range(1, 17):
                 html += "<div style='width:70px;height:70px;background:#E2E8F0;border-radius:8px;'></div>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
        time.sleep(0.2) 

    ph.empty() # Hapus visual blink

# -------------------------------------------------------------
# TES CORSI (CORE LOGIC)
# -------------------------------------------------------------
def render_corsi():
    st.header("Bagian 2 — Tes Corsi Block")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "positions": list(range(1, 17)), # Posisi tetap 1-16
            "sequence": [],
            "user_clicks": [],
            "attempt": 1,
            "results": {},
            "status": "init" # init, blink, input, finished
        }

    cs = st.session_state.corsi

    # --- LOGIC: INIT LEVEL ---
    if cs["status"] == "init":
        # Generate sequence baru
        seq_len = cs["level"] + 1 # Level 1 = 2 blok, Level 2 = 3 blok, dst
        # Pastikan tidak mengambil sampel lebih dari yg tersedia
        cs["sequence"] = random.sample(range(1, 17), min(seq_len, 16))
        cs["user_clicks"] = []
        cs["status"] = "blink"
        st.rerun()

    # --- LOGIC: BLINK ---
    if cs["status"] == "blink":
        blink_visual(cs["sequence"], cs["positions"])
        cs["status"] = "input"
        st.rerun() # PENTING: Gunakan rerun, BUKAN stop

    # --- LOGIC: INPUT USER ---
    if cs["status"] == "input":
        st.write(f"Level: **{cs['level']}** | Percobaan: **{cs['attempt']}/2**")
        st.write("Ulangi urutan kotak yang menyala tadi:")

        # Tampilkan progress klik user (opsional, visual feedback)
        # st.progress(len(cs['user_clicks']) / len(cs['sequence']))

        # Render Grid Tombol (4x4)
        # Menggunakan st.columns untuk layout grid yang stabil
        grid_container = st.container()
        with grid_container:
            for row in range(4):
                cols = st.columns(4)
                for col_idx in range(4):
                    block_id = (row * 4) + col_idx + 1 # ID 1 sampai 16
                    
                    # Cek apakah tombol ini sudah diklik user di langkah ini?
                    # (Opsional: jika ingin tombol berubah warna setelah diklik, butuh logika tambahan.
                    # Di sini kita buat simpel: tombol biasa).
                    
                    if cols[col_idx].button(" ", key=f"btn_{block_id}_{len(cs['user_clicks'])}"):
                        cs["user_clicks"].append(block_id)
                        st.rerun()

        # --- LOGIC: CEK JAWABAN ---
        # Cek setiap kali user klik (Real-time check) atau tunggu sampai jumlah klik sama
        if len(cs["user_clicks"]) == len(cs["sequence"]):
            
            if cs["user_clicks"] == cs["sequence"]:
                # BENAR
                st.success("Benar! Lanjut level berikutnya...")
                time.sleep(1)
                cs["results"][f"Level_{cs['level']}"] = 1
                cs["level"] += 1
                cs["attempt"] = 1
                cs["status"] = "init"
                st.rerun()
            else:
                # SALAH
                if cs["attempt"] == 1:
                    st.warning("Salah. Anda punya 1 kesempatan lagi untuk urutan yang sama.")
                    time.sleep(2)
                    cs["attempt"] = 2
                    cs["user_clicks"] = []
                    cs["status"] = "blink" # Ulangi blink urutan yang sama
                    st.rerun()
                else:
                    st.error("Salah kedua kali. Tes Selesai.")
                    cs["results"][f"Level_{cs['level']}"] = 0
                    cs["status"] = "finished"
                    time.sleep(2)
                    return True # Return True menandakan tes selesai

    return False

# -------------------------------------------------------------
# MAIN APP
# -------------------------------------------------------------
def main():
    # Jika sudah selesai submit
    if st.session_state.get("thankyou", False):
        st.balloons()
        st.success("Terima kasih! Data Anda berhasil disimpan.")
        st.info("Silakan tutup tab browser ini.")
        return

    # Step 1: Identitas
    if not st.session_state.get("identity_completed", False):
        render_identity_form()
        return

    # Step 2: Kuesioner
    if not st.session_state.get("questionnaire_done", False):
        render_questionnaire()
        return

    # Step 3: Corsi
    finished = render_corsi()

    # Step 4: Submit Data
    if finished:
        cs = st.session_state.corsi
        
        # Hitung Max Level (Level terakhir yang sukses)
        passed_levels = [int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1]
        max_level = max(passed_levels) if passed_levels else 0

        total_iat = sum(st.session_state.answers.values())
        
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": total_iat,
            "corsi_max_level": max_level,
            "raw_results": str(cs["results"])
        }
        
        # Gabungkan semua data
        payload.update(st.session_state.identity_data)
        payload.update(st.session_state.answers)

        with st.spinner("Mengirim data..."):
            ok, info = send_to_webhook(payload)

        if ok:
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error(f"Gagal koneksi ke server: {info}. Silakan screenshot halaman ini dan kirim ke peneliti.")

if __name__ == "__main__":
    main()
