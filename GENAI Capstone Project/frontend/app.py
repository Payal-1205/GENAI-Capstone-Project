import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Healthcare MediAssist AI",
    page_icon="🏥",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Custom CSS
# -----------------------------

st.markdown("""
<style>

.main-title{
    text-align:center;
    font-size:35px;
    font-weight:bold;
    color:#1E88E5;
}

.user-msg{
    background-color:#DCF8C6;
    padding:12px;
    border-radius:10px;
    margin-bottom:5px;
}

.bot-msg{
    background-color:#F1F1F1;
    padding:12px;
    border-radius:10px;
    margin-bottom:15px;
}

.source{
    color:green;
    font-weight:bold;
}

.score{
    color:#ff5722;
    font-weight:bold;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Page Title
# -----------------------------

st.markdown(
    '<div class="main-title">🏥 Healthcare MediAssist AI Chatbot</div>',
    unsafe_allow_html=True
)

st.write("")

# -----------------------------
# Layout
# -----------------------------

left_col, right_col = st.columns([1, 3])

# ==================================================
# LEFT SIDEBAR SECTION
# ==================================================

with left_col:

    st.header("📄 Upload Documents")

    pdf_files = st.file_uploader(
        "Select PDF Files",
        type=["pdf"],
        accept_multiple_files=True
    )

    if st.button("Upload PDFs"):

        if pdf_files:

            success_count = 0

            for pdf in pdf_files:

                files = {
                    "file": (
                        pdf.name,
                        pdf.getvalue(),
                        "application/pdf"
                    )
                }

                response = requests.post(
                    f"{BACKEND_URL}/upload",
                    files=files
                )

                if response.status_code == 200:
                    success_count += 1

            st.success(
                f"{success_count} document(s) uploaded successfully."
            )

    if pdf_files:

        st.subheader("Uploaded PDFs")

        for file in pdf_files:

            st.write("📄", file.name)

    st.divider()

    st.header("🖼 Upload Images")

    image_files = st.file_uploader(
        "Select Images",
        type=["png", "jpg", "jpeg"],
        accept_multiple_files=True
    )

    if image_files:

        for image in image_files:

            st.image(
                image,
                width=150
            )

    st.divider()

    st.header("⚙ System Status")

    try:

        health = requests.get(
            f"{BACKEND_URL}/health"
        )

        if health.status_code == 200:

            st.success("Backend Running")

        else:

            st.error("Backend Down")

    except:

        st.error("Cannot Connect Backend")

# ==================================================
# CHAT SECTION
# ==================================================

with right_col:

    st.subheader("💬 Ask Questions")

    question = st.text_input(
        "Enter your question"
    )

    col1, col2 = st.columns([1,1])

    with col1:

        ask_btn = st.button("Ask")

    with col2:

        clear_btn = st.button("Clear Chat")

    # ----------------------------------
    # Clear Chat
    # ----------------------------------

    if clear_btn:

        st.session_state.chat_history = []

    # ----------------------------------
    # Ask Question
    # ----------------------------------

    if ask_btn and question:

        try:

            response = requests.post(
                f"{BACKEND_URL}/chat",
                json={
                    "question": question
                }
            )

            data = response.json()

            answer = data.get(
                "answer",
                "No answer generated."
            )

            source = data.get(
                "source",
                "Unknown"
            )

            score = data.get(
                "score",
                0
            )

            st.session_state.chat_history.insert(
                0,
                {
                    "question": question,
                    "answer": answer,
                    "source": source,
                    "score": score
                }
            )

            # Keep only latest 10 chats

            st.session_state.chat_history = \
                st.session_state.chat_history[:10]

        except Exception as e:

            st.error(str(e))

    st.divider()

    st.subheader("📜 Conversation History")

    if len(st.session_state.chat_history) == 0:

        st.info("No conversation yet.")

    else:

        for chat in st.session_state.chat_history:

            st.markdown(
                f"""
                <div class='user-msg'>
                <b>You:</b><br>
                {chat['question']}
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <div class='bot-msg'>
                <b>MediAssist:</b><br>
                {chat['answer']}
                <br><br>

                <span class='source'>
                Source: {chat['source']}
                </span>

                <br>

                <span class='score'>
                Similarity Score: {round(chat['score'],4)}
                </span>

                </div>
                """,
                unsafe_allow_html=True
            )