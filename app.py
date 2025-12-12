import streamlit as st
import random
import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

st.set_page_config(page_title="Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja", layout="centered")

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

# ---------------- HELPER TO SEND DATA ----------------
def send_to_webhook(payload):
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200
    except:
        return False

# ---------------- IDENTITY FORM ----------------
def render_identity_form():

    st.header("Data Responden")

    st.write("""
    Terima kasih telah berpartisipasi dalam penelitian ini.  
    Aplikasi ini digunakan untuk **kepentingan akademik**, dan seluruh data dijaga kerahasiaannya.

    **Dengan melanjutkan, Anda menyetujui penggunaan data untuk penelitian.**
    """)

    inisial = st.text_input("Inisial (wajib)")
    umur = st.number_input("Umur", 17, 28)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
    kota = st.text_input("Domisili (Kota/Kabupaten)")

    durasi = st.selectbox("Durasi penggunaan layar per hari",
                          ["Pilih...", "< 1 jam", "1–2 jam", "2–4 jam", "4–6 jam", "> 6 jam"])

    aktivitas = st.selectbox("Aktivitas gawai utama",
                             ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])

    sebelum_tidur = st.radio("Menggunakan gawai sebelum tidur?", ["Ya", "Tidak"])

    kualitas_tidur = st.selectbox("Kualitas tidur", ["Pilih...", "Baik", "Sedang", "Buruk"])

    durasi_tidur = st.selectbox("Durasi tidur per hari",
                                ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])

    gangguan_fokus = st.selectbox("Riwayat gangguan fokus / belajar",
                                  ["Pilih...", "Tidak ada", "ADHD", "Slow learner", "Gangguan bahasa", "Kesulitan pemrosesan pendengaran"])

    riwayat_kognitif = st.selectbox("Riwayat kesehatan kognitif",
                                    ["Pilih...", "Tidak ada", "Cedera kepala", "Riwayat kejang", "Obat yang mempengaruhi fokus"])

    kafein = st.selectbox("Konsumsi kafein", ["Pilih...", "Tidak pernah", "1x", "2x", "3x+"])

    if st.button("Lanjut ke Kuesioner"):

        missing = (
            inisial.strip() == "" or pendidikan=="Pilih..." or kota.strip()=="" or
            durasi=="Pilih..." or aktivitas=="Pilih..." or kualitas_tidur=="Pilih..."
            or durasi_tidur=="Pilih..." or gangguan_fokus=="Pilih..." or 
            riwayat_kognitif=="Pilih..." or kafein=="Pilih..."
        )

        if missing:
            st.error("Semua field wajib diisi.")
        else:
            st.session_state.identity_completed = True
            st.session_state.identity_data = {
                "inisial": inisial,
                "umur": umur,
                "jenis_kelamin": gender,
                "pendidikan": pendidikan,
                "kota": kota,
                "durasi_layar": durasi,
                "aktivitas_gawai": aktivitas,
                "sebelum_tidur": sebelum_tidur,
                "kualitas_tidur": kualitas_tidur,
                "durasi_tidur": durasi_tidur,
                "gangguan_fokus": gangguan_fokus,
                "riwayat_kognitif": riwayat_kognitif,
                "kafein": kafein
            }
            st.rerun()

# ---------------- QUESTIONNAIRE ----------------
def render_questionnaire():

    st.header("Bagian 1 — Kuesioner Internet Addiction Test (IAT)")

    st.write("""
    **Petunjuk:**  
    Jawablah sesuai kondisi Anda.  
    - 1 = Sangat Tidak Setuju  
    - 2 = Tidak Setuju  
    - 3 = Setuju  
    - 4 = Sangat Setuju  
    """)

    answers = {}

    for i, q in enumerate(QUESTIONS, 1):
        answers[f"Q{i}"] = st.radio(
            f"**{i}. {q}**", [1, 2, 3, 4], horizontal=True, key=f"q{i}"
        )

    if st.button("Selesai → Lanjut Tes Corsi"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()

# ---------------- CORSI 4×4 MOBILE FRIENDLY ----------------
def generate_positions():
    pos = list(range(1, 17))
    random.shuffle(pos)
    return pos

def generate_sequence(level):
    return random.sample(range(1, 17), level + 1)

def blink(sequence, positions):
    placeholder = st.empty()
    for pid in sequence:
        with placeholder.container():

            html = "<div style='display:grid;grid-template-columns:repeat(4,65px);gap:10px;justify-content:center;'>"

            for b in positions:
                if b == pid:
                    html += "<div style='height:65px;background:#2B6CB0;border-radius:10px;'></div>"
                else:
                    html += "<div style='height:65px;background:#E2E8F0;border-radius:10px;'></div>"

            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        time.sleep(0.55)
        placeholder.empty()

    time.sleep(0.15)

def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi 4×4")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "positions": None,
            "sequence": None,
            "attempt": 1,
            "user_clicks": [],
            "results": {},
            "status": "idle"
        }

    cs = st.session_state.corsi

    # INIT LEVEL
    if cs["positions"] is None:
        cs["positions"] = generate_positions()
        cs["sequence"] = generate_sequence(cs["level"])
        cs["user_clicks"] = []
        cs["status"] = "idle"

    # Idle
    if cs["status"] == "idle":
        st.info(f"Level {cs['level']} — panjang urutan: {len(cs['sequence'])}")
        if st.button("Mulai Blink"):
            cs["status"] = "blink"
            st.rerun()
        return False

    # Blink
    if cs["status"] == "blink":
        blink(cs["sequence"], cs["positions"])
        cs["status"] = "input"
        st.rerun()
        return False

    # Input Mode - MOBILE FRIENDLY GRID
    if cs["status"] == "input":

        st.write("Klik kotak sesuai urutan blink tadi:")

        st.markdown("""
            <style>
            .grid{
                display:grid;
                grid-template-columns:repeat(4,65px);
                gap:10px;
                justify-content:center;
            }
            .box{
                width:65px;height:65px;
                border-radius:10px;
                background:#E2E8F0;
            }
            .box.selected{
                background:#38A169 !important;
            }
            </style>
        """, unsafe_allow_html=True)

        # HTML CLICK GRID
        html = "<div class='grid'>"
        for pid in cs["positions"]:
            selected = "selected" if pid in cs["user_clicks"] else ""
            html += f"""
                <div class='box {selected}' onclick="parent.postMessage({{'click': {pid}}}, '*')"></div>
            """
        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)

        # Listen to JS → Python
        msg = st.experimental_get_query_params().get("click", [None])[0]

        if msg and msg != "None":
            pid = int(msg)
            if pid not in cs["user_clicks"]:
                cs["user_clicks"].append(pid)

            st.experimental_set_query_params(click=None)
            st.rerun()

        st.write(f"Klik: {len(cs['user_clicks'])}/{len(cs['sequence'])}")

    # Evaluate
    if len(cs["user_clicks"]) == len(cs["sequence"]):

        if cs["user_clicks"] == cs["sequence"]:
            # BENAR
            cs["results"][f"Level_{cs['level']}"] = 1
            cs["level"] += 1
            cs["attempt"] = 1
            cs["positions"] = None
            st.success("Benar! Naik level.")
            st.rerun()
            return False

        # SALAH
        if cs["attempt"] == 1:
            cs["attempt"] = 2
            cs["user_clicks"] = []
            st.warning("Salah. Kesempatan 1x lagi.")
            st.rerun()
            return False
        else:
            cs["results"][f"Level_{cs['level']}"] = 0
            cs["status"] = "finished"
            st.error("Salah dua kali. Tes selesai.")
            return True

    return False

# ---------------- MAIN ----------------
def main():

    st.title("Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja")

    if st.session_state.get("thankyou", False):
        st.success("Terima kasih! Data telah direkam.")
        return

    if not st.session_state.get("identity_completed", False):
        render_identity_form()
        return

    if not st.session_state.get("questionnaire_done", False):
        render_questionnaire()
        return

    is_finished = render_corsi()

    if is_finished:

        cs = st.session_state.corsi

        max_level = max([int(k.split("_")[1]) for k,v in cs["results"].items() if v==1], default=0)
        total_iat = sum(st.session_state.answers.values())
        total_benar = sum(1 for v in cs["results"].values() if v == 1)
        total_salah = sum(1 for v in cs["results"].values() if v == 0)

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": total_iat,
            "corsi_max_level": max_level,
            "corsi_total_benar": total_benar,
            "corsi_total_salah": total_salah,
        }

        payload.update(st.session_state.identity_data)
        payload.update(st.session_state.answers)
        payload.update(cs["results"])

        if send_to_webhook(payload):
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error("Gagal mengirim data. Periksa koneksi internet.")

if __name__ == "__main__":
    main()
