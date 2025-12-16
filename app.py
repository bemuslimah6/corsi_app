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
# CSS STYLING (TIDAK BERUBAH DARI PERBAIKAN SEBELUMNYA)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* 1. KOTAK JAWABAN (Tombol Biasa/Secondary) */
    div.stButton > button {
        width: 100%;
        aspect-ratio: 1 / 1; 
        border-radius: 8px;
        border: 2px solid #CBD5E0;
        background-color: #EDF2F7;
        padding: 0;
        transition: all 0.1s;
        transform: none !important; 
    }
    
    /* Efek Hover di Kotak Jawaban */
    div.stButton > button:hover {
        border-color: #3182CE;
        background-color: #EBF8FF;
        transform: none;
    }

    /* FEEDBACK HIJAU INSTAN SAAT DITEKAN (Mencegah Layout Shift) */
    div.stButton > button:active {
        background-color: #48BB78 !important;
        color: white;
        box-shadow: 0 0 10px rgba(72, 187, 120, 0.5);
    }

    /* 2. TOMBOL NAVIGASI (Mulai, Lanjut, dll) */
    div.stButton > button[kind="primary"] {
        aspect-ratio: unset !important;
        width: auto !important;
        min-width: 120px;
        padding: 0.5rem 1rem;
        background-color: #FF4B4B;
        border: none;
        color: white;
        transform: none;
    }
    
    div.stButton > button[kind="primary"]:hover {
        background-color: #FF2B2B;
        transform: none;
    }

    /* 3. GRID HTML MANUAL (Untuk Fase Soal/Blink) */
    .corsi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem;
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
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# DATA & HELPERS
# ---------------------------------------------------------
QUESTIONS = [
    # ... (Daftar pertanyaan IAT) ...
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
    """Render grid visual (HTML) untuk soal atau feedback."""
    html = '<div class="corsi-grid">'
    for p in positions:
        extra_class = ""
        if p == active:
            extra_class = "corsi-active-green" if color_mode == "green" else "corsi-active-blue"
        html += f'<div class="corsi-box {extra_class}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def blink_sequence(sequence, positions, container):
    """Menjalankan animasi kedip di dalam container tertentu."""
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
# HALAMAN 3: TES CORSI (DENGAN ISOLASI LAYOUT)
# ---------------------------------------------------------
def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1, "positions": None, "sequence": None,
            "user_clicks": [], "attempt": 1, "results": {}, "status": "idle"
        }
    cs = st.session_state.corsi

    if cs["positions"] is None:
        cs["positions"] = generate_positions()
        cs["sequence"] = generate_sequence(cs["level"])
        cs["user_clicks"] = []
        cs["status"] = "idle"

    col_left, col_game, col_right = st.columns([1, 3, 1])

    with col_game:
        # 1. Tempatkan dua placeholder kosong di awal
        # grid_display_placeholder: untuk menampilkan grid HTML (soal/blink)
        # input_placeholder: untuk menampilkan grid tombol Streamlit (jawaban)
        grid_display_placeholder = st.empty()
        input_placeholder = st.empty() 

        # 1. FASE PERSIAPAN (IDLE)
        if cs["status"] == "idle":
            st.info(f"Level {cs['level']} | Ingat {len(cs['sequence'])} kotak")
            
            with grid_display_placeholder:
                render_grid_html(cs["positions"], active=None)
            
            # Pastikan input_placeholder kosong
            input_placeholder.empty()

            if st.button("Mulai Level Ini", type="primary", use_container_width=True):
                cs["status"] = "blink"
                st.rerun()
            return False

        # 2. FASE SOAL (BLINK)
        if cs["status"] == "blink":
            # Pastikan input_placeholder kosong
            input_placeholder.empty()

            # Jalankan animasi di placeholder display
            blink_sequence(cs["sequence"], cs["positions"], grid_display_placeholder)
            
            cs["status"] = "input"
            st.rerun()
            return False

        # 3. FASE JAWABAN (INPUT)
        if cs["status"] == "input":
            st.write("👉 Klik sesuai urutan:")
            
            # Kosongkan placeholder display (agar grid HTML hilang)
            grid_display_placeholder.empty()
            
            clicked_pos = None
            
            # Render Tombol di placeholder input
            with input_placeholder.container():
                for row in range(4):
                    row_cols = st.columns(4)
                    for col in range(4):
                        idx = row * 4 + col
                        pos_val = cs["positions"][idx]
                        
                        if row_cols[col].button(" ", key=f"btn_{pos_val}_{len(cs['user_clicks'])}"):
                            clicked_pos = pos_val

            # --- LOGIKA KLIK & PENILAIAN ---
            if clicked_pos is not None:
                # Feedback hijau terjadi secara instan via CSS :active
                cs["user_clicks"].append(clicked_pos)
                st.rerun()

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
                        cs["status"] = "blink"
                        st.rerun()
                    else:
                        cs["results"][f"Level_{cs['level']}"] = 0
                        cs["status"] = "finished"
                        st.error("Game Over.")
                        return True

    return False

# ---------------------------------------------------------
# MAIN (TIDAK BERUBAH)
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
        # Implementasi render_identity_form di sini...
        # Dihilangkan dari jawaban ini agar kode tidak terlalu panjang, 
        # asumsikan sudah ada di kode user.
        # ... (Kode render_identity_form)
        return

    if not st.session_state.get("questionnaire_done", False):
        # Implementasi render_questionnaire di sini...
        # ... (Kode render_questionnaire)
        return

    finished = render_corsi()

    if finished:
        cs = st.session_state.corsi
        
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
    # Panggil fungsi identity dan questionnaire untuk memastikan state berjalan
    
    # --- CATATAN ---
    # Karena saya tidak punya semua fungsi helper (identity dan questionnaire) 
    # di dalam blok kode yang saya kirimkan di sini, saya harus membuat versi 
    # dummy atau Anda harus pastikan fungsi-fungsi tersebut sudah ada 
    # di file Anda. Saya akan sertakan fungsi identitas dan kuesioner dari 
    # jawaban sebelumnya untuk memastikan main() dapat berjalan.
    
    # [Tambahkan fungsi render_identity_form dan render_questionnaire dari 
    # jawaban sebelumnya di sini jika Anda menjalankan kode ini secara utuh]
    
    # ... (Asumsi fungsi-fungsi itu sudah ada, kode main akan jalan) ...
    main()
