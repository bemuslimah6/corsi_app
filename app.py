import streamlit as st
import random
import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

st.set_page_config(
    page_title="Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja",
    layout="centered"
)

# ---------------------------------------------------------
# CSS STYLING (PERBAIKAN TAMPILAN PRESISI)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Styling Tombol Streamlit agar menjadi kotak sempurna */
    div.stButton > button {
        width: 100%;
        aspect-ratio: 1 / 1;
        border-radius: 8px;
        border: 2px solid #CBD5E0;
        background-color: #EDF2F7;
        transition: all 0.1s;
    }
    
    div.stButton > button:hover {
        border-color: #3182CE;
        background-color: #EBF8FF;
    }

    div.stButton > button:active {
        background-color: #48BB78 !important; /* Hijau saat ditekan manual */
        color: white;
    }

    /* Grid HTML Manual (Untuk fase Blink Soal) */
    .corsi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 0.8rem; /* Gap disesuaikan agar mirip st.columns */
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
        box-shadow: 0 0 10px rgba(49, 130, 206, 0.5);
        transform: scale(0.98);
    }

    /* Warna Hijau (Feedback Klik User) */
    .corsi-active-green {
        background: #48BB78 !important;
        border-color: #2F855A;
        box-shadow: 0 0 10px rgba(72, 187, 120, 0.5);
        transform: scale(0.95);
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 18 ITEM KUESIONER (IAT Indonesia)
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

# ---------------------------------------------------------
# HELPERS
# ---------------------------------------------------------
def send_to_webhook(payload):
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, str(e)

# ---------------------------------------------------------
# IDENTITY FORM
# ---------------------------------------------------------
def render_identity_form():
    st.header("Data Responden")

    inisial = st.text_input("Inisial (wajib)")
    umur = st.number_input("Umur", min_value=17, max_value=80, step=1)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
    kota = st.text_input("Domisili (Kota/Kabupaten)")

    durasi = st.selectbox("Durasi penggunaan layar per hari",
                          ["Pilih...", "< 1 jam", "1–2 jam", "2–4 jam", "4–6 jam", "> 6 jam"])

    aktivitas = st.selectbox("Aktivitas gawai utama",
                             ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])

    sebelum_tidur = st.radio("Menggunakan gawai sebelum tidur?", ["Ya", "Tidak"])
    kualitas_tidur = st.selectbox("Kualitas tidur", ["Pilih...", "Baik", "Sedang", "Buruk"])
    durasi_tidur = st.selectbox("Durasi tidur", ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])

    gangguan_fokus = st.selectbox(
        "Riwayat gangguan fokus",
        ["Pilih...", "Tidak ada", "ADHD", "Slow learner", "Gangguan bahasa", "Kesulitan pemrosesan pendengaran"]
    )

    riwayat_kesehatan = st.selectbox(
        "Riwayat kesehatan kognitif",
        ["Pilih...", "Tidak ada", "Cedera kepala", "Riwayat kejang", "Obat yang mempengaruhi fokus"]
    )

    kafein = st.selectbox("Konsumsi kafein",
                          ["Pilih...", "Tidak pernah", "1x sehari", "2x sehari", "3x atau lebih"])

    if st.button("Lanjut ke Kuesioner"):
        if inisial.strip() == "" or pendidikan == "Pilih..." or kota.strip() == "":
            st.error("Lengkapi semua data wajib.")
        else:
            st.session_state.identity_completed = True
            st.session_state.identity_data = {
                "inisial": inisial,
                "umur": int(umur),
                "jenis_kelamin": gender,
                "pendidikan": pendidikan,
                "kota": kota,
                "durasi_layar": durasi,
                "aktivitas_gawai": aktivitas,
                "sebelum_tidur": sebelum_tidur,
                "kualitas_tidur": kualitas_tidur,
                "durasi_tidur": durasi_tidur,
                "riwayat_gangguan_fokus": gangguan_fokus,
                "riwayat_kesehatan": riwayat_kesehatan,
                "kafein": kafein
            }
            st.rerun()

# ---------------------------------------------------------
# QUESTIONNAIRE
# ---------------------------------------------------------
def render_questionnaire():
    st.header("Bagian 1 — Internet Addiction Test (IAT)")

    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        answers[f"Q{i}"] = st.radio(
            f"{i}. {q}", [1, 2, 3, 4], horizontal=True, key=f"q{i}"
        )

    if st.button("Selesai → Tes Corsi"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()

# ---------------------------------------------------------
# CORSI HELPERS
# ---------------------------------------------------------
def generate_positions():
    pos = list(range(1, 17))
    random.shuffle(pos)
    return pos

def generate_sequence(level):
    return random.sample(range(1, 17), level + 1)

def render_grid_html(positions, active=None, color_mode="blue"):
    """
    Render grid menggunakan HTML.
    active: ID kotak yang sedang menyala.
    color_mode: 'blue' untuk soal, 'green' untuk feedback klik user.
    """
    html = '<div class="corsi-grid">'
    for p in positions:
        extra_class = ""
        if p == active:
            if color_mode == "green":
                extra_class = "corsi-active-green"
            else:
                extra_class = "corsi-active-blue"
        
        html += f'<div class="corsi-box {extra_class}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def blink_sequence(sequence, positions, container):
    """
    Menampilkan urutan blink di dalam container tertentu.
    """
    # Tampilan awal mati
    with container:
        render_grid_html(positions, active=None)
    time.sleep(1)

    for pid in sequence:
        # NYALA
        with container:
            render_grid_html(positions, active=pid, color_mode="blue")
        time.sleep(0.7) # Lama nyala
        
        # MATI
        with container:
            render_grid_html(positions, active=None)
        time.sleep(0.3) # Jeda antar blink

# ---------------------------------------------------------
# CORSI TEST
# ---------------------------------------------------------
def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi Block Tapping")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "positions": None,
            "sequence": None,
            "user_clicks": [],
            "attempt": 1,
            "results": {},
            "status": "idle"
        }

    cs = st.session_state.corsi

    if cs["positions"] is None:
        cs["positions"] = generate_positions()
        cs["sequence"] = generate_sequence(cs["level"])
        cs["user_clicks"] = []
        cs["status"] = "idle"

    # --- LAYOUT CENTERING ---
    # Kita pakai 3 kolom: [Kiri kosong, TENGAH ISI GAME, Kanan kosong]
    # Rasio [1, 2, 1] membuat area game tidak terlalu lebar
    col_left, col_game, col_right = st.columns([1, 2, 1])

    with col_game:
        # --- STATE: IDLE (Persiapan) ---
        if cs["status"] == "idle":
            st.info(f"Level {cs['level']} | Panjang Urutan: {len(cs['sequence'])}")
            render_grid_html(cs["positions"], active=None)
            
            if st.button("Mulai Level Ini", type="primary", use_container_width=True):
                cs["status"] = "blink"
                st.rerun()
            return False

        # --- STATE: BLINK (Menampilkan Urutan) ---
        if cs["status"] == "blink":
            # Placeholder agar animasi berjalan mulus di tempat yang sama
            grid_placeholder = st.empty()
            blink_sequence(cs["sequence"], cs["positions"], grid_placeholder)
            cs["status"] = "input"
            st.rerun()
            return False

        # --- STATE: INPUT (User Menjawab) ---
        if cs["status"] == "input":
            st.write("👉 Klik sesuai urutan:")
            
            # Placeholder ini penting untuk efek BLINK HIJAU (feedback)
            # Sebelum tombol dirender ulang, kita akan 'menimpa' area ini dengan gambar grid hijau
            game_placeholder = st.empty()

            with game_placeholder:
                # Kita render tombol di dalam placeholder
                # Menggunakan st.columns(4) agar grid tombol 4x4
                # Karena ini ada di dalam 'col_game' (yang sudah dipersempit),
                # maka ukurannya akan pas dengan grid HTML di atas.
                rows = [st.columns(4) for _ in range(4)]
                
                # Mapping posisi 1-16 ke grid 4x4
                # positions diacak, tapi kita urutkan tampilannya berdasarkan index list
                # agar layout tetap rapi, tapi logic tombolnya benar.
                
                # Logic: Kita iterasi tombol berdasarkan urutan grid visual (kiri-kanan, atas-bawah)
                # Tapi ID tombolnya diambil dari cs["positions"]
                
                clicked_pos = None

                for i, pos in enumerate(cs["positions"]):
                    row_idx = i // 4
                    col_idx = i % 4
                    
                    # Render tombol kosong
                    if rows[row_idx][col_idx].button(" ", key=f"btn_{pos}_{len(cs['user_clicks'])}"):
                        clicked_pos = pos

                # --- LOGIC FEEDBACK HIJAU ---
                if clicked_pos is not None:
                    # 1. Timpa tombol dengan Gambar Grid HTML (Salah satu kotak Hijau)
                    # Ini memberi efek visual instan bahwa klik diterima
                    render_grid_html(cs["positions"], active=clicked_pos, color_mode="green")
                    
                    # 2. Pause sebentar agar mata user melihat warna hijau
                    time.sleep(0.2)
                    
                    # 3. Simpan data & Rerun
                    cs["user_clicks"].append(clicked_pos)
                    st.rerun()

            # --- LOGIC PENILAIAN ---
            if len(cs["user_clicks"]) == len(cs["sequence"]):
                if cs["user_clicks"] == cs["sequence"]:
                    # BENAR
                    cs["results"][f"Level_{cs['level']}"] = 1
                    cs["level"] += 1
                    cs["positions"] = None 
                    cs["attempt"] = 1
                    st.success("Benar! Lanjut...")
                    time.sleep(1)
                    st.rerun()
                else:
                    # SALAH
                    if cs["attempt"] == 1:
                        cs["attempt"] = 2
                        cs["user_clicks"] = []
                        st.warning("Salah urutan. Coba sekali lagi.")
                        time.sleep(1.5)
                        cs["status"] = "blink"
                        st.rerun()
                    else:
                        cs["results"][f"Level_{cs['level']}"] = 0
                        cs["status"] = "finished"
                        st.error("Tes Selesai.")
                        return True

    return False

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
def main():
    st.title("Studi Kognitif")

    if st.session_state.get("thankyou", False):
        st.success("Terima kasih. Data berhasil disimpan.")
        if st.button("Isi Ulang (Reset)"):
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
        
        passed_levels = [int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1]
        max_level = max(passed_levels) if passed_levels else 0

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": sum(st.session_state.answers.values()),
            "corsi_max_level": max_level
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
            st.error(f"Gagal menyimpan data: {info}")
            if st.button("Coba Kirim Lagi"):
                ok_retry, info_retry = send_to_webhook(payload)
                if ok_retry:
                    st.session_state.thankyou = True
                    st.rerun()

if __name__ == "__main__":
    main()
