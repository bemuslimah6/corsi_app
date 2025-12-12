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
    Aplikasi ini hanya digunakan untuk **kepentingan akademik**, dan seluruh data akan dijaga kerahasiaannya.  

    **Dengan melanjutkan pengisian, Anda menyetujui penggunaan data untuk tujuan penelitian.**
    """)

    st.subheader("Informasi Dasar")

    inisial = st.text_input("Inisial (wajib)", key="idf_inisial")
    umur = st.number_input("Umur", min_value=17, max_value=80, step=1, key="idf_umur")
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], key="idf_gender")
    pendidikan = st.selectbox("Pendidikan",
                              ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"], key="idf_pendidikan")
    kota = st.text_input("Domisili (Kota/Kabupaten)", key="idf_kota")

    st.subheader("Kinerja Memori Kerja")

    durasi = st.selectbox("Durasi penggunaan layar per hari",
                          ["Pilih...", "< 1 jam", "1–2 jam", "2–4 jam", "4–6 jam", "> 6 jam"], key="idf_durasi")

    aktivitas = st.selectbox("Aktivitas gawai yang paling sering dilakukan",
                             ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"], key="idf_aktivitas")

    sebelum_tidur = st.radio("Menggunakan gawai sebelum tidur?", ["Ya", "Tidak"], key="idf_sebelum")

    kualitas_tidur = st.selectbox("Kualitas tidur",
                                  ["Pilih...", "Baik", "Sedang", "Buruk"], key="idf_kualitas")

    durasi_tidur = st.selectbox("Durasi tidur per hari",
                                ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"], key="idf_durasitidur")

    gangguan_fokus = st.selectbox(
        "Riwayat gangguan fokus atau kesulitan belajar",
        ["Pilih...", "Tidak ada", "ADHD", "Slow learner", "Gangguan bahasa", "Kesulitan pemrosesan pendengaran"],
        key="idf_gangguan"
    )

    riwayat_kesehatan = st.selectbox(
        "Riwayat kesehatan terkait kognitif",
        ["Pilih...", "Tidak ada", "Cedera kepala", "Riwayat kejang", "Menggunakan obat yang mempengaruhi fokus"],
        key="idf_riwayat"
    )

    kafein = st.selectbox(
        "Konsumsi kafein",
        ["Pilih...", "Tidak pernah", "1x sehari", "2x sehari", "3x atau lebih"],
        key="idf_kafein"
    )

    # VALIDASI SEMUA DATA
    if st.button("Lanjut ke Kuesioner"):
        if inisial.strip() == "":
            st.error("Inisial wajib diisi.")
        elif pendidikan == "Pilih...":
            st.error("Pendidikan wajib dipilih.")
        elif kota.strip() == "":
            st.error("Kota/Kabupaten wajib diisi.")
        elif durasi == "Pilih...":
            st.error("Durasi penggunaan layar wajib dipilih.")
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
            st.error("Konsumsi kafein wajib dipilih.")
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

    return None

# ---------------- QUESTIONNAIRE ----------------
def render_questionnaire():
    st.header("Bagian 1 — Kuesioner 18 Item (Likert 0–5)")
    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        # default selection: 0 (Tidak Pernah) to ensure selection exists
        answers[f"Q{i}"] = st.radio(f"{i}. {q}", [0, 1, 2, 3, 4, 5], index=0, horizontal=True, key=f"q{i}")
    if st.button("Selesai Kuesioner — Siap ke Tes Corsi"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()
    return answers

# ---------------- CORSI 4x4 (no numbers) ----------------
def generate_positions_4x4():
    # return shuffled positions (ids 1..16) to randomize visual arrangement per level
    positions = list(range(1, 17))
    random.shuffle(positions)
    return positions

def generate_sequence(level, n_blocks):
    length = min(level + 1, n_blocks)
    return random.sample(range(1, n_blocks+1), length)

def blink_visual(sequence, positions):
    # show simple visual blink using HTML grid; highlighted boxes use blue, others grey
    placeholder = st.empty()
    for hid in sequence:
        with placeholder.container():
            grid_html = "<div style='display:grid;grid-template-columns:repeat(4,1fr);gap:8px;'>"
            for pid in positions:
                if pid == hid:
                    grid_html += "<div style='height:64px;background:#2b6cb0;border-radius:8px;'></div>"
                else:
                    grid_html += "<div style='height:64px;background:#e2e8f0;border-radius:8px;'></div>"
            grid_html += "</div>"
            st.markdown(grid_html, unsafe_allow_html=True)
        time.sleep(0.7)
        placeholder.empty()
    # small pause
    time.sleep(0.2)

def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi (4×4 grid, kotak kosong)")

    # initialize corsi state (16 blocks)
    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "n_blocks": 16,
            "positions": None,     # visual arrangement (shuffled ids)
            "sequence": None,      # sequence of ids (1..16)
            "user_clicks": [],
            "results": {},
            "status": "idle",      # idle, showing, input, finished
        }

    cs = st.session_state.corsi

    # prepare positions & sequence when starting a level
    if cs["positions"] is None:
        cs["positions"] = generate_positions_4x4()
        cs["sequence"] = generate_sequence(cs["level"], cs["n_blocks"])
        cs["user_clicks"] = []
        cs["status"] = "idle"

    # idle: show level info and button to show sequence
    if cs["status"] == "idle":
        st.info(f"Level saat ini: {cs['level']} — Panjang urutan: {len(cs['sequence'])}")
        if st.button("Tampilkan urutan (blink)"):
            cs["status"] = "showing"
            st.rerun()
        return False

    # showing: blink visual then switch to input
    if cs["status"] == "showing":
        blink_visual(cs["sequence"], cs["positions"])
        cs["status"] = "input"
        st.rerun()
        return False

    # input mode: show 4x4 clickable empty boxes
    if cs["status"] == "input":
        st.write("Klik kotak sesuai urutan yang berkedip tadi.")
        # show grid of buttons (blank)
        cols = st.columns(4)
        for idx, pid in enumerate(cs["positions"]):
            col = cols[idx % 4]
            # use an empty label but give tooltip
            if col.button("", key=f"blk_{pid}_{cs['level']}", help="Klik kotak ini"):
                cs["user_clicks"].append(pid)
                st.rerun()
        st.write(f"Klik: {len(cs['user_clicks'])} / {len(cs['sequence'])}")

    # evaluate automatically when number of clicks equals sequence length
    if cs["status"] == "input" and len(cs["user_clicks"]) == len(cs["sequence"]):
        if cs["user_clicks"] == cs["sequence"]:
            cs["results"][f"Level_{cs['level']}"] = 1
            cs["level"] += 1
            # prepare next level (positions reshuffled)
            cs["positions"] = None
            cs["sequence"] = None
            cs["user_clicks"] = []
            cs["status"] = "idle"
            st.success("Benar! Melanjutkan ke level berikutnya...")
            st.rerun()
            return False
        else:
            cs["results"][f"Level_{cs['level']}"] = 0
            cs["status"] = "finished"
            st.error("Salah — Tes Berhenti.")
            return True

    return False

# ---------------- MAIN ----------------
def main():

    st.title("Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja")

    # if already done & sent, show thank you page
    if st.session_state.get("thankyou", False):
        st.success("Terima kasih! Data Anda telah berhasil direkam.")
        st.markdown("Formulir telah selesai. Anda dapat menutup halaman ini.")
        return

    # identity step
    if "identity_completed" not in st.session_state:
        st.session_state.identity_completed = False

    if not st.session_state.identity_completed:
        render_identity_form()
        return

    # questionnaire step
    if "questionnaire_done" not in st.session_state:
        st.session_state.questionnaire_done = False

    if not st.session_state.questionnaire_done:
        # render questionnaire — will set session_state.answers and questionnaire_done when user presses button
        render_questionnaire()
        return

    # after questionnaire, show a button to start Corsi (so corsi won't show while answering)
    if "start_corsi" not in st.session_state:
        st.session_state.start_corsi = False

    if not st.session_state.start_corsi:
        if st.button("Mulai Tes Corsi Sekarang"):
            st.session_state.start_corsi = True
            # ensure corsi state is reset
            if "corsi" in st.session_state:
                del st.session_state.corsi
            st.rerun()
        else:
            st.info("Tekan 'Mulai Tes Corsi Sekarang' jika sudah siap melanjutkan ke tes.")
        return

    # show corsi component
    is_finished = render_corsi()

    # if corsi finished (wrong answer) -> assemble data and auto-send then thank you
    if is_finished:
        cs = st.session_state.corsi
        max_level = 0
        for k, v in cs.get("results", {}).items():
            if v == 1:
                try:
                    lvl = int(k.split("_")[1])
                    if lvl > max_level:
                        max_level = lvl
                except:
                    pass

        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "max_level": max_level
        }
        # identity
        payload.update(st.session_state.identity_data if "identity_data" in st.session_state else {})
        # questionnaire answers
        payload.update(st.session_state.answers if "answers" in st.session_state else {})
        # corsi results
        payload.update(cs.get("results", {}))

        ok, info = send_to_webhook(payload)
        if ok:
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error(f"Gagal mengirim data: {info}. Simpan hasil dan coba lagi jika koneksi tersedia.")

if __name__ == "__main__":
    main()
