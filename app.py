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
    "1. Saya bermain internet lebih lama dari yang saya rencanakan.",
    "2. Saya membentuk pertemanan baru melalui internet.",
    "3. Saya merahasiakan aktivitas saya di internet dari orang lain.",
    "4. Saya menutupi pikiran yang mengganggu dengan memikirkan hal menyenangkan tentang internet.",
    "5. Saya takut hidup tanpa internet akan membosankan atau kosong.",
    "6. Saya marah jika ada yang mengganggu saat saya bermain internet.",
    "7. Saya terus memikirkan internet ketika tidak sedang bermain.",
    "8. Saya lebih memilih internet daripada beraktivitas dengan orang lain.",
    "9. Saya merasa gelisah jika tidak bermain internet, dan tenang kembali setelah bermain.",
    "10. Saya mengabaikan pekerjaan rumah demi bermain internet.",
    "11. Waktu belajar atau nilai akademik saya menurun akibat internet.",
    "12. Kinerja saya di sekolah/rumah terganggu karena internet.",
    "13. Saya sering kurang tidur karena bermain internet.",
    "14. Saya berusaha mengurangi waktu internet tetapi gagal.",
    "15. Saya sering berkata 'sebentar lagi' saat bermain internet.",
    "16. Saya berusaha menyembunyikan durasi bermain internet.",
    "17. Saya mengabaikan kegiatan penting demi internet.",
    "18. Saya merasa sulit berhenti ketika sedang bermain internet."
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
    Aplikasi ini hanya digunakan untuk **kepentingan akademik**, dan seluruh data akan dijaga kerahasiaannya.  
    """)

    inisial = st.text_input("Inisial (wajib)", key="idf_inisial")
    umur = st.number_input("Umur", min_value=17, max_value=80, step=1)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan", ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
    kota = st.text_input("Domisili (Kota/Kabupaten)")

    durasi = st.selectbox("Durasi penggunaan layar per hari",
                          ["Pilih...", "< 1 jam", "1–2 jam", "2–4 jam", "4–6 jam", "> 6 jam"])

    aktivitas = st.selectbox("Aktivitas gawai yang paling sering dilakukan",
                             ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])

    sebelum_tidur = st.radio("Menggunakan gawai sebelum tidur?", ["Ya", "Tidak"])
    kualitas_tidur = st.selectbox("Kualitas tidur", ["Pilih...", "Baik", "Sedang", "Buruk"])
    durasi_tidur = st.selectbox("Durasi tidur", ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])

    gangguan_fokus = st.selectbox("Riwayat gangguan fokus",
                                  ["Pilih...", "Tidak ada", "ADHD", "Slow learner",
                                   "Gangguan bahasa", "Kesulitan pemrosesan pendengaran"])

    riwayat_kesehatan = st.selectbox("Riwayat kesehatan kognitif",
                                     ["Pilih...", "Tidak ada", "Cedera kepala",
                                      "Riwayat kejang", "Obat tertentu"])

    kafein = st.selectbox("Konsumsi kafein", ["Pilih...", "Tidak pernah", "1x sehari", "2x sehari", "3x+"])

    if st.button("Lanjut ke Kuesioner"):
        if "" in [inisial.strip(), kota.strip()] or \
           "Pilih..." in [pendidikan, durasi, aktivitas, kualitas_tidur,
                          durasi_tidur, gangguan_fokus, riwayat_kesehatan, kafein]:
            st.error("Semua data wajib diisi.")
        else:
            st.session_state.identity_completed = True
            st.session_state.identity_data = {
                "inisial": inisial,
                "umur":umur,
                "jenis_kelamin":gender,
                "pendidikan":pendidikan,
                "kota":kota,
                "durasi_layar":durasi,
                "aktivitas_gawai":aktivitas,
                "sebelum_tidur":sebelum_tidur,
                "kualitas_tidur":kualitas_tidur,
                "durasi_tidur":durasi_tidur,
                "gangguan_fokus":gangguan_fokus,
                "riwayat_kesehatan":riwayat_kesehatan,
                "kafein":kafein
            }
            st.rerun()


# ---------------- QUESTIONNAIRE ----------------
def render_questionnaire():
    st.header("Bagian 1 — Kuesioner IAT")
st.write("""
    Mohon isi sesuai dengan kondisi Anda, 1 = Sangat Tidak Setuju , 2 = Tidak Setuju , 3 = Setuju , 4 = Sangat Setuju  
    """)
    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        answers[f"Q{i}"] = st.radio(q, [1,2,3,4], key=f"q{i}", horizontal=True)

    if st.button("Selesai → Lanjut Tes Corsi"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()


# ---------------- CORSI (fixed per request) ----------------
def generate_positions():
    pos = list(range(1,17))
    random.shuffle(pos)
    return pos

def generate_sequence(level):
    length = min(level + 1, 16)
    return random.sample(range(1,17), length)

def blink_visual(seq, pos):
    ph = st.empty()
    for target in seq:
        html = "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:6px;'>"
        for p in pos:
            if p == target:
                html += "<div style='height:70px;background:#2b6cb0;border-radius:10px;'></div>"
            else:
                html += "<div style='height:70px;background:#e2e8f0;border-radius:10px;'></div>"
        html += "</div>"
        ph.markdown(html, unsafe_allow_html=True)
        time.sleep(0.6)
        ph.empty()
        time.sleep(0.2)

def render_corsi():
    st.header("Bagian 2 — Tes Corsi 4×4")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "positions": None,
            "sequence": None,
            "user": [],
            "attempt": 1,
            "results": {},
            "status": "idle"
        }

    cs = st.session_state.corsi

    # siapkan level
    if cs["positions"] is None:
        cs["positions"] = generate_positions()
        cs["sequence"] = generate_sequence(cs["level"])
        cs["user"] = []
        cs["status"] = "show"

    # BLINK
    if cs["status"] == "show":
        blink_visual(cs["sequence"], cs["positions"])
        cs["status"] = "input"
        st.rerun()
        return

    # INPUT
    if cs["status"] == "input":
        st.info(f"Level {cs['level']} — Klik urutannya")

        cols = st.columns(4)

        for idx, pid in enumerate(cs["positions"]):
            col = cols[idx % 4]

            clicked = pid in cs["user"]
            color = "#38a169" if clicked else "#e2e8f0"

            if col.button(" ", key=f"p{pid}_{cs['level']}", help="Klik kotak",
                          use_container_width=True):
                cs["user"].append(pid)
                st.rerun()

        # Jika jumlah klik sudah sama
        if len(cs["user"]) == len(cs["sequence"]):

            # BENAR
            if cs["user"] == cs["sequence"]:
                cs["results"][f"Level_{cs['level']}"] = 1
                cs["level"] += 1
                cs["attempt"] = 1
                cs["positions"] = None
                st.success("Benar! Lanjut level berikutnya")
                st.rerun()

            else:
                # SALAH PERTAMA KALI
                if cs["attempt"] == 1:
                    cs["attempt"] = 2
                    cs["user"] = []
                    cs["status"] = "show"
                    st.warning("Salah! Anda dapat 1 kesempatan lagi pada level ini.")
                    st.rerun()

                # SALAH KEDUA → STOP
                else:
                    cs["results"][f"Level_{cs['level']}"] = 0
                    cs["status"] = "finished"
                    st.error("Salah dua kali. Tes selesai.")
                    return True

    return False


# ---------------- MAIN ----------------
def main():

    st.title("Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja")

    # TERIMAKASIH
    if st.session_state.get("thankyou", False):
        st.success("Terima kasih! Data berhasil direkam.")
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
    finished = render_corsi()

    # Jika selesai → kirim data
    if finished:
        cs = st.session_state.corsi
        max_level = max(
            [int(k.split("_")[1]) for k,v in cs["results"].items() if v==1],
            default=0
        )

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "max_level": max_level
        }

        payload.update(st.session_state.identity_data)
        payload.update(st.session_state.answers)
        payload.update(cs["results"])

        ok, info = send_to_webhook(payload)

        if ok:
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error("Gagal mengirim data.")


if __name__ == "__main__":
    main()

