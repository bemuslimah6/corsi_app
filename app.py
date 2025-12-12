import streamlit as st
import random
import requests
import time
from datetime import datetime

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

st.set_page_config(page_title="Pengaruh Ketergatungan terhadap Internet pada Kinerja Memori Kerja", layout="centered")

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

def render_identity_form():

    st.header("Data Responden")

    st.write("""
    
    Terima kasih telah berpartisipasi dalam penelitian ini.  
    Aplikasi ini hanya digunakan untuk **kepentingan akademik**, dan seluruh data akan dijaga kerahasiaannya.  

    **Dengan melanjutkan pengisian, Anda menyetujui penggunaan data untuk tujuan penelitian.**
    """)

    st.subheader("Informasi Dasar")

    inisial = st.text_input("Inisial (wajib)")
    umur = st.number_input("Umur", min_value=17, max_value=28, step=1)
    gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"])
    pendidikan = st.selectbox("Pendidikan",
                              ["Pilih...", "SMA/SMK", "D3", "S1/Sederajat"])
    kota = st.text_input("Domisili (Kota/Kabupaten)")

    st.subheader("Kinerja Memori Kerja")

    durasi = st.selectbox("Durasi penggunaan layar per hari",
                          ["Pilih...", "< 1 jam", "1–2 jam", "2–4 jam", "4–6 jam", "> 6 jam"])

    aktivitas = st.selectbox("Aktivitas gawai yang paling sering dilakukan",
                             ["Pilih...", "Belajar", "Media sosial", "Game", "Menonton video", "Lainnya"])

    sebelum_tidur = st.radio("Menggunakan gawai sebelum tidur?", ["Ya", "Tidak"])

    kualitas_tidur = st.selectbox("Kualitas tidur",
                                  ["Pilih...", "Baik", "Sedang", "Buruk"])

    durasi_tidur = st.selectbox("Durasi tidur per hari",
                                ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])

    gangguan_fokus = st.selectbox(
        "Riwayat gangguan fokus atau kesulitan belajar",
        ["Pilih...", "Tidak ada", "ADHD", "Slow learner", "Gangguan bahasa", "Kesulitan pemrosesan pendengaran"]
    )

    riwayat_kesehatan = st.selectbox(
        "Riwayat kesehatan terkait kognitif",
        ["Pilih...", "Tidak ada", "Cedera kepala", "Riwayat kejang", "Menggunakan obat yang mempengaruhi fokus"]
    )

    kafein = st.selectbox(
        "Konsumsi kafein",
        ["Pilih...", "Tidak pernah", "1x sehari", "2x sehari", "3x atau lebih"]
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
                "umur": umur,
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
            st.experimental_rerun()

    return None

def render_questionnaire():
    st.header("Bagian 1 — Kuesioner 18 Item")

    answers = {}

    for i, q in enumerate(QUESTIONS, 1):
        answers[f"Q{i}"] = st.radio(q, [0, 1, 2, 3, 4, 5], horizontal=True, key=f"q{i}")

    return answers

def generate_grid(n):
    ids = list(range(1, n+1))
    random.shuffle(ids)
    return ids

def generate_sequence(level, n):
    length = min(level + 1, n)
    return random.sample(range(1, n+1), length)

def blink_sequence(blocks, sequence):
    st.info("Perhatikan blok yang berkedip...")
    for b in sequence:
        cols = st.columns(3)
        for i, blk in enumerate(blocks):
            with cols[i % 3]:
                color = "#2b6cb0" if blk == b else "#e2e8f0"
                text_color = "white" if blk == b else "#2d3748"
                st.markdown(
                    f"""
                    <div style='padding:20px;background:{color};color:{text_color};
                    margin:8px;border-radius:10px;text-align:center;font-size:28px;'>
                    {blk}</div>
                    """,
                    unsafe_allow_html=True
                )
        time.sleep(0.7)
        st.empty()

def render_corsi():
    st.header("🧠 Bagian 2 — Tes Corsi Tapping Multi-Level")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "n_blocks": random.randint(7, 12),
            "blocks": None,
            "sequence": None,
            "user_clicks": [],
            "results": {},
            "finished": False
        }

    cs = st.session_state.corsi

    if cs["blocks"] is None:
        cs["blocks"] = generate_grid(cs["n_blocks"])
        cs["sequence"] = generate_sequence(cs["level"], cs["n_blocks"])

    if "blink_done" not in cs:
        blink_sequence(cs["blocks"], cs["sequence"])
        cs["blink_done"] = True

    st.write(f"Level saat ini: {cs['level']}")
    st.write("Klik blok sesuai urutan yang berkedip tadi.")

    cols = st.columns(3)
    for i, blk in enumerate(cs["blocks"]):
        with cols[i % 3]:
            if st.button(str(blk), key=f"blk_{blk}_{cs['level']}"):
                cs["user_clicks"].append(blk)

    if len(cs["user_clicks"]) == len(cs["sequence"]):
        if cs["user_clicks"] == cs["sequence"]:
            st.success(f"Benar! Lanjut ke level {cs['level']+1}.")
            cs["results"][f"Level_{cs['level']}"] = 1
            cs["level"] += 1
            cs["blocks"] = generate_grid(cs["n_blocks"])
            cs["sequence"] = generate_sequence(cs["level"], cs["n_blocks"])
            cs["user_clicks"] = []
            del cs["blink_done"]
            st.experimental_rerun()
        else:
            st.error("Salah! Tes selesai.")
            cs["results"][f"Level_{cs['level']}"] = 0
            cs["finished"] = True
            return True

    return False

def main():

    st.title("Pengaruh Ketergantungan Internet terhadap Kinerja Memori Kerja")

    # Halaman terima kasih otomatis
    if "thankyou" in st.session_state and st.session_state.thankyou:
        st.success("Terima kasih! Data Anda telah berhasil direkam.")
        st.markdown("Formulir telah selesai. Anda dapat menutup halaman ini.")
        return

    if "identity_completed" not in st.session_state:
        st.session_state.identity_completed = False

    if not st.session_state.identity_completed:
        render_identity_form()
        return

    identity = st.session_state.identity_data

    answers = render_questionnaire()

    st.markdown("---")

    is_finished = render_corsi()

    if is_finished:
        cs = st.session_state.corsi
        max_level = max([int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1], default=0)

        st.subheader("Hasil Akhir Corsi")
        for k, v in cs["results"].items():
            st.write(f"{k}: {v}")
        st.write(f"**Level Tertinggi:** {max_level}")

        data = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "max_level": max_level
        }
        data.update(identity)
        data.update(answers)
        data.update(cs["results"])

        response = requests.post(WEBHOOK_URL, json=data)

        if response.status_code == 200:
            st.session_state.thankyou = True
            st.experimental_rerun()
        else:
            st.error("Gagal mengirim data. Periksa koneksi internet.")

if __name__ == "__main__":
    main()

