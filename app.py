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
# CSS STYLING (PERBAIKAN TAMPILAN)
# ---------------------------------------------------------
st.markdown("""
<style>
    /* Membuat tombol di dalam kolom (grid corsi) menjadi persegi */
    div[data-testid="stHorizontalBlock"] button {
        aspect-ratio: 1 / 1;
        width: 100% !important;
        border-radius: 10px;
        border: 2px solid #E2E8F0;
        background-color: #F7FAFC;
        transition: all 0.2s;
    }
    
    /* Efek hover agar lebih interaktif */
    div[data-testid="stHorizontalBlock"] button:hover {
        background-color: #BEE3F8;
        border-color: #3182CE;
        transform: scale(0.98);
    }

    /* Grid HTML manual (untuk fase blink) */
    .corsi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1rem; /* Jarak antar kotak disamakan dengan st.columns */
        max-width: 100%;
        margin: auto;
    }
    .corsi-box {
        aspect-ratio: 1 / 1;
        border-radius: 10px;
        background: #F7FAFC; /* Warna default (mati) */
        border: 2px solid #E2E8F0;
    }
    .corsi-active {
        background: #3182CE !important; /* Warna saat menyala (Biru) */
        box-shadow: 0 0 15px rgba(49, 130, 206, 0.6);
        transform: scale(1.05);
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

def render_grid_html(positions, active=None):
    """
    Fungsi ini merender grid menggunakan HTML murni untuk fase 'Blink'.
    """
    html = '<div class="corsi-grid">'
    for p in positions:
        # Jika posisi p sama dengan yang aktif, beri kelas 'corsi-active'
        active_class = "corsi-active" if p == active else ""
        html += f'<div class="corsi-box {active_class}"></div>'
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def blink_sequence(sequence, positions):
    """
    Menampilkan urutan nyala.
    PERBAIKAN: Tidak menggunakan st.empty() untuk menghindari layout shift.
    Melainkan menimpa konten dengan layout 'mati' saat jeda.
    """
    grid_placeholder = st.empty()
    
    # Tampilkan grid mati dulu sebentar
    with grid_placeholder:
        render_grid_html(positions, active=None)
    time.sleep(1)

    for pid in sequence:
        # 1. NYALA (Render dengan active=pid)
        with grid_placeholder:
            render_grid_html(positions, active=pid)
        time.sleep(0.7) # Durasi nyala
        
        # 2. MATI (Render dengan active=None)
        # Jangan gunakan placeholder.empty(), tapi render grid mati agar layout tetap diam
        with grid_placeholder:
            render_grid_html(positions, active=None)
        time.sleep(0.3) # Durasi jeda antar blok

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

    # Setup awal level baru
    if cs["positions"] is None:
        cs["positions"] = generate_positions()
        cs["sequence"] = generate_sequence(cs["level"])
        cs["user_clicks"] = []
        cs["status"] = "idle"

    # --- STATE: IDLE (Persiapan) ---
    if cs["status"] == "idle":
        st.info(f"Level {cs['level']} | Panjang Urutan: {len(cs['sequence'])}")
        st.write("Perhatikan urutan kotak yang menyala biru.")
        
        # Tampilkan grid statis sebagai preview
        render_grid_html(cs["positions"], active=None)
        
        if st.button("Mulai Level Ini", type="primary"):
            cs["status"] = "blink"
            st.rerun()
        return False

    # --- STATE: BLINK (Menampilkan Urutan) ---
    if cs["status"] == "blink":
        # Jalankan animasi blink
        blink_sequence(cs["sequence"], cs["positions"])
        # Setelah selesai, pindah ke input
        cs["status"] = "input"
        st.rerun()
        return False

    # --- STATE: INPUT (User Menjawab) ---
    if cs["status"] == "input":
        st.write("👉 **Klik kotak sesuai urutan yang tadi menyala:**")

        # Buat Grid Input menggunakan st.columns
        # CSS di atas sudah memaksa tombol di sini menjadi kotak (persegi)
        cols = st.columns(4)
        for i, pos in enumerate(cs["positions"]):
            # Tombol diberi label kosong " "
            # Key harus unik setiap klik agar state terdeteksi
            if cols[i % 4].button(" ", key=f"btn_{pos}_{len(cs['user_clicks'])}"):
                cs["user_clicks"].append(pos)
                st.rerun()

        # Logika Pengecekan
        if len(cs["user_clicks"]) == len(cs["sequence"]):
            if cs["user_clicks"] == cs["sequence"]:
                # BENAR
                cs["results"][f"Level_{cs['level']}"] = 1
                cs["level"] += 1
                cs["positions"] = None # Reset posisi untuk level baru
                cs["attempt"] = 1
                st.success("Benar! Lanjut ke level berikutnya...")
                time.sleep(1)
                st.rerun()
            else:
                # SALAH
                if cs["attempt"] == 1:
                    cs["attempt"] = 2
                    cs["user_clicks"] = []
                    st.warning("Salah urutan. Coba sekali lagi pada level yang sama.")
                    time.sleep(1.5)
                    cs["status"] = "blink" # Ulangi blink
                    st.rerun()
                else:
                    cs["results"][f"Level_{cs['level']}"] = 0
                    cs["status"] = "finished"
                    st.error("Salah dua kali. Tes selesai.")
                    return True # Mengembalikan True = Selesai

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
        
        # Hitung level maksimum yang berhasil
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
                # Logic retry sederhana
                ok_retry, info_retry = send_to_webhook(payload)
                if ok_retry:
                    st.session_state.thankyou = True
                    st.rerun()

if __name__ == "__main__":
    main()
