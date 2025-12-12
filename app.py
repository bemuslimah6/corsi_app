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

# ---------------- HELPERS ----------------
def send_to_webhook(payload):
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, str(e)

# ---------------- IDENTITY FORM ----------------
def render_identity_form():

    st.header("Data Responden")

    st.write("""
    Terima kasih telah berpartisipasi dalam penelitian ini.  
    Aplikasi ini digunakan untuk **kepentingan akademik**, dan seluruh data dijaga kerahasiaannya.

    **Dengan melanjutkan, Anda menyetujui penggunaan data untuk penelitian.**
    """)

    st.subheader("Informasi Dasar")

    inisial = st.text_input("Inisial (wajib)")
    umur = st.number_input("Umur", min_value=17, max_value=28, step=1)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
    kota = st.text_input("Domisili (Kota/Kabupaten)")

    st.subheader("Kinerja Memori Kerja")

    durasi = st.selectbox("Durasi penggunaan layar per hari",
                          ["Pilih...", "< 1 jam", "1–2 jam", "2–4 jam", "4–6 jam", "> 6 jam"])

    aktivitas = st.selectbox("Aktivitas gawai yang paling sering dilakukan",
                             ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])

    sebelum_tidur = st.radio("Menggunakan gawai sebelum tidur?", ["Ya", "Tidak"])

    kualitas_tidur = st.selectbox("Kualitas tidur", ["Pilih...", "Baik", "Sedang", "Buruk"])

    durasi_tidur = st.selectbox("Durasi tidur per hari", ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])

    gangguan_fokus = st.selectbox("Riwayat gangguan fokus / kesulitan belajar",
                                  ["Pilih...", "Tidak ada", "ADHD", "Slow learner", "Gangguan bahasa", "Kesulitan pemrosesan pendengaran"])

    riwayat_kesehatan = st.selectbox("Riwayat kesehatan kognitif",
                                     ["Pilih...", "Tidak ada", "Cedera kepala", "Riwayat kejang", "Menggunakan obat yang mempengaruhi fokus"])

    kafein = st.selectbox("Konsumsi kafein",
                          ["Pilih...", "Tidak pernah", "1x sehari", "2x sehari", "3x atau lebih"])

    if st.button("Lanjut ke Kuesioner"):

        # VALIDASI
        if inisial.strip() == "":
            st.error("Inisial wajib diisi.")
        elif pendidikan == "Pilih...":
            st.error("Pendidikan wajib dipilih.")
        elif kota.strip() == "":
            st.error("Kota wajib diisi.")
        elif durasi == "Pilih...":
            st.error("Durasi layar wajib dipilih.")
        elif aktivitas == "Pilih...":
            st.error("Aktivitas gawai wajib dipilih.")
        elif kualitas_tidur == "Pilih...":
            st.error("Kualitas tidur wajib dipilih.")
        elif durasi_tidur == "Pilih...":
            st.error("Durasi tidur wajib dipilih.")
        elif gangguan_fokus == "Pilih...":
            st.error("Riwayat gangguan fokus wajib dipilih.")
        elif riwayat_kesehatan == "Pilih...":
            st.error("Riwayat kesehatan wajib dipilih.")
        elif kafein == "Pilih...":
            st.error("Kafein wajib dipilih.")
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
            f"**{i}. {q}**",
            [1, 2, 3, 4],
            key=f"q{i}",
            horizontal=True
        )

    if st.button("Selesai → Lanjut Tes Corsi"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()

# ---------------- CORSI 4x4 WITH 1-MISTAKE RULE ----------------
def generate_positions_4x4():
    pos = list(range(1, 17))
    random.shuffle(pos)
    return pos

def generate_sequence(level):
    return random.sample(range(1, 17), level + 1)

def blink(sequence, positions):
    placeholder = st.empty()
    for pid in sequence:
        with placeholder.container():
            html = "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;'>"
            for b in positions:
                if b == pid:
                    html += "<div style='height:70px;background:#2B6CB0;border-radius:10px;'></div>"
                else:
                    html += "<div style='height:70px;background:#E2E8F0;border-radius:10px;'></div>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)
        time.sleep(0.6)
        placeholder.empty()
    time.sleep(0.2)

def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi 4×4")

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

    # Initialize level
    if cs["positions"] is None:
        cs["positions"] = generate_positions_4x4()
        cs["sequence"] = generate_sequence(cs["level"])
        cs["user_clicks"] = []
        cs["status"] = "idle"

    # Idle state
    if cs["status"] == "idle":
        st.info(f"Level {cs['level']} — Panjang urutan: {len(cs['sequence'])}")
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

    # Input mode
    if cs["status"] == "input":
        st.write("Klik kotak sesuai urutan blink tadi.")

        cols = st.columns(4)
        for idx, pos in enumerate(cs["positions"]):
            col = cols[idx % 4]

            is_selected = pos in cs["user_clicks"]
            color = "#38A169" if is_selected else "#E2E8F0"

            if col.button(" ", key=f"blk_{pos}_{len(cs['user_clicks'])}"):
                if pos not in cs["user_clicks"]:
                    cs["user_clicks"].append(pos)
                st.rerun()

        st.write(f"Klik: {len(cs['user_clicks'])}/{len(cs['sequence'])}")

    # Evaluate
    if len(cs["user_clicks"]) == len(cs["sequence"]):

        if cs["user_clicks"] == cs["sequence"]:
            # SUCCESS
            cs["results"][f"Level_{cs['level']}"] = 1
            cs["level"] += 1
            cs["positions"] = None
            cs["attempt"] = 1
            st.success("Benar! Naik ke level berikutnya.")
            st.rerun()
            return False

        else:
            # WRONG
            if cs["attempt"] == 1:
                cs["attempt"] = 2
                cs["user_clicks"] = []
                st.warning("Salah. Kesempatan 1x lagi pada level yang sama.")
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
        st.success("Terima kasih! Data Anda telah direkam.")
        return

    # IDENTITAS
    if not st.session_state.get("identity_completed", False):
        render_identity_form()
        return

    # KUESIONER
    if not st.session_state.get("questionnaire_done", False):
        render_questionnaire()
        return

    # CORSI
    is_finished = render_corsi()

    # SUBMIT
    if is_finished:
        cs = st.session_state.corsi

        max_level = max([int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1], default=0)
        total_iat = sum(st.session_state.answers.values())
        total_corsi_benar = sum(1 for v in cs["results"].values() if v == 1)
        total_corsi_salah = sum(1 for v in cs["results"].values() if v == 0)

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": total_iat,
            "corsi_max_level": max_level,
            "corsi_total_benar": total_corsi_benar,
            "corsi_total_salah": total_corsi_salah,
        }

        payload.update(st.session_state.identity_data)
        payload.update(st.session_state.answers)
        payload.update(cs["results"])

        ok, info = send_to_webhook(payload)
        if ok:
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error(f"Gagal mengirim data: {info}")

if __name__ == "__main__":
    main()

