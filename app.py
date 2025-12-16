import streamlit as st
import streamlit.components.v1 as components
import random
import requests
import time
from datetime import datetime

# =========================================================
# CONFIG
# =========================================================
WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

st.set_page_config(
    page_title="Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja",
    layout="centered"
)

# =========================================================
# KUESIONER IAT
# =========================================================
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

# =========================================================
# WEBHOOK
# =========================================================
def send_to_webhook(payload):
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200
    except:
        return False

# =========================================================
# IDENTITAS
# =========================================================
def render_identity_form():
    st.header("Data Responden")

    inisial = st.text_input("Inisial")
    umur = st.number_input("Umur", min_value=17, max_value=80, step=1)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1"])
    kota = st.text_input("Domisili")

    if st.button("Lanjut"):
        if inisial.strip() == "" or pendidikan == "Pilih..." or kota.strip() == "":
            st.error("Lengkapi data wajib.")
        else:
            st.session_state.identity_completed = True
            st.session_state.identity_data = {
                "inisial": inisial,
                "umur": umur,
                "gender": gender,
                "pendidikan": pendidikan,
                "kota": kota
            }
            st.rerun()

# =========================================================
# KUESIONER
# =========================================================
def render_questionnaire():
    st.header("Bagian 1 — Internet Addiction Test (IAT)")

    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        answers[f"Q{i}"] = st.radio(q, [1, 2, 3, 4], horizontal=True)

    if st.button("Lanjut Tes Corsi"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()

# =========================================================
# CORSI GRID (SATU-SATUNYA RENDER)
# =========================================================
def render_corsi_grid(positions, highlight=None):
    boxes = ""
    for p in positions:
        color = "#E2E8F0"
        if highlight == p:
            color = "#38A169"
        boxes += f"""
        <div class="box" onclick="sendClick({p})"
             style="background:{color};"></div>
        """

    html = f"""
    <style>
    .grid {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 12px;
        width: 280px;
        margin: auto;
    }}
    .box {{
        aspect-ratio: 1 / 1;
        border-radius: 12px;
        cursor: pointer;
    }}
    </style>

    <div class="grid">{boxes}</div>

    <script>
    function sendClick(val) {{
        const url = new URL(window.location);
        url.searchParams.set("corsi_click", val);
        window.location.href = url.toString();
    }}
    </script>
    """
    components.html(html, height=320)

# =========================================================
# BLINK
# =========================================================
def blink(sequence, positions):
    placeholder = st.empty()
    for pid in sequence:
        with placeholder:
            render_corsi_grid(positions, highlight=pid)
        time.sleep(0.6)
        placeholder.empty()
        time.sleep(0.2)

# =========================================================
# CORSI TEST
# =========================================================
def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi Block Tapping")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "positions": random.sample(range(1, 17), 16),
            "sequence": [],
            "user_clicks": [],
            "attempt": 1,
            "results": {},
            "status": "idle"
        }

    cs = st.session_state.corsi

    # INIT LEVEL
    if cs["status"] == "idle":
        cs["sequence"] = random.sample(range(1, 17), cs["level"] + 1)
        cs["user_clicks"] = []
        st.info(f"Level {cs['level']} | Panjang urutan: {len(cs['sequence'])}")
        if st.button("Mulai"):
            cs["status"] = "blink"
            st.rerun()
        return False

    # BLINK
    if cs["status"] == "blink":
        blink(cs["sequence"], cs["positions"])
        cs["status"] = "input"
        st.rerun()
        return False

    # INPUT
    if cs["status"] == "input":
        st.write("Klik kotak sesuai urutan yang tadi menyala.")
        render_corsi_grid(cs["positions"])

        click = st.query_params.get("corsi_click", None)
        if click:
            click = int(click)
            st.query_params.clear()

            cs["user_clicks"].append(click)

            # BLINK HIJAU
            render_corsi_grid(cs["positions"], highlight=click)
            time.sleep(0.2)
            st.rerun()

    # EVALUASI
    if len(cs["user_clicks"]) == len(cs["sequence"]):
        if cs["user_clicks"] == cs["sequence"]:
            cs["results"][f"Level_{cs['level']}"] = 1
            cs["level"] += 1
            cs["attempt"] = 1
            cs["status"] = "idle"
            st.success("Benar! Lanjut level berikutnya.")
            st.rerun()
        else:
            if cs["attempt"] == 1:
                cs["attempt"] = 2
                cs["user_clicks"] = []
                st.warning("Salah. Coba sekali lagi.")
                st.rerun()
            else:
                cs["results"][f"Level_{cs['level']}"] = 0
                st.error("Salah dua kali. Tes selesai.")
                return True

    return False

# =========================================================
# MAIN
# =========================================================
def main():
    st.title("Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja")

    if st.session_state.get("thankyou"):
        st.success("Terima kasih. Data tersimpan.")
        return

    if not st.session_state.get("identity_completed"):
        render_identity_form()
        return

    if not st.session_state.get("questionnaire_done"):
        render_questionnaire()
        return

    finished = render_corsi()

    if finished:
        cs = st.session_state.corsi
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": sum(st.session_state.answers.values()),
            "corsi_max_level": max(
                [int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1],
                default=0
            )
        }
        payload.update(st.session_state.identity_data)
        payload.update(st.session_state.answers)

        if send_to_webhook(payload):
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error("Gagal mengirim data.")

if __name__ == "__main__":
    main()
