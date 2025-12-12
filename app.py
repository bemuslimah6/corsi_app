import streamlit as st
import random
import requests
import time
from datetime import datetime

# -------------------------------------------------------------
# KONFIGURASI HALAMAN
# -------------------------------------------------------------
st.set_page_config(
    page_title="Tes Memori Kerja",
    layout="centered",
    initial_sidebar_state="collapsed"
)

WEBHOOK_URL = "https://script.google.com/macros/s/AKfycbxfcOZUB5oUS74pQvoLFOsYD2SWfFwlHhgJkviawY1m56SVthIf1Qszxo4Zb3koCsEe/exec"

# -------------------------------------------------------------
# CSS CSS FIX (KHUSUS MOBILE AGAR TETAP KOTAK 4x4)
# -------------------------------------------------------------
st.markdown("""
<style>
    /* 1. Mencegah Padding Halaman terlalu lebar di HP */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* 2. Styling Tombol Corsi (Input User) */
    div[data-testid="stButton"] button {
        width: 100%;
        aspect-ratio: 1 / 1; /* Memaksa tombol jadi persegi */
        border-radius: 8px;
        border: 2px solid #CBD5E0;
        background-color: #E2E8F0;
        transition: all 0.1s;
        padding: 0 !important; /* Hilangkan padding teks agar muat di HP */
    }
    
    div[data-testid="stButton"] button:active {
        background-color: #2B6CB0 !important;
        transform: scale(0.95);
    }

    /* 3. MOBILE HACK: Memaksa kolom tetap 4 ke samping (tidak turun ke bawah) */
    /* Kita targetkan kolom di dalam grid */
    [data-testid="column"] {
        width: 25% !important;
        flex: 1 1 25% !important;
        min-width: 0 !important; /* Mencegah kolom pecah */
        padding: 0 2px !important; /* Jarak antar tombol diperkecil */
    }
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# DATA IAT (18 SOAL)
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
# FUNGSI BANTUAN
# -------------------------------------------------------------
def send_to_webhook(payload):
    try:
        r = requests.post(WEBHOOK_URL, json=payload, timeout=10)
        return r.status_code == 200, r.status_code
    except Exception as e:
        return False, str(e)

# -------------------------------------------------------------
# HALAMAN 1: IDENTITAS
# -------------------------------------------------------------
def render_identity_form():
    st.title("Studi Memori & Internet")
    st.info("Data Anda dijamin kerahasiaannya untuk keperluan akademik.")

    with st.form("identity_form"):
        # Layout Vertikal agar aman dari CSS Hack mobile
        inisial = st.text_input("Inisial Nama (Wajib)")
        umur = st.number_input("Umur", min_value=12, max_value=28, step=1)
        gender = st.radio("Jenis Kelamin", ["Laki-laki", "Perempuan"], horizontal=True)
        kota = st.text_input("Domisili (Kota/Kabupaten)")
        pendidikan = st.selectbox("Pendidikan Terakhir/Sedang Ditempuh", ["Pilih...", "SMP", "SMA/SMK", "D3", "S1", "S2/Lainnya"])
        
        st.markdown("---")
        st.write("**Kebiasaan Digital**")
        durasi = st.selectbox("Rata-rata penggunaan layar (HP/Laptop) per hari", 
                              ["Pilih...", "<1 jam", "1–2 jam", "2–4 jam", "4–6 jam", ">6 jam"])
        aktivitas = st.selectbox("Aktivitas paling sering dilakukan", 
                                 ["Pilih...", "Belajar/Kerja", "Media Sosial (TikTok/IG/dll)", "Game Online", "Streaming Video/Film", "Lainnya"])
        sebelum_tidur = st.radio("Apakah bermain HP sebelum tidur?", ["Ya", "Tidak"], horizontal=True)
        
        st.markdown("---")
        st.write("**Kondisi Kesehatan**")
        kualitas_tidur = st.selectbox("Bagaimana kualitas tidur Anda?", ["Pilih...", "Sangat Baik", "Cukup", "Buruk"])
        durasi_tidur = st.selectbox("Rata-rata durasi tidur malam", ["Pilih...", "< 5 jam", "5–6 jam", "6–8 jam", "> 8 jam"])
        gangguan_fokus = st.selectbox("Riwayat kesulitan fokus / belajar", 
                                      ["Pilih...", "Tidak ada", "ADHD/ADD", "Slow learner", "Lainnya"])
        kafein = st.selectbox("Konsumsi Kopi/Kafein hari ini?", ["Pilih...", "Tidak minum", "1 gelas", "2 gelas", "3 gelas atau lebih"])

        if st.form_submit_button("Lanjut ke Kuesioner", type="primary"):
            # Validasi sederhana
            if inisial.strip() == "" or kota.strip() == "" or pendidikan == "Pilih...":
                st.error("Mohon lengkapi Inisial, Domisili, dan Pendidikan.")
            else:
                st.session_state.identity_data = {
                    "inisial": inisial, "umur": int(umur), "jenis_kelamin": gender,
                    "pendidikan": pendidikan, "kota": kota, "durasi_layar": durasi,
                    "aktivitas_gawai": aktivitas, "sebelum_tidur": sebelum_tidur,
                    "kualitas_tidur": kualitas_tidur, "durasi_tidur": durasi_tidur,
                    "riwayat_gangguan_fokus": gangguan_fokus, "kafein": kafein
                }
                st.session_state.identity_completed = True
                st.rerun()

# -------------------------------------------------------------
# HALAMAN 2: KUESIONER
# -------------------------------------------------------------
def render_questionnaire():
    st.header("Bagian 1: Kuesioner")
    st.caption("Pilihlah skala 1 (Sangat Tidak Setuju) sampai 4 (Sangat Setuju).")

    answers = {}
    for i, q in enumerate(QUESTIONS, 1):
        st.write(f"**{i}. {q}**")
        # Menggunakan key unik untuk setiap radio button
        answers[f"Q{i}"] = st.radio(
            f"Jawaban no {i}", 
            [1, 2, 3, 4], 
            horizontal=True, 
            label_visibility="collapsed", 
            key=f"q_iat_{i}"
        )
        st.write("") # Spacer

    if st.button("Simpan & Lanjut ke Tes Memori", type="primary"):
        st.session_state.answers = answers
        st.session_state.questionnaire_done = True
        st.rerun()

# -------------------------------------------------------------
# FUNGSI VISUALISASI BLINK (RESPONSIF MOBILE)
# -------------------------------------------------------------
def blink_visual(sequence):
    placeholder = st.empty()
    
    # CSS Grid Layout untuk Visual Blink (Menggunakan fr unit agar responsif di HP)
    grid_style = """
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 5px;
    width: 100%;
    max-width: 350px;
    margin: 0 auto;
    aspect-ratio: 1/1;
    """
    
    # Fungsi helper untuk render kotak
    def render_grid(active_idx=None):
        html = f"<div style='{grid_style}'>"
        for i in range(1, 17):
            color = "#2B6CB0" if i == active_idx else "#E2E8F0"
            # Efek menyala
            style_extra = "box-shadow: 0 0 10px #3182CE; transform: scale(1.02);" if i == active_idx else ""
            
            html += f"""
            <div style="
                background-color: {color};
                border-radius: 6px;
                width: 100%;
                padding-top: 100%; /* Trick aspect ratio 1:1 murni CSS */
                position: relative;
                transition: background-color 0.1s;
                {style_extra}
            "></div>
            """
        html += "</div>"
        return html

    # 1. Tampilkan Grid Kosong
    with placeholder.container():
        st.markdown("<h4 style='text-align: center;'>Hafalkan Urutan!</h4>", unsafe_allow_html=True)
        st.markdown(render_grid(None), unsafe_allow_html=True)
    
    time.sleep(1.0) # Jeda persiapan

    # 2. Loop Animasi
    for target in sequence:
        # NYALA
        with placeholder.container():
            st.markdown("<h4 style='text-align: center;'>Hafalkan Urutan!</h4>", unsafe_allow_html=True)
            st.markdown(render_grid(target), unsafe_allow_html=True)
        time.sleep(0.7) # Durasi nyala
        
        # MATI SEJENAK (Penting untuk angka kembar)
        with placeholder.container():
            st.markdown("<h4 style='text-align: center;'>Hafalkan Urutan!</h4>", unsafe_allow_html=True)
            st.markdown(render_grid(None), unsafe_allow_html=True)
        time.sleep(0.2)

    # Biarkan placeholder terakhir (kosong) tetap ada agar tidak flicker saat transisi ke input

# -------------------------------------------------------------
# HALAMAN 3: LOGIKA UTAMA CORSI
# -------------------------------------------------------------
def render_corsi():
    st.header("Bagian 2: Tes Memori")

    if "corsi" not in st.session_state:
        st.session_state.corsi = {
            "level": 1,
            "sequence": [],
            "user_clicks": [],
            "attempt": 1,
            "results": {},
            "status": "init"
        }

    cs = st.session_state.corsi

    # --- PHASE 1: INITIALIZE SOAL ---
    if cs["status"] == "init":
        seq_len = cs["level"] + 1
        cs["sequence"] = random.sample(range(1, 17), min(seq_len, 16))
        cs["user_clicks"] = []
        cs["status"] = "ready"
        st.rerun()

    # --- PHASE 2: TOMBOL MULAI (PENTING AGAR TIDAK ERROR DI HP) ---
    if cs["status"] == "ready":
        st.info(f"Level {cs['level']} — Percobaan {cs['attempt']}")
        st.write("Tekan tombol di bawah untuk memulai urutan.")
        
        col_center = st.columns([1, 2, 1])
        with col_center[1]:
            if st.button(f"▶️ Mulai Level {cs['level']}", use_container_width=True, type="primary"):
                cs["status"] = "blink"
                st.rerun()

    # --- PHASE 3: ANIMASI ---
    if cs["status"] == "blink":
        blink_visual(cs["sequence"])
        cs["status"] = "input"
        st.rerun()

    # --- PHASE 4: INPUT USER ---
    if cs["status"] == "input":
        st.write(f"Level: **{cs['level']}** | Klik sesuai urutan tadi:")
        
        # CONTAINER GRID INPUT
        # Kita pakai container biasa, tapi CSS global di atas sudah memaksa kolom jadi 25% width
        with st.container():
            for row in range(4):
                cols = st.columns(4) # Ini akan dipaksa CSS menjadi sejajar di HP
                for col_idx in range(4):
                    block_id = (row * 4) + col_idx + 1
                    
                    # Key unik agar state tombol terjaga
                    btn_key = f"btn_{cs['level']}_{cs['attempt']}_{block_id}_{len(cs['user_clicks'])}"
                    
                    # Tombol kosong (hanya kotak)
                    if cols[col_idx].button(" ", key=btn_key):
                        cs["user_clicks"].append(block_id)
                        st.rerun()

        # LOGIKA PENILAIAN (REALTIME)
        if len(cs["user_clicks"]) == len(cs["sequence"]):
            if cs["user_clicks"] == cs["sequence"]:
                # BENAR
                st.success("✅ Benar!")
                time.sleep(0.5)
                cs["results"][f"Level_{cs['level']}"] = 1
                cs["level"] += 1
                cs["attempt"] = 1
                cs["status"] = "init"
                st.rerun()
            else:
                # SALAH
                if cs["attempt"] == 1:
                    st.warning("❌ Salah urutan. Coba sekali lagi.")
                    time.sleep(1.5)
                    cs["attempt"] = 2
                    cs["user_clicks"] = []
                    cs["status"] = "ready" # Kembali ke tombol start
                    st.rerun()
                else:
                    # GAME OVER
                    st.error("❌ Salah kedua kali. Tes Selesai.")
                    cs["results"][f"Level_{cs['level']}"] = 0
                    cs["status"] = "finished"
                    time.sleep(2)
                    return True # Return True = Selesai

    return False

# -------------------------------------------------------------
# MAIN APP FLOW
# -------------------------------------------------------------
def main():
    # SCREEN 4: TERIMA KASIH
    if st.session_state.get("thankyou", False):
        st.balloons()
        st.success("Terima kasih! Data berhasil disimpan.")
        st.write("Anda dapat menutup halaman ini.")
        if st.button("Kembali ke Awal (Reset)"):
            st.session_state.clear()
            st.rerun()
        return

    # SCREEN 1: IDENTITAS
    if not st.session_state.get("identity_completed", False):
        render_identity_form()
        return

    # SCREEN 2: KUESIONER
    if not st.session_state.get("questionnaire_done", False):
        render_questionnaire()
        return

    # SCREEN 3: CORSI TEST
    finished = render_corsi()

    # SCREEN 4: SUBMIT DATA
    if finished:
        cs = st.session_state.corsi
        
        # Hitung skor
        passed_levels = [int(k.split("_")[1]) for k, v in cs["results"].items() if v == 1]
        max_level = max(passed_levels) if passed_levels else 0
        total_iat = sum(st.session_state.answers.values())
        
        # Siapkan Payload JSON
        payload = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "total_iat": total_iat,
            "corsi_max_level": max_level,
            "raw_results": str(cs["results"])
        }
        payload.update(st.session_state.identity_data)
        payload.update(st.session_state.answers)

        with st.spinner("Sedang mengirim data..."):
            ok, info = send_to_webhook(payload)

        if ok:
            st.session_state.thankyou = True
            st.rerun()
        else:
            st.error(f"Gagal koneksi server: {info}. Mohon screenshot hasil ini.")
            st.json(payload) # Tampilkan data jika error agar bisa dicatat manual

if __name__ == "__main__":
    main()
