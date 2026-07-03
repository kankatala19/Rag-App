import streamlit as st
import requests

import os

FASTAPI_URL = os.getenv(
    "FASTAPI_URL",
    "http://127.0.0.1:8000"
)
st.set_page_config(
    page_title="Simple RAG Assistant",
    page_icon="📄",
    layout="wide"
)

# -----------------------------
# Session State
# -----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("📄 Document Upload")

    uploaded_file = st.file_uploader(
        "Choose a file",
        type=["pdf", "txt", "docx", "md"]
    )

    if st.button("Upload Document"):

        if uploaded_file is None:
            st.warning("Please select a file.")
        else:

            with st.spinner("Uploading..."):

                files = {
                    "file": (
                        uploaded_file.name,
                        uploaded_file.getvalue(),
                        uploaded_file.type
                    )
                }

                response = requests.post(
                    f"{FASTAPI_URL}/upload",
                    files=files
                )

                data = response.json()

                if data["success"]:
                    st.success(data["message"])
                else:
                    st.error(data["message"])

    st.divider()

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

        st.rerun()

    if st.button("🗑 Clear Database"):

        response = requests.post(
            f"{FASTAPI_URL}/clear"
        )

        data = response.json()

        if data["success"]:

            st.session_state.messages = []

            st.success(data["message"])

            st.rerun()

        else:

            st.error(data["message"])

# -----------------------------
# Main Screen
# -----------------------------

st.title("🤖 Simple RAG Assistant")

st.caption("Upload a document and ask questions about it.")

# -----------------------------
# Show Previous Messages
# -----------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            sources = message.get("sources", [])

            if len(sources) > 0:

                with st.expander("📄 Sources"):

                    for source in sources:

                        st.write(
                            f"**File:** {source['file']}"
                        )

                        st.write(
                            f"**Page:** {source['page']}"
                        )

                        st.divider()

# -----------------------------
# Chat Input
# -----------------------------

question = st.chat_input("Ask a question...")

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.spinner("Thinking..."):

        response = requests.get(
            f"{FASTAPI_URL}/query",
            params={
                "question": question
            }
        )

        data = response.json()

        if data["success"]:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": data["answer"],
                    "sources": data.get("sources", [])
                }
            )

        else:

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": data["message"],
                    "sources": []
                }
            )

    st.rerun()