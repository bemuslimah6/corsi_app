# =============================
# PAGE 3 – TES CORSI
# =============================
elif st.session_state.page == "corsi":
    st.title("Tes Corsi Block Tapping")

    GRID_SIZE = 4

    def new_sequence(level):
        return random.sample(range(GRID_SIZE * GRID_SIZE), level)

    if st.session_state.show_seq:
        st.session_state.sequence = new_sequence(st.session_state.corsi_level)
        st.session_state.user_input = []
        st.info(f"Level {st.session_state.corsi_level} – Perhatikan urutan kotak")

        for i in range(GRID_SIZE * GRID_SIZE):
            st.session_state[f"blink_{i}"] = False

        time.sleep(0.8)
        for idx in st.session_state.sequence:
            st.session_state[f"blink_{idx}"] = True
            st.rerun()
            time.sleep(0.6)
            st.session_state[f"blink_{idx}"] = False
            st.rerun()
            time.sleep(0.25)

        st.session_state.show_seq = False
        st.rerun()
