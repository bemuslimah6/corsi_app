import streamlit as st
import random
import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

st.set_page_config(
    page_title="Studi Memori Kerja",
    layout="centered"
)

# ---------------------------------------------------------
# CSS STYLING (FIX: KOTAK PRESISI & UKURAN TOMBOL)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 1. KOTAK JAWABAN (Tombol Biasa/Secondary) 
       Ini dipaksa menjadi KOTAK (Persegi) 1:1 */
    div.stButton > button {
        width: 100%;
        aspect-ratio: 1 / 1; 
        border-radius: 8px;
        border: 2px solid #CBD5E0;
        background-color: #EDF2F7;
        padding: 0;
        transition: all 0.1s;
    }
    
    /* Efek Hover di Kotak Jawaban */
    div.stButton > button:hover {
        border-color: #3182CE;
        background-color: #EBF8FF;
        transform: scale(0.98);
    }

    /* Efek Klik Manual (Saat ditekan) */
    div.stButton > button:active {
        background-color: #48BB78 !important;
        color: white;
    }

    /* 2. TOMBOL NAVIGASI (Mulai, Lanjut, dll)
       Tombol dengan type="primary" ukurannya DIKEMBALIKAN NORMAL (Persegi Panjang)
       supaya tidak jadi kotak raksasa. */
    div.stButton > button[kind="primary"] {
        aspect-ratio: unset !important; /* Batalkan rasio 1:1 */
        width: auto !important;         /* Lebar menyesuaikan teks */
        min-width: 120px;
        padding: 0.5rem 1rem;
        background-color: #FF4B4B;      /* Warna Merah Streamlit */
        border: none;
        color: white;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background-color: #FF2B2B;
        transform: none; /* Jangan mengecil saat hover */
    }

    /* 3. GRID HTML MANUAL (Untuk Fase Soal/Blink) */
    .corsi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem; /* Jarak antar kotak disamakan dengan st.columns */
        width: 100%;
    }
    .corsi-box {
        aspect-ratio: 1 / 1;
        border-radius: 8px;
        background: #EDF2F7;
        border: 2px solid #CBD5E0;
    }
    
    /* Warna Biru (Soal) */
    .corsi-active-blue {
        background: #3182CE !important;
        border-color: #2B6CB0;
        box-shadow: 0 0 15px rgba(49, 130, 206, 0.5);
    }

    /* Warna Hijau (Feedback Klik User) */
    .corsi-active-green {
        background: #48BB78 !important;
        border-color: #2F855A;
        box-shadow: 0 0 15px rgba(72, 187, 120, 0.5);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA & HELPERS
# ---------------------------------------------------------
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

def send_to_webhook(payload):
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, str(e)

def generate_positions():
    pos = list(range(1, 17))
    random.shuffle(pos)
    return pos

def generate_sequence(level):
    return random.sample(range(1, 17), level + 1)

def render_grid_html(positions, active=None, color_mode="blue"):
    """
    Render grid visual (HTML) untuk soal atau feedback.
    """
    html = '<div class="corsi-grid">'
    for p in positions:
        extra_class = ""
        if p == active:
            extra_class = "corsi-active-green" if color_mode == "green" else "corsi-active-blue"
        html += f'<div class="corsi-box {extra_class}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def blink_sequence(sequence, positions, container):
    """
    Menjalankan animasi kedip di dalam container tertentu.
    """
    # Tampilan awal (Mati)
    with container:
        render_grid_html(positions, active=None)
    time.sleep(1)

    for pid in sequence:
        # NYALA (Biru)
        with container:
            render_grid_html(positions, active=pid, color_mode="blue")
        time.sleep(0.7) # Durasi nyala
        
        # MATI
        with container:
            render_grid_html(positions, active=None)
        time.sleep(0.3) # Jeda antar kotak

# ---------------------------------------------------------
# HALAMAN 1: IDENTITAS
# ---------------------------------------------------------
def render_identity_form():
    st.header("Data Responden")

    inisial = st.text_input("Inisial (wajib)")
    umur = st.number_input("Umur", min_value=17, max_value=80, step=1)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
    kota = st.text_input("Domisili (Kota/Kabupaten)")
    durasi = st.selectbox("Durasi layar/hari", ["Pilih...", "< 1 jam", "1–2 jam", "2–4 jam", "4–6 jam", "> 6 jam"])
    aktivitas = st.selectbox("Aktivitas utama", ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])
    sebelum_tidur = st.radio("Gawai sebelum tidur?", ["Ya", "Tidak"])
    kualitas_tidur = st.selectbox("Kualitas tidur", ["Pilih...", "Baik", "Sedang", "Buruk"])
    durasi_tidur = st.selectbox("Durasi tidur", ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])
    gangguan = st.selectbox("Riwayat gangguan fokus", ["Pilih...", "Tidak ada", "ADHD", "Slow learner", "Lainnya"])
    kesehatan = st.selectbox("Riwayat kesehatan kognitif", ["Pilih...", "Tidak ada", "Cedera kepala", "Riwayat kejang", "Obat fokus"])
    kafein = st.selectbox("Konsumsi kafein", ["Pilih...", "Tidak pernah", "1x sehari", "2x sehari", "3x atau lebih"])

    # GUNAKAN TYPE="PRIMARY" AGAR TOMBOL TETAP PERSEGI PANJANG (NORMAL)
    if st.button("Lanjut ke Kuesioner", type="primary"):
        if inisial.strip() == "" or pendidikan == "Pilih..." or kota.strip() == "":
            st.error("Lengkapi semua data wajib.")
        else:
            st.session_state.identity_completed = True
            st.session_state.identity_data = {
                "inisial": inisial, "umur": int(umur), "jenis_kelamin": gender,
                "pendidikan": pendidikan, "kota": kota, "durasi_layar": durasi,
                "aktivitas_gawai": aktivitas, "sebelum_tidur": sebelum_tidur,
                "kualitas_tidur": kualitas_tidur, "durasi_tidur": durasi_tidur,
                "riwayat_gangguan_fokus": gangguan, "riwayat_kesehatan": kesehatan, "kafein": kafein
            }
            st.rerun()

# ---------------------------------------------------------
# HALAMAN 2: KUESIONER
# ---------------------------------------------------------
def render_questionnaire():
    st.header("Bagian 1 — IAT")
    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        answers[f"Q{i}"] = st.radio(f"{i}. {q}", [1, 2, 3, 4], horizontal=True, key=f"q{i}")

    # GUNAKAN TYPE="PRIMARY"
    if st.button("Selesai → Tes Corsi", type="primary"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()

# ---------------------------------------------------------
# HALAMAN 3: TES CORSI (INTI LOGIKA)
# ---------------------------------------------------------
def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1, "positions": None, "sequence": None,
            "user_clicks": [], "attempt": 1, "results": {}, "status": "idle"
        }
    cs = st.session_state.corsi

    # Setup Level Baru
    if cs["positions"] is None:
        cs["positions"] = generate_positions()
        cs["sequence"] = generate_sequence(cs["level"])
        cs["user_clicks"] = []
        cs["status"] = "idle"

    # LAYOUT: Gunakan kolom tengah agar game tidak melebar
    col_left, col_game, col_right = st.columns([1, 3, 1])

    with col_game:
        # 1. FASE PERSIAPAN (IDLE)
        if cs["status"] == "idle":
            st.info(f"Level {cs['level']} | Ingat {len(cs['sequence'])} kotak")
            render_grid_html(cs["positions"], active=None)
            
            # Tombol Mulai (Primary = Persegi Panjang)
            if st.button("Mulai Level Ini", type="primary", use_container_width=True):
                cs["status"] = "blink"
                st.rerun()
            return False # RETURN PENTING: Stop render apapun di bawah ini

        # 2. FASE SOAL (BLINK)
        if cs["status"] == "blink":
            # Placeholder untuk animasi
            grid_placeholder = st.empty()
            blink_sequence(cs["sequence"], cs["positions"], grid_placeholder)
            
            # Setelah animasi selesai, pindah status
            cs["status"] = "input"
            st.rerun()
            return False # RETURN PENTING: Jangan render tombol input dulu

        # 3. FASE JAWABAN (INPUT)
        if cs["status"] == "input":
            st.write("👉 Klik sesuai urutan:")
            
            # Placeholder agar kita bisa menimpa grid tombol dengan grid visual (feedback)
            input_placeholder = st.empty()
            
            clicked_pos = None
            
            with input_placeholder.container():
                # --- FIX GRID 4x4 (Menggunakan Nested Loop) ---
                # Jangan pakai cols = st.columns(4) di luar loop!
                for row in range(4):
                    row_cols = st.columns(4) # Bikin kolom baru tiap baris
                    for col in range(4):
                        # Hitung index 0 sampai 15
                        idx = row * 4 + col
                        pos_val = cs["positions"][idx]
                        
                        # Tombol Grid (Default/Secondary = KOTAK)
                        # Key unik: btn_posisi_jumlahklik
                        if row_cols[col].button(" ", key=f"btn_{pos_val}_{len(cs['user_clicks'])}"):
                            clicked_pos = pos_val

            # --- LOGIKA KLIK & FEEDBACK HIJAU ---
            if clicked_pos is not None:
                # 1. Timpa seluruh input container dengan gambar grid HIJAU di posisi yg diklik
                with input_placeholder:
                    render_grid_html(cs["positions"], active=clicked_pos, color_mode="green")
                
                # 2. Jeda sebentar supaya mata user lihat hijaunya
                time.sleep(0.25)
                
                # 3. Simpan & Reload
                cs["user_clicks"].append(clicked_pos)
                st.rerun()

            # --- CEK JAWABAN SETELAH RELOAD ---
            if len(cs["user_clicks"]) == len(cs["sequence"]):
                if cs["user_clicks"] == cs["sequence"]:
                    # BENAR
                    cs["results"][f"Level_{cs['level']}"] = 1
                    cs["level"] += 1
                    cs["positions"] = None
                    cs["attempt"] = 1
                    st.success("Benar! Lanjut...")
                    time.sleep(0.8)
                    st.rerun()
                else:
                    # SALAH
                    if cs["attempt"] == 1:
                        cs["attempt"] = 2
                        cs["user_clicks"] = []
                        st.warning("Salah urutan. Coba lagi.")
                        time.sleep(1.5)
                        cs["status"] = "blink" # Ulangi soal
                        st.rerun()
                    else:
                        cs["results"][f"Level_{cs['level']}"] = 0
                        cs["status"] = "finished"
                        st.error("Game Over.")
                        return True

    return False

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    st.title("Studi Kognitif")

    if st.session_state.get("thankyou", False):
        st.success("Terima kasih. Data tersimpan.")
        if st.button("Reset", type="primary"):
            st.session_state.clear()
            st.rerun()
        return

    if not st.session_state.get("identity_completed", False):
        render_identity_form()
        return

    if not st.session_state.get("questionnaire_done", False):
        render_questionnaire()
        return

    finished = render_corsi()

    if finished:
        cs = st.session_state.corsi
        # Hitung skor
        passed = [int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1]
        max_lvl = max(passed) if passed else 0

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": sum(st.session_state.answers.values()),
            "corsi_max_level": max_lvl
        }
        payload.update(st.session_state.identity_data)
        payload.update(st.session_state.answers)
        payload.update(cs["results"])

        with st.spinner("Menyimpan data..."):
            ok, info = send_to_webhook(payload)
        
        if ok:
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error("Gagal kirim data.")
            if st.button("Coba Lagi", type="primary"):
                st.rerun()

if __name__ == "__main__":
    main()
