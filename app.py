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

    st.write("""
    Terima kasih telah berpartisipasi dalam penelitian ini.  
    Data Anda bersifat **rahasia** dan hanya digunakan untuk **kepentingan akademik**.
    """)

    inisial = st.text_input("Inisial (wajib)")
    umur = st.number_input("Umur", min_value=17, max_value=80, step=1)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
    kota = st.text_input("Domisili (Kota/Kabupaten)")

    durasi = st.selectbox("Durasi penggunaan layar per hari",
                          ["Pilih...", "<1 jam", "1–2 jam", "2–4 jam", "4–6 jam", ">6 jam"])

    aktivitas = st.selectbox("Aktivitas gawai utama",
                             ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])

    sebelum_tidur = st.radio("Menggunakan gawai sebelum tidur?", ["Ya", "Tidak"])

    kualitas_tidur = st.selectbox("Kualitas tidur", ["Pilih...", "Baik", "Sedang", "Buruk"])

    durasi_tidur = st.selectbox("Durasi tidur", ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])

    gangguan_fokus = st.selectbox("Riwayat gangguan fokus / kesulitan belajar",
                                  ["Pilih...", "Tidak ada", "ADHD", "Slow learner",
                                   "Gangguan bahasa", "Kesulitan pendengaran"])

    riwayat_kognitif = st.selectbox("Riwayat kesehatan terkait kognitif",
                                    ["Pilih...", "Tidak ada", "Cedera kepala",
                                     "Riwayat kejang", "Obat yang mempengaruhi fokus"])

    kafein = st.selectbox("Konsumsi kafein",
                          ["Pilih...", "Tidak pernah", "1x", "2x", "3x atau lebih"])

    if st.button("Lanjut ke Kuesioner"):
        required = [
            inisial.strip(),
            kota.strip(),
            pendidikan != "Pilih...",
            durasi != "Pilih...",
            aktivitas != "Pilih...",
            kualitas_tidur != "Pilih...",
            durasi_tidur != "Pilih...",
            gangguan_fokus != "Pilih...",
            riwayat_kognitif != "Pilih...",
            kafein != "Pilih...",
        ]

        if not all(required):
            st.error("Semua field wajib diisi.")
            return

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
            "riwayat_kognitif": riwayat_kognitif,
            "kafein": kafein
        }

        st.rerun()


# -------------------------------------------------------------
# KUESIONER IAT
# -------------------------------------------------------------
def render_questionnaire():

    st.header("Bagian 1 — Kuesioner Internet Addiction Test")

    st.write("""
    **Petunjuk:**  
    Jawab sesuai kondisi Anda  
    - 1 = Sangat Tidak Setuju  
    - 2 = Tidak Setuju  
    - 3 = Setuju  
    - 4 = Sangat Setuju  
    """)

    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        answers[f"Q{i}"] = st.radio(f"**{i}. {q}**", [1,2,3,4],
                                   horizontal=True, key=f"q{i}")

    if st.button("Selesai → Mulai Tes Corsi"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()


# -------------------------------------------------------------
# BLINK VISUAL
# -------------------------------------------------------------
def blink_visual(sequence, positions):
    ph = st.empty()

    for target in sequence:
        with ph.container():
            html = "<div style='display:grid;grid-template-columns:repeat(4,70px);gap:10px;justify-content:center;'>"
            for p in positions:
                if p == target:
                    html += "<div style='width:70px;height:70px;background:#2B6CB0;border-radius:10px;'></div>"
                else:
                    html += "<div style='width:70px;height:70px;background:#E2E8F0;border-radius:10px;'></div>"
            html += "</div>"
            st.markdown(html, unsafe_allow_html=True)

        time.sleep(0.55)
        ph.empty()

    time.sleep(0.2)


# -------------------------------------------------------------
# TES CORSI (STABIL)
# -------------------------------------------------------------
def render_corsi():
    st.header("Bagian 2 — Tes Corsi (4×4)")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "positions": None,
            "sequence": None,
            "user_clicks": [],
            "attempt": 1,
            "results": {},
            "status": "idle",
            "last_clicked": None
        }

    cs = st.session_state.corsi

    # INIT
    if cs["positions"] is None:
        cs["positions"] = list(range(1,17))
        random.shuffle(cs["positions"])
        cs["sequence"] = random.sample(range(1,17), min(cs["level"]+1,16))
        cs["user_clicks"] = []
        cs["status"] = "idle"

    # IDLE → BLINK
    if cs["status"] == "idle":
        cs["status"] = "blink"
        st.rerun()

    # BLINK
    if cs["status"] == "blink":
        blink_visual(cs["sequence"], cs["positions"])
        cs["status"] = "input"
        st.stop()     # <- memastikan blink tampil

    # INPUT MODE
    if cs["status"] == "input":

        clicked = st.session_state.get("last_clicked", None)

        if clicked is not None:
            if clicked not in cs["user_clicks"]:
                cs["user_clicks"].append(clicked)
            st.session_state.last_clicked = None
            st.rerun()

        st.write(f"Klik kotak: **{len(cs['user_clicks'])}/{len(cs['sequence'])}**")

        # CSS GRID
        st.markdown("""
        <style>
        .box {width:70px;height:70px;border-radius:10px;background:#E2E8F0;margin:5px;}
        .box-selected {width:70px;height:70px;border-radius:10px;background:#38A169;margin:5px;}
        .wrap {display:flex;flex-wrap:wrap;width:320px;margin:auto;justify-content:center;}
        </style>
        """, unsafe_allow_html=True)

        html = "<div class='wrap'>"

        for pid in cs["positions"]:
            if pid in cs["user_clicks"]:
                html += "<div class='box-selected'></div>"
            else:
                html += (
                    f"<form>"
                    f"<button name='click' value='{pid}' "
                    f"style='width:70px;height:70px;border:none;border-radius:10px;"
                    f"background:#E2E8F0;margin:5px;'></button>"
                    f"</form>"
                )
        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)

        # listen click
        params = st.experimental_get_query_params()
        if "click" in params:
            st.session_state.last_clicked = int(params["click"][0])
            st.experimental_set_query_params()
            st.rerun()

    # EVALUATE
    if len(cs["user_clicks"]) == len(cs["sequence"]):

        if cs["user_clicks"] == cs["sequence"]:
            cs["results"][f"Level_{cs['level']}"] = 1
            cs["level"] += 1
            cs["attempt"] = 1
            cs["positions"] = None
            st.success("Benar! Ke level berikutnya.")
            st.rerun()

        else:
            if cs["attempt"] == 1:
                cs["attempt"] = 2
                cs["user_clicks"] = []
                cs["status"] = "blink"
                st.warning("Salah. Kesempatan 1x lagi.")
                st.rerun()
            else:
                cs["results"][f"Level_{cs['level']}"] = 0
                cs["status"] = "finished"
                st.error("Salah dua kali. Tes selesai.")
                return True

    return False


# -------------------------------------------------------------
# MAIN APP
# -------------------------------------------------------------
def main():

    st.title("Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja")

    # Jika sudah submit → halaman terima kasih
    if st.session_state.get("thankyou", False):
        st.success("Terima kasih! Data Anda berhasil direkam.")
        st.write("Anda dapat menutup halaman ini.")
        return

    # Step 1
    if not st.session_state.get("identity_completed", False):
        render_identity_form()
        return

    # Step 2
    if not st.session_state.get("questionnaire_done", False):
        render_questionnaire()
        return

    # Step 3
    finished = render_corsi()

    if finished:

        cs = st.session_state.corsi

        max_level = max(
            [int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1],
            default=0
        )

        total_iat = sum(st.session_state.answers.values())
        total_benar = sum(1 for v in cs["results"].values() if v == 1)
        total_salah = sum(1 for v in cs["results"].values() if v == 0)

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": total_iat,
            "corsi_max_level": max_level,
            "corsi_total_benar": total_benar,
            "corsi_total_salah": total_salah
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
